import grpc
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from google.protobuf.empty_pb2 import Empty

from config import available_servers
from proto.clock.clock_pb2 import AdjustClockRequest, FetchClockResponse
from proto.clock.clock_pb2_grpc import (
    ClockServiceStub,
    ClockServiceServicer,
)

# implementation of the ring election algorithm


class ClockService(ClockServiceServicer):
    def __init__(self, server_id: int) -> None:
        self.server_id = server_id
        self._offset = 0

        self.get_leader_id = None

    def configure(self, get_leader_id):
        self.get_leader_id = get_leader_id

    def get_local_time(self):
        return datetime.utcnow().timestamp() - self._offset

    def get_remote_time(self, server_id):
        try:
            start = time.time()
            response = self._send_fetch_clock_message(server_id)
            rtt = (time.time() - start) / 2
            return server_id, rtt + response.time
        except grpc.RpcError:
            return server_id, None

    def fetch_clock(self, request, context):
        print(f"Returning time {self.get_local_time()}")
        return FetchClockResponse(timestamp=self.get_local_time())

    def adjust_clock(self, request, context):
        print(f"Adjusting local time by {request.offset}")
        self._offset += request.offset
        return Empty()

    def sync_clock(self):
        print("Running clock sync!")
        futures = []
        with ThreadPoolExecutor(max_workers=len(available_servers)) as executor:
            for server_id in available_servers.values():
                futures.append(executor.submit(self.get_remote_time, server_id))

        node_times = {}
        for future in as_completed(futures):
            node_id, node_time = future.result()
            if node_time is not None:
                node_times[node_id] = node_time

        average_time = sum(node_times.values()) / len(node_times)
        node_offsets = {
            node_id: node_time - average_time for node_id, node_time in node_times.items()
        }

        futures = []
        with ThreadPoolExecutor(max_workers=len(available_servers)) as executor:
            for node_id, node_offset in node_offsets.items():
                futures.append(
                    executor.submit(self._send_adjust_clock_message, node_id, node_offset)
                )
        wait(futures)
        print(f"Clocks synced! Offsets: {node_offsets}")

    def set_node_time(self, server_id, time_str):
        try:
            t = datetime.strptime(time_str, "hh:mm:ss")
        except Exception:
            print("Invalid time format")
            return
        new_node_time = datetime.combine(datetime.utcnow().date(), t.time()).timestamp()

        if server_id != self.server_id:
            if self.server_id != self.get_leader_id():
                print(f"Only game master ({self.get_leader_id()}) can modify another nodes time!")
            else:
                _, node_time = self.get_remote_time(server_id)
                if not node_time:
                    print(f"Node {server_id} not responding!")
                else:
                    self._send_adjust_clock_message(server_id, node_time - new_node_time)
                    print("Time adjusted!")
        else:
            self._offset += self.get_local_time() - new_node_time
            print("Time adjusted!")

    def _create_stub(self, channel) -> ClockServiceStub:
        return ClockServiceStub(channel)

    def _send_fetch_clock_message(self, server_id):
        print(f"Fetching clock from server {server_id}")
        with grpc.insecure_channel(available_servers[server_id]) as channel:
            return self._create_stub(channel).fetch_clock(Empty())

    def _send_adjust_clock_message(self, server_id, offset):
        print(f"Adjusting clock on server {server_id} by {offset}s")
        with grpc.insecure_channel(available_servers[server_id]) as channel:
            return self._create_stub(channel).adjust_clock(AdjustClockRequest(offset=offset))

import grpc
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from google.protobuf.empty_pb2 import Empty

from config import available_servers
from proto.clock.clock import AdjustClockRequest, FetchClockResponse
from proto.clock.clock_grpc import (
    ClockServiceStub,
    ClockServiceServicer,
)

# implementation of the ring election algorithm


class ClockService(ClockServiceServicer):
    def __init__(self, server_id: int) -> None:
        self._offset = 0

    def get_local_time(self):
        return datetime.utcnow().timestamp() - self._offset

    def fetch_clock(self, request, context):
        return FetchClockResponse(timestamp=self.get_local_time())

    def adjust_clock(self, request, context):
        self._offset += request.offset
        return ring_pb2.Empty()

    def sync_clock(self):
        def get_time(server_id):
            try:
                start = time.time()
                self._send_fetch_clock_message(server_id)
                rtt = (time.time() - start) / 2
                return server_id, rtt + response.time
            except grpc.RpcError:
                return server_id, None

        futures = []
        with ThreadPoolExecutor(max_workers=len(available_servers)) as executor:
            for server_id in available_servers.values():
                futures.append(executor.submit(get_time, server_id))

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

import grpc
from google.protobuf.empty_pb2 import Empty

from config import available_servers
from proto.election.election_pb2 import CoordinationRequest, ElectionRequest
from proto.election.election_pb2_grpc import (
    ElectionServiceServicer,
    ElectionServiceStub,
)
from utils import find_next

# implementation of the ring election algorithm


class ElectionService(ElectionServiceServicer):
    def __init__(self, server_id: int) -> None:
        self.server_id = server_id
        self.leader_id = -1
        self.election_is_done = False

        self.start_game_callback = None
        self.sync_clock_callback = None
        self.is_game_in_progress = None

    def configure(self, start_game_callback, sync_clock_callback, is_game_in_progress):
        self.start_game_callback = start_game_callback
        self.sync_clock_callback = sync_clock_callback
        self.is_game_in_progress = is_game_in_progress

    def get_leader_id(self):
        return self.leader_id

    def elect(self, request, context):
        candidate_id = request.node_id

        if candidate_id == self.server_id:
            self.election_is_done = True
            self.leader_id = self.server_id
            print("Starting coordination process ...")
            return self._send_coordination_message(find_next(self.server_id), self.leader_id)

        # TODO: this implementation doesn't account for when a node goes down
        return self._send_election_message(
            find_next(self.server_id), max(self.server_id, candidate_id)
        )

    def coordinate(self, request, context):
        self.leader_id = request.leader_id

        if self.leader_id == self.server_id:
            if self.election_is_done:
                print(f"All nodes agreed on {self.server_id} to be a leader")
                self.sync_clock_callback()
                self.start_game_callback(
                    [pid for pid in available_servers if pid != self.server_id]
                )  # game creation #TODO: send only active servers as participants
                return Empty()
            else:
                self.election_is_done = True
        else:
            print(f"New leader is {self.leader_id}")

        return self._send_coordination_message(find_next(self.server_id), self.leader_id)

    def initiate(self):
        if not self.is_game_in_progress():
            self._send_election_message(find_next(self.server_id), self.server_id)
        else:
            print("The game is already in progress!")

    def _create_stub(self, channel) -> ElectionServiceStub:
        return ElectionServiceStub(channel)

    def _send_coordination_message(self, server_id, leader_id):
        print(f"Sending coordination message to server {server_id}")
        with grpc.insecure_channel(available_servers[server_id]) as channel:
            return self._create_stub(channel).coordinate(CoordinationRequest(leader_id=leader_id))

    def _send_election_message(self, server_id, leader_id):
        print(f"Sending election message to server {server_id} with leader_id {leader_id}")
        with grpc.insecure_channel(available_servers[server_id]) as channel:
            return self._create_stub(channel).elect(ElectionRequest(node_id=leader_id))

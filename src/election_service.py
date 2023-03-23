from typing import List
from utils import find_next
from google.protobuf.empty_pb2 import Empty
from proto.election.election_pb2_grpc import ElectionServiceServicer, ElectionServiceStub
from proto.election.election_pb2 import ElectionRequest, CoordinationRequest
from config import available_servers
import grpc


# implementation of the ring election algorithm

class ElectionService(ElectionServiceServicer):
    def __init__(self, server_id: int, callback) -> None:
        self.server_id = server_id
        self.num_of_processes = len(available_servers)
        self.servers = available_servers
        self.callback = callback
        self.leader_id = -1
        self.election_is_done = False
    
    def elect(self, request, context):
        candidate_id = request.node_id

        if candidate_id == self.server_id:
            self.election_is_done = True
            self.leader_id = self.server_id
            print("Starting coordination process ...")
            return self._send_coordination_message(find_next(self.server_id), self.leader_id)

        return self._send_election_message(find_next(self.server_id), max(self.server_id, candidate_id))

    def coordinate(self, request, context):
        leader_id = request.leader_id
        self.leader_id = leader_id

        if leader_id == self.server_id:
            if self.election_is_done:
                print(f"All nodes agreed on {self.server_id} to be a leader")
                # ToDo: probably suitable place for placing sync_clock_callback
                self.callback() # game creation
                return Empty()
            else: 
                self.election_is_done = True
        else:
            print(f"New leader is {self.leader_id}")
        
        return self._send_coordination_message(find_next(self.server_id), leader_id)

    def initiate(self):
        return self._send_election_message(find_next(self.server_id), self.server_id)

    def _create_stub(self, channel) -> ElectionServiceStub:
        return ElectionServiceStub(channel)

    def _send_coordination_message(self, server_id, leader_id):
        print(f'Sending coordination message to server {server_id}')
        with grpc.insecure_channel(available_servers[server_id]) as channel:
            return self._create_stub(channel).coordinate(CoordinationRequest(leader_id=leader_id))

    def _send_election_message(self, server_id, leader_id):
        print(f'Sending selection message to server {server_id} with leader_id {leader_id}')
        with grpc.insecure_channel(available_servers[server_id]) as channel:
            return self._create_stub(channel).elect(ElectionRequest(node_id=leader_id))


from typing import List
from grpc._channel import _InactiveRpcError
from proto.election_pb2_grpc import ElectionServiceStub
import proto.election_pb2 as election_pb2
import grpc

class ElectionClient:
    def __init__(self, node_id: int, servers: List[int], callback) -> None:
        self.node_id = node_id
        self.servers = servers
        self.callback = callback
    
    def elect(self):
        for id in self.servers:
            if self.node_id < id:
                try:
                    self.__get_stub(id).Election(election_pb2.ElectionRequest(node_id=id))
                    return
                except _InactiveRpcError:
                    print(f'Node {id} is unavailable')
        
        for id in self.servers:
            try:
                self.__get_stub(id).Broadcast(election_pb2.BroadcastRequest(node_id=self.node_id))
            except _InactiveRpcError:
                continue
        
        self.callback(self.node_id)

    def __get_stub(self, id) -> ElectionServiceStub:
        channel = grpc.insecure_channel('localhost:5000{id}')
        return ElectionServiceStub(channel)

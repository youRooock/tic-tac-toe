from concurrent import futures

import grpc

from clock_service import ClockService
from config import available_servers
from election_service import ElectionService
from game_service import GameService
from proto.clock.clock_pb2_grpc import add_ClockServiceServicer_to_server
from proto.election.election_pb2_grpc import add_ElectionServiceServicer_to_server
from proto.game.game_pb2_grpc import add_GameServiceServicer_to_server


class Server:
    def __init__(
        self,
        server_id: int,
        election_service: ElectionService,
        game_service: GameService,
        clock_service: ClockService,
    ) -> None:
        self.server_id = server_id
        self.election_service = election_service
        self.game_service = game_service
        self.clock_service = clock_service

    def start(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_ElectionServiceServicer_to_server(self.election_service, server)
        add_GameServiceServicer_to_server(self.game_service, server)
        add_ClockServiceServicer_to_server(self.clock_service, server)
        server.add_insecure_port(available_servers[self.server_id])
        server.start()
        print(f"server {self.server_id} is up and running ...")
        server.wait_for_termination()

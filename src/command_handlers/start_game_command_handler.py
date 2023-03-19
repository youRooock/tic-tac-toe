from .handler import Handler
from ..election_client import ElectionClient
from ..server import Server
from ..config import servers
from typing import List

class StartGameCommandHandler(Handler):
    def __init__(self, node_id: int, servers: List[int], server: Server):
        self.election_client = ElectionClient(node_id, servers, server.on_elected)

    def handle(self, args):
       node_id = args[0]

       self.election_client.elect()

    def start_server():
        pass
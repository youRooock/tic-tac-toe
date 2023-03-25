from typing import List

from config import available_servers
from election_service import ElectionService

from .handler import Handler


class StartGameCommandHandler(Handler):
    def __init__(self, election_service: ElectionService):
        self.election_service = election_service

    def handle(self, args):
        # ToDo:
        # syck clock should happen here as well
        # we can pass another callback to trigger clock sync
        # see how it's done for game callback
        return self.election_service.initiate()

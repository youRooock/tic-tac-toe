from .handler import Handler


class StartGameCommandHandler(Handler):
    def __init__(self, election_service):
        self.election_service = election_service

    def handle(self, args):
        return self.election_service.initiate()

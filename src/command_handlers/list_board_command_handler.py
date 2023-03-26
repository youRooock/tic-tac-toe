from .handler import Handler


class ListBoardCommandHandler(Handler):
    def __init__(self, game_service):
        self.game_service = game_service

    def handle(self, args):
        self.game_service.list_board()

from .handler import Handler


class SetSymbolCommandHandler(Handler):
    def __init__(self, game_service):
        self.game_service = game_service

    def handle(self, args):
        position = args[0]
        self.game_service.set_user_turn(position)

from .handler import Handler


class SetSymbolCommandHandler(Handler):
    def __init__(self, game_service):
        self.game_service = game_service

    def handle(self, args):
        self.game_service.set_user_turn(int(args[0]))

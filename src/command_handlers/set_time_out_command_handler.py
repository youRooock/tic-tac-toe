from .handler import Handler


class SetTimeOutCommandHandler(Handler):
    def __init__(self, game_service):
        self.game_service = game_service

    def handle(self, args):
        role, timeout_in_mins = args[0], int(args[1])
        self.game_service.refresh_timer(role, timeout_in_mins)
from .handler import Handler


class SetNodeTimeCommandHandler(Handler):
    def __init__(self, clock_service):
        self.clock_service = clock_service

    def handle(self, args):
        self.clock_service.set_node_time(int(args[0]), args[1])

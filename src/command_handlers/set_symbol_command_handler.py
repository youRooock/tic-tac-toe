from .handler import Handler

class SetSymbolCommandHandler(Handler):
    def handle(self, args):
        position, mark = args[0], args[1]
        
        # send these args to the leader and receive a current representation of board as a string
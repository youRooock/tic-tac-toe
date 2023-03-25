from random import shuffle

import grpc
from google.protobuf.empty_pb2 import Empty

import proto.game.game_pb2 as game_pb2
from config import available_servers
from game import Game
from mark import Mark
from player import Player
from proto.game.game_pb2_grpc import GameServiceServicer, GameServiceStub
from utils import find_next


class GameService(GameServiceServicer):
    def __init__(self, server_id: int) -> None:
        self.game = Game()
        marks = [Mark.X.value, Mark.O.value]
        shuffle(marks)
        self.player_one = Player(find_next(server_id), marks[0])
        self.player_two = Player(find_next(self.player_one.id), marks[-1])
        super().__init__()

    def set_mark(self, request, context):
        # ToDo: implement
        # modify game object, return to the caller string board,  make decision about winner, inform the second player with the actual board
        pass

    def inform(self, request, context):
        message = request.message

        print("okay, I'm starting!")

        return Empty()

    def set_user_turn(self):
        pass
        # ToDo: this method should be called in Set Symbol handler
        # it should:
        # 1. make rpc set_mark call
        # 2. print board after the move

    def list_board(self):
        pass
        # ToDo: this method should be called in list board handler
        # it should:
        # 1. if it's a host -- return current game board
        # 2. if it's a player -- probably add another rpc to game.proto and retrieve from the host current board

    def start_game(self):
        print("The game has started!")
        start_player = self.player_one if self.player_one.mark == Mark.X else self.player_two
        with grpc.insecure_channel(available_servers[start_player.id]) as channel:
            stub = GameServiceStub(channel)
            return stub.inform(
                game_pb2.InformRequest(message="Please start!")
            )  # ToDo: send here board string representation

import random

import grpc
import time
from threading import Thread, Event
from google.protobuf.empty_pb2 import Empty

from config import available_servers
from game import Game
from mark import Mark
from player import Player
from proto.game.game_pb2 import InformMessage, SetMarkRequest
from proto.game.game_pb2_grpc import GameServiceServicer, GameServiceStub
from utils import find_next

DEFAULT_TIME_OUT_MINS = 1

class GameService(GameServiceServicer):
    def __init__(self, server_id: int) -> None:
        self.server_id = server_id

        self.game = None
        self.is_player = False

        self.get_local_time = None
        self.get_game_master_id = None
        self.time_out = DEFAULT_TIME_OUT_MINS * 60

    def configure(self, get_time_function, get_game_master_id):
        self.get_local_time = get_time_function
        self.get_game_master_id = get_game_master_id

    def set_mark(self, request, context):
        if not self.game:
            raise grpc.RpcError("Sory, the game is not in progress!")
        if self.server_id != self.get_game_master_id():
            raise grpc.RpcError("Sory, this server doesn't host the game!")
        if request.server_id not in self.game.player_ids:
            raise grpc.RpcError("Sory, you are not one of the players in the game!")

        player = self.game.get_player_by_id(request.server_id)
        try:
            self.game.set_mark(request.timestamp, request.position, player)
        except Exception as e:
            raise grpc.RpcError(str(e))
        
        self.last_player_action_at = time.time()
        board_repr = str(self.game.board)
        if self.game.is_finished():
            winner = self.game.winner
            for p in self.game.players:
                self._send_end_game_message(
                    p.id,
                    f"The game has finished! The winner is {winner.mark.value} ({winner.id})! Board:\n{board_repr}",
                )
            self.game = None
            return InformMessage(message="")
        else:
            self._send_inform_message(
                self.game.get_opposite_player(player).id,
                f"Your turn! Board:\n{board_repr}",
            )

        return InformMessage(message=f"Success! Board:\n{board_repr}")

    def start_game(self, request, context):
        print(request.message)
        self.is_player = True
        return Empty()

    def end_game(self, request, context):
        print(request.message)
        self.is_player = False
        return Empty()

    def inform(self, request, context):
        print(request.message)
        return Empty()

    def get_board(self, request, context):
        if not self.game:
            raise grpc.RpcError("Sory, the game is not in progress!")

        return InformMessage(f"Board:\n{str(self.game.board)}")

    def set_user_turn(self, position):
        try:
            resp = self._send_set_mark_message(
                server_id=self.get_game_master_id(), position=position
            )
            print(resp.message)
        except grpc.RpcError as e:
            print(str(e))

    def list_board(self):
        if not self.game and not self.is_player:
            print("Game is not in progress!")
        elif self.server_id == self.get_game_master_id():
            print(str(self.game.board))
        else:
            try:
                resp = self._send_get_board_message(self.get_game_master_id())
                print(resp.message)
            except grpc.RpcError as e:
                print(e)

    def initiate(self, potential_player_ids):
        if len(potential_player_ids) < 2:
            raise Exception("Not enough players to start a game!")
        
        self.timer_thread = Thread(target=self._master_timer_job, args=(DEFAULT_TIME_OUT_MINS * 60,))
        self.last_player_action_at = time.time()
        self.timer_thread.start()

        print("The game has started!")
        player_X, player_O = [
            Player(pid, mark)
            for pid, mark in zip(random.sample(potential_player_ids, 2), [Mark.X, Mark.O])
        ]
        self.game = Game(player_X, player_O)

        self._send_start_game_message(
            self.game.player_X.id, "The game has started! Player X, you go first!"
        )
        self._send_start_game_message(
            self.game.player_O.id, "The game has started! Player O, please standby!"
        )

    def refresh_timer(self, role, timeout_in_mins):
        if role == 'players' and not self.is_player:
            self.time_out = timeout_in_mins * 60
            print(f'Set players timeout to {timeout_in_mins} mins')

    def _master_timer_job(self, timeout):
        while True:
            diff = time.time() - self.last_player_action_at
            if diff > self.time_out:
                if not self.game.is_finished():
                    print('The game has timed out!')

                    for p in self.game.players:
                        self._send_end_game_message(p.id, 'The game has timed out!') 
                    self.game = None
                break
            time.sleep(1)

    def _create_stub(self, channel) -> GameServiceStub:
        return GameServiceStub(channel)

    def _send_inform_message(self, server_id, message):
        print(f"Sending inform message to server {server_id} with message {message}")
        with grpc.insecure_channel(available_servers[server_id]) as channel:
            return self._create_stub(channel).inform(InformMessage(message=message))

    def _send_set_mark_message(self, server_id, position):
        print(f"Sending set mark message to server {server_id} with position {position}")
        with grpc.insecure_channel(available_servers[server_id]) as channel:
            return self._create_stub(channel).set_mark(
                SetMarkRequest(
                    position=position, server_id=self.server_id, timestamp=self.get_local_time()
                )
            )

    def _send_start_game_message(self, server_id, message):
        print(f"Sending start game message to server {server_id} with message {message}")
        with grpc.insecure_channel(available_servers[server_id]) as channel:
            return self._create_stub(channel).start_game(InformMessage(message=message))

    def _send_end_game_message(self, server_id, message):
        print(f"Sending end game message to server {server_id} with message {message}")
        with grpc.insecure_channel(available_servers[server_id]) as channel:
            return self._create_stub(channel).end_game(InformMessage(message=message))

    def _send_get_board_message(self, server_id):
        print(f"Sending get board message to server {server_id}")
        with grpc.insecure_channel(available_servers[server_id]) as channel:
            return self._create_stub(channel).get_board(Empty())

from player import Player
from tic_tac_toe_board import TicTacToeBoard
from datetime import datetime


class Game:
    def __init__(self, player_X, player_O) -> None:
        self.grid_size = 3
        self.board = TicTacToeBoard(self.grid_size)

        self.player_X = player_X
        self.player_O = player_O

        self.turns = []
        self.winner = None

    def set_mark(self, timestamp: float, position: int, player: Player) -> None:
        if self.turns and self.turns[-1].player == player:
            raise Exception("Player can not make two moves in a row")
        if self.turns and self.turns[-1].timestamp > timestamp:
            raise Exception(
                f"Time desync detected! "
                f"Last turn was made at {self.turns[-1].timestamp}, "
                f"but you are trying to make a turn at {timestamp}. "
                f"Please adjust your clock and try again, or restart the game!"
            )

        self.board.set_cell(player.mark, position)
        self.turns.append(Turn(timestamp, position, player))

        if self.board.is_crossed(player.mark):
            self.winner = player

    def is_finished(self) -> bool:
        return self.winner != None

    @property
    def players(self):
        return (self.player_X, self.player_O)

    @property
    def player_ids(self):
        return (self.player_X.id, self.player_O.id)

    def get_player_by_id(self, server_id: int):
        return {p.id: p for p in (self.player_X, self.player_O) if p}.get(server_id)

    def get_opposite_player(self, player: Player):
        return self.player_X if self.player_O == player else self.player_O
    
    def __str__(self):
        turns = []

        for turn in self.turns:
            turns.append(f'{datetime.fromtimestamp(turn.timestamp)}: Player #{turn.player.id} played {turn.player.mark.value} at the position {turn.position}')
        
        return "\n".join(turns)



class Turn:
    def __init__(self, timestamp, position, player):
        self.timestamp = timestamp
        self.position = position
        self.player = player

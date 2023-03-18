from tic_tac_toe_board import TicTacToeBoard
from player import Player


class Game:
    def __init__(self) -> None:
        self.grid_size = 3
        self.prev_move_by = None
        self.winner = None
        self.board = TicTacToeBoard(self.grid_size)

    def set_mark(self, position: int, player: Player) -> None:
        if player == self.prev_move_by:
            raise Exception('Player cannot have two moves in a row')
        
        self.prev_move_by = player
        self.board.set_cell(player.mark, position)

        if self.board.is_crossed(player.mark):
            self.winner = player

    def is_finished(self) -> bool:
        return self.winner != None
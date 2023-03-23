from mark import Mark


class TicTacToeBoard:
    def __init__(self, size: int) -> None:
        self.size = size
        self.cells = [None] * size ** 2
    
    def set_cell(self, mark: Mark, position: int) -> None:
        if position <= 0 or position > self.size ** 2:
            raise Exception('Position is outside the boarder')
        if self.cells[position-1]:
            raise Exception('The cell is already set')
        self.cells[position-1] = mark.value

    def is_crossed(self, mark: Mark):
        # Check rows
        for i in range(self.size):
            row = self.cells[i*self.size : (i+1)*self.size]
            if all([x == mark.value for x in row]):
                return True
        
        # Check columns
        for i in range(self.size):
            col = [self.cells[x] for x in range(i, self.size * self.size, self.size)]
            if all([x == mark.value for x in col]):
                return True

        # Check left-to-right diagonal
        diag = [self.cells[x] for x in range(0, self.size * self.size, self.size + 1)]
        if all([x == mark.value for x in diag]):
            return True

        # Check right-to-left diagonal
        anti_diag = [self.cells[i] for i in range(self.size-1, self.size * self.size-self.size + 1, self.size - 1)]
        if all([x == mark.value for x in anti_diag]):
            return True

        return False
    
    def __str__(self) -> str:
        #ToDo: fancy board convertion to string in order to send to players
        pass
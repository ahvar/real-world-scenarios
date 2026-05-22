from typing import Optional
from player import DiscColor


class Board:

    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._grid = [[None] * cols for _ in range(rows)]

    def get_rows(self):
        return self._rows

    def get_cols(self):
        return self._cols

    def can_place(self, column):
        if column < 0 or column >= self._cols:
            return False
        if None not in self.get_cols():
            return False

    def place_disc(self, col, color: DiscColor):

        rows = self.get_rows()
        curr = 0
        while curr < rows:
            if self.get_cell(curr, col) == None:
                self._grid[curr][col] = color

    def check_win(self, color, col):
        pass

    def is_full(self):
        pass

    def get_cell(self, row: int, col: int) -> Optional[DiscColor]:
        pass

    @property
    def board(self):
        return self._board

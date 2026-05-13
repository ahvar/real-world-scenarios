from enum import Enum
from typing import List, Optional


class DiscColor(Enum):
    RED = "RED"
    YELLOW = "YELLOW"


class Board:
    def __init__(self, rows: int = 6, cols: int = 7):
        self.rows = rows
        self.cols = cols
        self.grid: List[List[Optional[DiscColor]]] = [
            [None] * cols for _ in range(rows)
        ]

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def can_place(self, column: int):
        if column < 0 or column >= self.cols:
            return False
        return self.grid[0][column] is None

    def place_disc(self, column: int, color: DiscColor):
        if not self.can_place(column):
            return -1
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][column] is None:
                self.grid[row][column] = color
                return row
        return -1

    def is_full(self):
        pass

    def get_cell(self, row: int, col: int):
        pass

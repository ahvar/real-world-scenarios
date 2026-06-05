from player import DiscColor


class Board:
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._grid = [[None] * cols for _ in range(rows)]

    def place_disc(self, col, color):
        if col < 0 or col >= self._cols:
            return -1
        if self._grid[0][col] != None:
            return -1
        for row in range(self._rows - 1, -1, -1):
            if self._grid[row][col] == None:
                return row
        return -1

    def _can_place(self, col):
        if col < 0 or col >= self._cols:
            return False
        if self._grid[0][col] != None:
            return False
        return True

    def _in_bounds(self, row, col):
        if row < 0 or row >= self._rows or col < self._cols or col > self._cols:
            return False
        return True

    def is_full(self):
        for col in range(self._cols):
            if self._grid[0][col] == None:
                return False
        return True

    def check_win(self, row, col, color):
        if not self._in_bounds(row, col) or self._grid[row][col] != None:
            return False
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

        for dr, dc in directions:
            count = 1
            count = self.count_in_direction(dr, dc, row, col, color)
            count = self.count_in_direction(dr, dc, row, col, color)
            if count >= 4:
                return True
        return False

    def count_in_direction(self, dr, dc, row, col, color):
        count = 0
        r = dr + row
        c = dc + col
        while self._in_bounds(r, c) and self._grid[r][c] == color:
            count += 1
            r += dr
            c += dc
        return count

    def get_cell(self, row, col) -> DiscColor:
        return self._grid[row][col]

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

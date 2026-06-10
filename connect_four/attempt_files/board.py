class Board:

    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._grid = [[None] * cols for _ in range(rows)]

    def can_place(self, column) -> bool:
        if column < 0 or column >= self._cols:
            return False
        return self._grid[0][column] == None

    def place_disc(self, column, color):
        if not self.can_place(column):
            return -1
        if self._grid[0][column] != None:
            return -1

        for row in range(self._rows - 1, -1, -1):
            if self._grid[row][column] == None:
                self._grid[row][column] == color
                return row
        return -1

    def check_win(self, row, column, color):

        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for dr, dc in directions:
            count = 1
            count += self._count_in_direction(row, column, color, dr, dc)
            count += self._count_in_direction(row, column, color, -dr, -dc)
        if count >= 4:
            return True
        return False

    def _count_in_direction(self, row, column, color, dr, dc):
        count = 0
        r = row + dr
        c = column + dc
        while self._in_bounds(r, c) and self._grid[row][column] == color:
            count += 1
            r += dr
            c += dc
        return count

    def is_full(self):
        for col in range(self._cols):
            if self._grid[0][col] == None:
                return False
        return True

    def _in_bounds(self, row, col):
        if row < 0 or row >= self._rows or col < 0 or col >= self._cols:
            return False

        return True

    def get_cell(self, row, col):
        if not self._in_bounds(row, col):
            return -1

        return self._grid[row][col]

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @property
    def grid(self):
        return self._grid

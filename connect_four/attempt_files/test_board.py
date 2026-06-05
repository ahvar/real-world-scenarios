from board import Board
from board import DiscColor


class TestBoard:
    def setup_method(self):
        self._board = Board(6, 7)

    def test_board_construction(self):
        assert self._board.rows == 6 and self._board.cols == 7

    def test_place_disc_empty_board(self):
        assert self._board.place_disc(10, DiscColor.RED) == -1
        assert self._board.place_disc(0, DiscColor.RED) == 5

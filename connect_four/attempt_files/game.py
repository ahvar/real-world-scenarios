from enum import Enum
from board import Board


class GameState:
    WON = "WON"
    IN_PROGRESS = "IN_PROGRESS"
    DRAW = "DRAW"


class Game:
    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2
        self._board = Board()
        self._current_player = p1
        self._game_state = GameState.IN_PROGRESS

    def make_move(self, player, column):
        if self._game_state != GameState.IN_PROGRESS:
            return
        if player != self._current_player:
            return

        row = self._board.place_disc()

    @property
    def game_state(self):
        return self._game_state

    @property
    def board(self):
        return self._board

    @property
    def current_player(self):
        return self._current_player

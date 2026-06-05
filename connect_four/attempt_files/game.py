from enum import Enum
from board import Board
from player import Player


class GameState:
    DRAW = "DRAW"
    IN_PROGRESS = "IN_PROGRESS"
    IDLE = "IDLE"


class Game:

    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2
        self._game_state = GameState.IN_PROGRESS
        self._current_player = p1
        self._board = Board()

    def make_move(self, player, column):
        if player != self._current_player:
            return False

        self._board.place_disc(column, player.color)

    def get_winner(self):
        pass

    @property
    def current_player(self):
        return self._current_player

    @property
    def board(self):
        return self._board

    @property
    def game_state(self):
        return self._game_state


if __name__ == "__main__":
    p1 = Player("arthur", "red")
    p2 = Player("carlo", "yellow")
    game = Game(p1, p2)

from player import Player
from board import Board
from enum import Enum


class GameState(Enum):
    IN_PROGRESS = 1
    WON = 2
    DRAW = 3



class Game:

    def __init__(self):
        self._players = [Player("fred", "red"), Player("carl", "blue")]
        self._game_state = GameState()
        self._board = Board()

    def make_move(self, player, column: int):
        if player not in self._players:
            return
        if column

    def get_current_player(self):
        pass

    def get_game_state(self):
        pass

    def get_winner(self):
        pass

    def get_board(self):
        return self._board

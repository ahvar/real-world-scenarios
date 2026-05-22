from board import Board
from player import Player


class GameState:
    IN_PROGRESS = "IN_PROGRESS"
    WON = "WON"
    DRAW = "DRAW"


class Game:
    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2
        self._current_player = None
        self._winner = None
        self._board = Board()
        self._game_state = GameState.IN_PROGRESS

    def make_move(self, player, column) -> bool:
        if self._game_state != GameState.IN_PROGRESS:
            return False
        if self._current_player != player:
            return False

        row = self._board.place_disc(column, player.color)
        if row == -1:
            return False

        if self._board.check_win(row, column, player.color):
            self._game_state = GameState.WON
            self._winner = None
        elif self._board.is_full():
            self._game_state = GameState.DRAW
        else:
            self._current_player = (
                self._p2 if self._current_player is self._p1 else self._p1
            )
        return True

    def get_current_player(self):
        pass

    def get_game_state(self) -> GameState:
        pass

    def get_winner(self):
        pass

    def get_board(self):
        pass


if __name__ == "__main__":
    p1 = Player("Arthur", "RED")
    p2 = Player("Carlo", "YELLOW")
    game = Game(p1, p2)

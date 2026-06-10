from enum import Enum


class DiscColor(Enum):
    RED = "RED"
    YELLOW = "YELLOW"


class Player:

    def __init__(self, name, color):
        self._name = name
        self._color = color

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    def __eq__(self, other):
        return other.color == self._color and other.name == self._name

from enum import Enum


class DiscColor:
    RED = "RED"
    YELLOW = "YELLOW"


class Player:
    def __init__(self, name: str, color: DiscColor):
        self._name = name
        self._color = color

    def __eq__(self, other) -> bool:
        return self._name == other.name and self._color == other.color

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

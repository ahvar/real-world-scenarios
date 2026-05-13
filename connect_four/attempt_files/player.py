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
        return self._name == other.name and self._color == other.color

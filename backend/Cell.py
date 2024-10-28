from enum import Enum


class Color(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    VOID = -1

    @classmethod
    def swap_turn(self, curr):
        if curr == Color.BLACK:
            return Color.WHITE
        elif curr == Color.WHITE:
            return Color.BLACK


class Cell:
    def __init__(self):
        self.state = Color.VOID

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

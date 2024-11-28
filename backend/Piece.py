from enum import Enum

from backend.Cell import Color


class Piece:
    def __init__(self, color):
        self.color = color
        self.position = (-1, -1)

    def get_turn(self):
        return self.color

    def get_position(self):
        return self.position

    def set_turn(self, color):
        self.color = color

    def set_position(self, position):
        self.position = position
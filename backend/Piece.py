from enum import Enum


class Turn(Enum):
    BLACK = 1
    WHITE = 2

    @classmethod
    def swap_turn(self, curr):
        if curr == Turn.BLACK:
            return Turn.WHITE
        else:
            return Turn.BLACK

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


class Pieces():
    def __init__(self, total):
        self.white_pieces = []
        self.black_pieces = []

        for _ in range(total):
            self.white_pieces.append(Piece(Turn.WHITE))
            self.black_pieces.append(Piece(Turn.BLACK))

        self.count_white_placed = 0
        self.count_black_placed = 0
        self.size = total
    
    # delete this if it doesn't get used -- support for frontend/testing
    # def get_white_piece_positions(self):
    #     pos = []
    #     for piece in self.white_pieces:
    #         pos.append(piece.get_position())
    #     return pos
    # def get_black_piece_positions(self):
    #     pos = []
    #     for piece in self.black_pieces:
    #         pos.append(piece.get_position())
    #     return pos

    # private methods for increasing piece counts
    def __increase_count_white_placed(self):
        self.count_white_placed += 1
    def __increase_count_black_placed(self):
        self.count_black_placed += 1
    
    #only all_pieces_placed is public!
    def __all_white_placed(self):
        if self.count_white_placed < self.size:
            return False
        return True
    def __all_black_placed(self):
        if self.count_black_placed < self.size:
            return False
        return True
    def all_pieces_placed(self):
        if self.__all_white_placed() and self.__all_black_placed():
            return True
        return False
    
    def set_white_piece(self, row, column):
        if self.__all_white_placed():
            return "PiecePlacementError -- Cannot place more white pieces"
        self.white_pieces[self.count_white_placed].set_position((row, column))
        self.__increase_count_white_placed()
        return 1
    def set_black_piece(self, row, column):
        if self.__all_black_placed():
            return "PiecePlacementError -- Cannot place more black pieces"
        self.black_pieces[self.count_black_placed].set_position((row, column))
        self.__increase_count_black_placed()
        return 1
from backend.Piece import Piece
from backend.Cell import Color
class Player:
    def __init__(self, max_piece_count, color):
        self.pieces = []
        self.color = color
        self.pieces = [Piece(color) for _ in range(max_piece_count)]

        self.piece_index = 0
        self.pieces_placed = 0
        self.starting_piece_count = max_piece_count

    # only all_pieces_placed is public!
    def all_of_players_pieces_placed(self):
        # iterate over all pieces and check if they have a position not equal to (-1, -1)
        for piece in self.pieces:
            if piece.get_position() == (-1, -1):
                return False
        return True
    
    def all_pieces_placed(self):
        if self.all_of_players_pieces_placed() and self.__all_black_placed():
            return True
        return False

    def set_players_piece(self, row, column):
        if self.all_of_players_pieces_placed():
            return "PiecePlacementError -- Cannot place more white pieces"
        self.pieces[self.piece_index].set_position((row, column))
        self.piece_index += 1
        self.pieces_placed += 1
        return 1

    def remove_piece(self, row, col):
        for piece in self.pieces:
            if piece.get_position() == (row, col):
                self.pieces.remove(piece)
                self.piece_index -= 1
                break

    def get_color(self):
        return self.color
    
    def get_placed_pieces_position(self):
        return [piece.get_position() for piece in self.pieces if piece.get_position() != (-1, -1)]
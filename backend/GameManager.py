# import pygame as pg
from backend.Board import Board
from backend.Piece import Pieces, Turn

class GameManager:
    def __init__(self, size, pieces):
        self.board = Board(size)
        self.pieces = Pieces(pieces)
        self.turn = Turn.WHITE

        self.all_possible_moves = self.board.get_valid_moves()
        self.current_moves = self.all_possible_moves

    def get_board(self, row=-1, col=-1):
        if row == -1 or col == -1:
            return self.board
        return self.board.check_position(row, col)

    def get_turn(self):
        if self.turn == Turn.WHITE:
            return 'white'
        else:
            return 'black'
    
    def placement_complete(self):
        return self.pieces.all_pieces_placed()

    def piece_placement(self, row, column):
        if (row, column) in self.current_moves:
            if self.board.check_position(row, column) != "empty":
                print(self.board.check_position(row, column).lower())
                return "GameManagerError -- position not empty"
            
            isPiecePlaced = 0
            if self.turn == Turn.WHITE:
                isPiecePlaced = self.pieces.set_white_piece(row, column)
            else:
                isPiecePlaced = self.pieces.set_black_piece(row, column)


            if isPiecePlaced == 1:
                self.board.set_position(row, column, self.turn.name.lower())
                self.current_moves.remove((row, column))
                return 1
            #else error -- figure out handling. are we making error classes?
            return 0

        else:
            return "GameManagerError -- invalid piece placement position"
        
    # function for getting the current amount of pieces left to be placed
    def get_pieces_left(self):
        # dictionary for black and white pieces left to be placed
        return {"white": self.pieces.size - self.pieces.count_white_placed, "black": self.pieces.size - self.pieces.count_black_placed}
    
    def end_turn(self):
        self.turn = Turn.swap_turn(self.turn)
        return 1
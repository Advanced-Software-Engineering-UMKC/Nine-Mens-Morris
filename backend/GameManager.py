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

    def piece_placement(self, row, column):
        if (row, column) in self.current_moves:
            flag_board = 0
            flag_piece = 0
            if self.turn == Turn.WHITE:
                flag_piece = self.pieces.set_white_piece(row, column)
                if flag_piece == 1:
                    flag_board = self.board.set_position(row, column, 'white')
            else:
                flag_piece = self.pieces.set_black_piece(row, column)
                if flag_piece == 1:
                    flag_board = self.board.set_position(row, column, 'black')


            if flag_board == 1 and flag_piece == 1:
                self.current_moves.remove((row, column))
                return 1
            #else error -- figure out handling. are we making error classes?
            return 0

        else:
            return "GameManagerError -- invalid piece placement position"
    
    def end_turn(self):
        self.turn = Turn.swap_turn(self.turn)
        return 1
# import pygame as pg
from backend.Board import Board
from backend.Cell import CellType
from backend.Piece import Pieces, Turn


class GameManager:
    def __init__(self, size, pieces):
        self.board = Board(size)
        self.pieces = Pieces(pieces)
        self.turn = Turn.WHITE
        self.selected_piece = None
        self.all_possible_moves = self.board.get_valid_moves()
        self.current_moves = self.all_possible_moves
        

    def get_board(self, row=-1, col=-1):
        if row == -1 or col == -1:
            return self.board
        return self.board.check_position(row, col)

    def get_turn(self):
        return self.turn

    def get_turn_as_string(self):
        return self.turn.name.lower()

    def placement_complete(self):
        return self.pieces.all_pieces_placed()

    def place_piece(self, row, column):
        if (row, column) in self.current_moves:
            if self.board.check_position(row, column) != CellType.EMPTY:
                print(self.board.check_position(row, column))
                return "GameManagerError -- position not empty"

            is_piece_placed = 0
            if self.turn == Turn.WHITE:
                is_piece_placed = self.pieces.set_white_piece(row, column)
            else:
                is_piece_placed = self.pieces.set_black_piece(row, column)

            if is_piece_placed == 1:
                self.board.set_position(row, column, self.turn.name.lower())
                self.current_moves.remove((row, column))
                return 1
            # else error -- figure out handling. are we making error classes?
            return 0

        else:
            return "GameManagerError -- invalid piece placement position"

    # function for getting the current amount of pieces left to be placed
    def get_pieces_left(self):
        # dictionary for black and white pieces left to be placed
        return {
            "white": self.pieces.size - self.pieces.count_white_placed,
            "black": self.pieces.size - self.pieces.count_black_placed,
        } 

    def end_turn(self):
        self.turn = Turn.swap_turn(self.turn)
        return 1

        
        
    def is_adjacent(self, current_row, current_col, target_row, target_col):
        """ Check if the target position is adjacent to the current position """
        return (target_row, target_col) in self.board.adjacent_positions_map.get((current_row, current_col), [])

    def is_empty(self, row, col):
        """ Check if the cell at (row, col) is empty """
        return self.board.board[row][col] is None

    def is_adjacent_and_empty(self, current_row, current_col, target_row, target_col):
        """ Check if the target cell is adjacent to the current cell and is empty """
        if self.is_adjacent(current_row, current_col, target_row, target_col):
            if (target_row, target_col) in self.all_possible_moves:
                return True
        return False
    
    
    def select_piece(self, row, col):
        if not self.placement_complete():
            print("SelectionError -- Cannot select pieces during placement phase")
            return False
        
        if self.turn == Turn.WHITE and self.board.check_position(row, col) == CellType.WHITE:
            self.selected_piece = (row, col)
            return True
        
        if self.turn == Turn.BLACK and self.board.check_position(row, col) == CellType.BLACK:
            self.selected_piece = (row, col)
            return True
        
        print("SelectionError -- Invalid piece selection")
        return False
        
    def move_piece(self, target_row, target_col):
        if not self.selected_piece:
            return "MoveError -- No piece selected"
        
        start_row, start_col = self.selected_piece

        # Validate the target position is empty and adjacent
        if self.board.check_position(target_row, target_col) != CellType.EMPTY:
            return "MoveError -- Target position is not empty"
        
        if not self.is_adjacent_and_empty(start_row, start_col, target_row, target_col):
            return "MoveError -- Invalid move, pieces can only move to adjacent positions"

        # Perform the move
        self.board.set_position(target_row, target_col, self.turn.name.lower())
        self.board.set_position(start_row, start_col, CellType.EMPTY)
        self.selected_piece = None

        return True

    def get_piece_at(self, row, col):
        return self.board.board[row][col]  

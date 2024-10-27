# import pygame as pg
from backend.Board import Board
from backend.Piece import Pieces, Turn
from backend.Cell import Color


class GameManager:
    def __init__(self, size, pieces):
        self.board = Board(size)
        self.pieces = Pieces(pieces)
        self.turn = Color.WHITE
        self.selected_piece = None
        self.current_moves = self.board.get_valid_moves()

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
            if self.board.check_position(row, column) != Color.EMPTY:
                print(self.board.check_position(row, column))
                return "GameManagerError -- position not empty"

            is_piece_placed = 0
            if self.turn == Color.WHITE:
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
            if (target_row, target_col) in self.current_moves:
                return True
        return False

    def filter_empty_adjacent(self, adjacent_positions):
        filtered_adjacent_positions = []
        for row, col in adjacent_positions:
            if self.board.check_position(row, col) == Color.EMPTY or self.board.check_position(row, col) == Color.VOID:
                filtered_adjacent_positions.append((row, col))

        return filtered_adjacent_positions

    '''
    the select_piece func should return the available empty adjacent positions to where the piece can be moved 
    or throw exception if it should be selectable
    '''
    def select_piece(self, row, col):
        if not self.placement_complete():
            raise Exception("SelectionError -- Cannot select pieces during placement phase")

        cell = self.board.get_cell(row, col)
        if self.turn == Color.WHITE and cell.get_state() == Color.WHITE:
            # calculate the available adjacent positions
            return self.filter_empty_adjacent(self.board.adjacent_positions_map[(row, col)])

        if self.turn == Color.BLACK and self.board.check_position(row, col) == Color.BLACK:
            # calculate the available adjacent positions
            return self.filter_empty_adjacent(self.board.adjacent_positions_map[(row, col)])

        raise Exception("SelectionError -- Invalid piece selection")

    def move_piece(self, target_row, target_col):
        if not self.selected_piece:
            return "MoveError -- No piece selected"

        start_row, start_col = self.selected_piece

        # Validate the target position is empty and adjacent
        if self.board.check_position(target_row, target_col) != Color.EMPTY:
            return "MoveError -- Target position is not empty"

        if not self.is_adjacent_and_empty(start_row, start_col, target_row, target_col):
            return "MoveError -- Invalid move, pieces can only move to adjacent positions"

        # Perform the move
        self.board.set_position(target_row, target_col, self.turn.name.lower())
        self.board.set_position(start_row, start_col, Color.EMPTY)
        # self.board.board[start_row][start_col] = None
        self.current_moves.append((start_row, start_col))
        self.current_moves.remove((target_row, target_col))
        self.selected_piece = None

        return True

    def get_piece_at(self, row, col):
        return self.board.board[row][col]

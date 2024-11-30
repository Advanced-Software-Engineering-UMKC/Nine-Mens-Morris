# import pygame as pg
from backend.Cell import Cell, Color


class Board:
    def __init__(self, size):
        self.board_size = size
        self.create_initial_board(size)
        self.adjacent_positions_map = {
            # Outer square
            (0, 0): [(0, 3), (3, 0)],
            (0, 3): [(0, 0), (0, 6), (1, 3)],
            (0, 6): [(0, 3), (3, 6)],
            (3, 0): [(0, 0), (3, 1), (6, 0)],
            (3, 6): [(0, 6), (3, 5), (6, 6)],
            (6, 0): [(3, 0), (6, 3)],
            (6, 3): [(6, 0), (6, 6), (5, 3)],
            (6, 6): [(6, 3), (3, 6)],

            # Middle square
            (1, 1): [(1, 3), (3, 1)],
            (1, 3): [(1, 1), (1, 5), (0, 3), (2, 3)],
            (1, 5): [(1, 3), (3, 5)],
            (3, 1): [(1, 1), (5, 1), (3, 0), (3, 2)],
            (3, 5): [(1, 5), (5, 5), (3, 4), (3, 6)],
            (5, 1): [(3, 1), (5, 3)],
            (5, 3): [(5, 1), (5, 5), (6, 3), (4, 3)],
            (5, 5): [(5, 3), (3, 5)],

            # Inner square
            (2, 2): [(2, 3), (3, 2)],
            (2, 3): [(2, 2), (2, 4), (1, 3)],
            (2, 4): [(2, 3), (3, 4)],
            (3, 2): [(2, 2), (4, 2), (3, 1), (3, 3)],
            (3, 4): [(2, 4), (4, 4), (3, 3), (3, 5)],
            (4, 2): [(3, 2), (4, 3)],
            (4, 3): [(4, 2), (4, 4), (5, 3)],
            (4, 4): [(4, 3), (3, 4)]
        }
        self.pieces_on_board = {}

    def create_initial_board(self, size):
        indices_array = []
        for i in range(size):
            horizontal_line = [(i, j) for j in range(size)]
            indices_array.append(horizontal_line)

        # create 2D array of Cell objects
        self.board = [[Cell() for j in range(size)] for i in range(size)]

        # set the state of the cells to EMPTY
        self.valid_moves = []
        self.set_valid_cells_to_empty()
        # print(self.board)

        return self.board

    # def init_valid_moves(self, row):
    #     rowMoves = []
    #     middle = (self.board_size - 1) // 2
    #     if row == middle:
    #         i = 0
    #         while i < self.board_size:
    #             if i != middle:
    #                 rowMoves.append(i)
    #             i += 1
    #     else:
    #         dist = abs(row - middle)
    #         for i in range(3):
    #             offset = (i - 1) * dist
    #             rowMoves.append(offset + middle)
    #     return rowMoves
    
    def init_valid_moves(self, row):
        middle = (self.board_size - 1) // 2
        if row == middle:
            return self._get_middle_row_moves(middle)
        else:
            return self._get_non_middle_row_moves(row, middle)

    def _get_middle_row_moves(self, middle):
        row_moves = []
        for cell in range(self.board_size):
            if cell != middle:
                row_moves.append(cell)
        return row_moves

    # 3 needs to be changed to support any board size
    def _get_non_middle_row_moves(self, row, middle):
        row_moves = []
        dist = abs(row - middle)
        for cell in range(3):
            offset = (cell - 1) * dist
            row_moves.append(offset + middle)
        return row_moves
    
    def set_valid_cells_to_empty(self):
        for index, row in enumerate(self.board):
            valid = self.init_valid_moves(index)
            for cell in valid:
                self.board[index][cell].set_state(Color.EMPTY)
                self.valid_moves.append((index, cell))

    def get_valid_moves(self):
        return self.valid_moves

    def check_position(self, row, column):
        state = self.board[row][column].get_state()
        return state

    def set_position(self, row, column, color):
        if color == "white":
            self.board[row][column].set_state(Color.WHITE)
        elif color == "black":
            self.board[row][column].set_state(Color.BLACK)
        else:
            self.board[row][column].set_state(Color.EMPTY)
        return 1

    def get_cell(self, row, column):
        return self.board[row][column]
    
    def remove_piece(self, row, col):
        # Remove the piece from the internal structure
        if (row, col) in self.pieces_on_board:
            del self.pieces_on_board[(row, col)]

    
    def find_empty_adjacents(self, row, col):
        empty_adjacent_positions = []
        all_adjacent_positions = self.adjacent_positions_map[(row, col)]

        for row, col in all_adjacent_positions:
            position_state = self.check_position(row, col)
            if position_state == Color.EMPTY:
                empty_adjacent_positions.append((row, col))

        return empty_adjacent_positions
    
    def get_movable_options(self, row, col, can_fly):
        # calculate the available adjacent positions
        if can_fly:
            # if can fly, return all open positions
            return self.valid_moves
        else:
            # if more than 3 pieces left, user can only move to empty adjacent positions
            return self.find_empty_adjacents(row, col)

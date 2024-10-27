# import pygame as pg
from backend.Cell import Cell, CellType


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

    # is this valid movement for 6, 9, and 12?
    def init_valid_moves(self, row):
        rowMoves = []
        middle = (self.board_size - 1) // 2
        if row == middle:
            i = 0
            while i < self.board_size:
                if i != middle:
                    rowMoves.append(i)
                i += 1
        else:
            dist = abs(row - middle)
            for i in range(3):
                offset = (i - 1) * dist
                rowMoves.append(offset + middle)
        return rowMoves

    def set_valid_cells_to_empty(self):
        for index, row in enumerate(self.board):
            valid = self.init_valid_moves(index)
            for cell in valid:
                self.board[index][cell].set_state(CellType.EMPTY)
                self.valid_moves.append((index, cell))

    def get_valid_moves(self):
        return self.valid_moves

    def check_position(self, row, column):
        state = self.board[row][column].get_state()
        return state

    def set_position(self, row, column, color):
        if color == "white":
            self.board[row][column].set_state(CellType.WHITE)
        elif color == "black":
            self.board[row][column].set_state(CellType.BLACK)
        else:
            self.board[row][column].set_state(CellType.EMPTY)
        return 1

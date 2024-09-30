import pygame as pg
from backend.Cell import Cell, CellType

class Board:
    def __init__(self, size):
        self.board_size = size
        self.create_initial_board(size)
        
                       
    def create_initial_board(self, size):
        indices_array = []
        for i in range(size):
            horizontal_line = [(i, j) for j in range(size)]
            indices_array.append(horizontal_line)

        # create 2D array of Cell objects
        self.board = [[Cell() for j in range(size)] for i in range(size)]
        
        # set the state of the cells to EMPTY
        self.set_valid_cells_to_empty()
        # print(self.board)

        return self.board
    
    def get_valid_moves(self, row):
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
            validMoves = self.get_valid_moves(index)
            for cell in validMoves:
                self.board[index][cell].setState(CellType.EMPTY)
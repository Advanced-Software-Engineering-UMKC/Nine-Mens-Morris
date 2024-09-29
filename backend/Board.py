import pygame as pg
from backend.Cell import Cell, CellType

class Board:
    def __init__(self, size):
        self.create_initial_board(size)
        
                       
    def create_initial_board(self, size):
        indices_array = []
        for i in range(size):
            horizontal_line = [(i, j) for j in range(size)]
            indices_array.append(horizontal_line)

        # create 2D array of Cell objects
        self.board = [[Cell(i, j) for j in range(size)] for i in range(size)]

        print(self.board)

        return self.board
    
    def get_valid_moves(row):
        rowMoves = []
        middle = len(row - 1) // 2
        if row == middle:
            for cell in row:
                if cell != middle:
                    rowMoves.append(cell)
        else:
            dist = abs(row - middle)
            for i in range(3):
                offset = (i - 1) * dist
                rowMoves.append(offset + middle)
        return rowMoves

    def set_valid_cells_to_empty(self):
        for row in self.board:
            validMoves = self.get_valid_moves(row)
            for cell in validMoves:
                self.board[row][cell].setState(CellType.EMPTY)
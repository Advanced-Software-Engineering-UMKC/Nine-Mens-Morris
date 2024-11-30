# import pygame as pg
from backend.Cell import Cell, Color


class Board:
    def __init__(self, size, piece_count):
        self.board_info = {
            "type": piece_count,
            "size": size,
            "diagonals": True if piece_count == 12 else False,
            "row_size": 2 if piece_count == 6 else 3
        }
        self.create_initial_board(self.board_info["size"])
        self.adjacent_positions_map = self.gen_adj_moves()
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

    # determine the adjacent moves dynamically
    def gen_adj_moves(self):
        pos_map = {}

        # intraconnections for squares (a1-d1-g1, e.g.)
        for offset in range(self.board_info["row_size"], 0, -1):
            ini = self.board_info["row_size"] - offset
            sec = ini + offset
            thi = ini + offset*2

            pos_map[(ini, ini)] = [(ini, sec), (sec, ini)]
            pos_map[(ini, sec)] = [(ini, ini), (ini, thi)]
            pos_map[(ini, thi)] = [(ini, sec), (sec, thi)]

            pos_map[(sec, ini)] = [(ini, ini), (thi, ini)]
            pos_map[(sec, thi)] = [(ini, thi), (thi, thi)]

            pos_map[(thi, ini)] = [(sec, ini), (thi, sec)]
            pos_map[(thi, sec)] = [(thi, ini), (thi, thi)]
            pos_map[(thi, thi)] = [(thi, sec), (sec, thi)]
        
        mid = self.board_info["row_size"]
        
        # "positive" interconnections for squares (a4-b4-c4, e.g.)
        for inter in range(self.board_info["row_size"]-1):
            pos_map[(mid, inter)].append((mid, inter+1))
            pos_map[(mid, inter+1)].append((mid, inter))

            pos_map[(inter, mid)].append((inter+1, mid))
            pos_map[(inter+1, mid)].append((inter, mid))
        
        # "negative" interconnections for squares (g4-f4-e4, e.g.)
        for inter in range(self.board_info["row_size"]-1, 0, -1):
            fin = mid*2 - inter

            pos_map[(mid, fin)].append((mid, fin+1))
            pos_map[(mid, fin+1)].append((mid, fin))

            pos_map[(fin, mid)].append((fin+1, mid))
            pos_map[(fin+1, mid)].append((fin, mid))

        # diagonals
        if self.board_info["diagonals"]:
            for inter in range(self.board_info["row_size"]-1):
                fin = mid*2 - inter

                pos_map[(inter, inter)].append((inter+1, inter+1))
                pos_map[(inter+1, inter+1)].append((inter, inter))

                pos_map[(fin, fin)].append((fin-1, fin-1))
                pos_map[(fin-1, fin-1)].append((fin, fin))

                pos_map[(inter, fin)].append((inter+1, fin-1))
                pos_map[(inter+1, fin-1)].append((inter, fin))

                pos_map[(fin, inter)].append((fin-1, inter+1))
                pos_map[(fin-1, inter+1)].append((fin, inter))

        return pos_map
    
    def init_valid_moves(self, row):
        middle = (self.board_info["size"] - 1) // 2
        if row == middle:
            return self._get_middle_row_moves(middle)
        else:
            return self._get_non_middle_row_moves(row, middle)

    def _get_middle_row_moves(self, middle):
        row_moves = []
        for cell in range(self.board_info["size"]):
            if cell != middle:
                row_moves.append(cell)
        return row_moves

    '''hmm, so the "magic number" 3 here represents the number valid spots in a row. 
    that actually doesn't change depending on the board, except in the middle on 6, 
    but the middle works fine and is in a separate function
    
    we can change this if you guys are concerned about it, but it's the same no matter the men's morris game. even 3 works this way'''
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

import pygame as pg
from backend.Board import Board

vec2 = pg.math.Vector2

class BoardGUI:
    def __init__(self, game, WIN_SIZE, board_size):
        self.game = game
        self.board_image = self.get_scaled_image('resources/board/board.png', [WIN_SIZE] * 2)
        self.cell_size = WIN_SIZE // board_size
        self.black_piece_image = self.get_scaled_image('resources/pieces/black_piece.png', [self.cell_size] * 2)
        self.white_piece_image = self.get_scaled_image('resources/pieces/white_piece.png', [self.cell_size] * 2)
        self.board = Board(board_size)
        

    def draw_board(self):
        self.game.screen.blit(self.board_image, (0, 0))

    @staticmethod
    def get_scaled_image(path, resolution):
        image = pg.image.load(path)
        return pg.transform.smoothscale(image.convert_alpha(), resolution)
    
    def build_board(self):
        self.draw_board()

    def draw_piece(self, piece, position):
        if piece == 'black':
            self.game.screen.blit(self.black_piece_image, position)
        else:
            self.game.screen.blit(self.white_piece_image, position)

    def getCellClicked(self):
        current_cell = vec2(pg.mouse.get_pos()) // self.cell_size
        col, row = map(int, current_cell)
        left_click = pg.mouse.get_pressed()[0]
        if left_click and self.
        print(left_click)
        # mouse_pos = pg.mouse.get_pos()
        # col, row = mouse_pos[0] // self.cell_size, mouse_pos[1] // self.cell_size
        # print(col, row)
        return current_cell
        # return col, row

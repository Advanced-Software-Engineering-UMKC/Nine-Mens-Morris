import pygame as pg
from backend.Board import Board
from backend.GameManager import GameManager
# import backend.Cell as CellType

vec2 = pg.math.Vector2

class BoardGUI:
    def __init__(self, game, WIN_SIZE, board_size, total_pieces, gameManager):
        self.game = game
        self.board_image = self.get_scaled_image('resources/board/board.png', [WIN_SIZE] * 2)
        self.cell_size = WIN_SIZE // board_size
        self.black_piece_image = self.get_scaled_image('resources/pieces/black_piece.png', [self.cell_size] * 2)
        self.white_piece_image = self.get_scaled_image('resources/pieces/white_piece.png', [self.cell_size] * 2)
        self.game_manager = gameManager
        self.board = Board(board_size)
        self.count = 0
        self.win_size = WIN_SIZE


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

    def get_cell_clicked(self):
        current_cell = vec2(pg.mouse.get_pos()) // self.cell_size
        col, row = map(int, current_cell)
        mouse_buttons = pg.mouse.get_pressed()  # Call this once and store the result

        if mouse_buttons[0]:  # Left click
            self.count += 1
            if not self.game_manager.placement_complete():
                isPiecePlaced = self.game_manager.place_piece(row, col)
                if isPiecePlaced == 1:
                    self.draw_piece(self.game_manager.get_turn(), current_cell * self.cell_size)
                    self.game_manager.end_turn()
            return current_cell  # Return the current cell for left click

        if mouse_buttons[2]:  # Right click
            return None  # Return None on right click

        return None  # Return None if no click


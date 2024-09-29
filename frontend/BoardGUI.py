import pygame as pg

class BoardGUI:
    def __init__(self, game, WIN_SIZE):
        self.game = game
        self.board_image = self.get_scaled_image('resources/board.png', [WIN_SIZE] * 2)

    def draw_board(self):
        self.game.screen.blit(self.board_image, (0, 0))

    @staticmethod
    def get_scaled_image(path, resolution):
        image = pg.image.load(path)
        return pg.transform.smoothscale(image.convert_alpha(), resolution)
    
    def build_board(self):
        self.draw_board()


import pygame as pg
import sys
from BoardGUI import BoardGUI 

WIN_SIZE = 900

class GameGUI:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([WIN_SIZE] * 2)
        self.clock = pg.time.Clock()
        # window title
        pg.display.set_caption('Nine-Mens-Morris')
        self.board = BoardGUI(self, WIN_SIZE)

    def check_events(self):
        # check for exit event and properly exit game
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def run_game(self):
        while True:
            self.check_events()
            pg.display.update()
            self.clock.tick(60)
            self.board.build_board()
        
if __name__ == '__main__':
    game = GameGUI()
    game.run_game()
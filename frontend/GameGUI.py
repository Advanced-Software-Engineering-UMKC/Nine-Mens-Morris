import pygame as pg
import sys
from frontend.BoardGUI import BoardGUI 

WIN_SIZE = 500

class GameGUI:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([WIN_SIZE] * 2)
        self.clock = pg.time.Clock()
        # window title
        pg.display.set_caption('Nine-Mens-Morris')
        self.board_size = 7
        self.total_pieces = 9
        self.board = BoardGUI(self, WIN_SIZE, self.board_size, self.total_pieces)
        

    def check_events(self):
        # check for exit event and properly exit game
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def run_game(self):
        self.board.build_board()
    
        while True:
            self.check_events()
            pg.display.update()
            self.clock.tick(60)
            self.board.get_cell_clicked() #this runs too much. reduce or face errors

def main():
    game = GameGUI()
    game.run_game()
        
if __name__ == '__main__':
    main()
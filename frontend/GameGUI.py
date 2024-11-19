import sys
import pygame as pg
from backend.GameManager import GameManager
from frontend.BoardGUI import BoardGUI

WIN_SIZE = 500

class GameGUI:
    def __init__(self):
        pg.init()
        self.info_height = 100
        self.screen = pg.display.set_mode((WIN_SIZE, WIN_SIZE + self.info_height))
        self.clock = pg.time.Clock()
        # window title
        pg.display.set_caption("Nine-Mens-Morris")
        self.board_size = 7
        self.total_pieces = 9
        self.gameManager = GameManager(self.board_size, self.total_pieces)
        self.board = BoardGUI(
            self, WIN_SIZE, self.board_size, self.total_pieces, self.gameManager
        )

    def check_events(self):
        # check for exit event and properly exit game
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # Check for mouse click events
            elif event.type == pg.MOUSEBUTTONDOWN:
                # Only run get_cell_clicked when a mouse button is clicked
                self.board.get_cell_clicked()

    def run_game(self):
        self.board.build_board()

        while True:
            self.check_events()
            self.draw_info()
            pg.display.update()
            self.clock.tick(60)

    def draw_info(self):
        font = pg.font.Font(None, 36)
        turn_text = font.render(
            f"Turn: {self.gameManager.turn.name}", True, (255, 255, 255)
        )
        white_pieces_text = font.render(
            f"White Pieces Left: {self.gameManager.get_pieces_left()['white']}", 
            True,
            (255, 255, 255),
        )
        black_pieces_text = font.render(
            f"Black Pieces Left: {self.gameManager.get_pieces_left()['black']}",
            True,
            (255, 255, 255),
        )

        # Clear the info area
        pg.draw.rect(self.screen, (0, 0, 0), (0, WIN_SIZE, WIN_SIZE, self.info_height))

        # Draw the text
        self.screen.blit(turn_text, (10, WIN_SIZE + 10))
        self.screen.blit(white_pieces_text, (200, WIN_SIZE + 10))
        self.screen.blit(black_pieces_text, (200, WIN_SIZE + 40))


def main():
    game = GameGUI()
    game.run_game()


if __name__ == "__main__":
    main()

import sys
import pygame as pg
from backend.GameManager import GameManager
from frontend.BoardGUI import BoardGUI
from backend.Piece import Color

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

    def start_screen(self):
        font = pg.font.Font(None, 34)
        title_font = pg.font.Font(None, 48)
        title_text = title_font.render("Nine Mens Morris", True, (255, 255, 255))
        human_text = font.render("Press 1 for Human", True, (255, 255, 255))
        computer_text = font.render("Press 2 for Computer", True, (255, 255, 255))

        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(title_text, (50, 50))
            self.screen.blit(human_text, (50, 250))
            self.screen.blit(computer_text, (50, 350))
            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        self.use_computer_opponent = False
                        return
                    elif event.key == pg.K_2:
                        self.use_computer_opponent = True
                        self.gameManager.set_use_computer_opponent(self.use_computer_opponent)
                        return

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
        self.start_screen()
        self.board.build_board()

        while True:
            self.check_events()
            self.draw_info()
            pg.display.update()
            self.clock.tick(60)
            if self.use_computer_opponent and self.gameManager.turn == Color.BLACK:
                self.board.handle_computer_move()

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

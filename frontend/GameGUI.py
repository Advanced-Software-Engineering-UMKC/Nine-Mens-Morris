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

    def finish_init(self, size, pieces):
        cap = "-Mens-Morris"
        if pieces == 6:
            cap = "Six" + cap
        elif pieces == 9:
            cap = "Nine" + cap
        else:
            cap = "Twelve" + cap
        pg.display.set_caption(cap)
        self.board_size = size
        self.total_pieces = pieces
        self.game_manager = GameManager(self.board_size, self.total_pieces)
        self.board_gui = BoardGUI(self, WIN_SIZE, self.board_size, self.game_manager)

    def game_picker_screen(self):
        title_text = self.font.render("Pick a Men's Morris game", True, (255, 255, 255))
        six_text = self.font.render("Press 1 for Six", True, (255, 255, 255))
        nine_text = self.font.render("Press 2 for Nine", True, (255, 255, 255))
        twelve_text = self.font.render("Press 3 for Twelve", True, (255, 255, 255))

        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(title_text, (50, 50))
            self.screen.blit(six_text, (50, 250))
            self.screen.blit(nine_text, (50, 350))
            self.screen.blit(twelve_text, (50, 450))
            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        self.finish_init(5, 6)
                        return
                    elif event.key == pg.K_2:
                        self.finish_init(7, 9)
                        return
                    elif event.key == pg.K_3:
                        self.finish_init(7, 12)
                        return

    def start_screen(self):
        self.font = pg.font.Font(None, 34)
        self.title_font = pg.font.Font(None, 48)
        title_text = self.title_font.render("Nine Mens Morris", True, (255, 255, 255))
        human_text = self.font.render("Press 1 for Human", True, (255, 255, 255))
        computer_text = self.font.render("Press 2 for Computer", True, (255, 255, 255))

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
                        self.game_manager.set_use_computer_opponent(self.use_computer_opponent)
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
                self.board_gui.get_cell_clicked()

    def run_game(self):
        self.start_screen()
        self.game_picker_screen()
        self.board_gui.build_board()

        while True:
            self.check_events()
            self.draw_info()
            pg.display.update()
            self.clock.tick(60)
            if self.use_computer_opponent and self.game_manager.turn == Color.BLACK:
                self.board_gui.handle_computer_move()
                pg.display.update()


    def draw_info(self):
        font = pg.font.Font(None, 36)
        turn_text = font.render(
            f"Turn: {self.game_manager.turn.name}", True, (255, 255, 255)
        )
        white_pieces_text = font.render(
            f"White Pieces Left: {self.game_manager.get_pieces_left()['white']}", 
            True,
            (255, 255, 255),
        )
        black_pieces_text = font.render(
            f"Black Pieces Left: {self.game_manager.get_pieces_left()['black']}",
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

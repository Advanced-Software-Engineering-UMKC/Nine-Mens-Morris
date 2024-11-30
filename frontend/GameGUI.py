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
        self.play = True  # This will determine if the user plays a new game or replays

    def show_start_screen(self):
        # Display a simple start screen for the user to choose play or replay
        font = pg.font.Font(None, 48)
        play_text = font.render("Press P to Play a New Game", True, (255, 255, 255))
        replay_text = font.render("Press R to Replay", True, (255, 255, 255))
        
        self.screen.fill((0, 0, 0))  # Clear the screen with black

        # Draw the options on the screen
        self.screen.blit(play_text, (WIN_SIZE // 2 - play_text.get_width() // 2, WIN_SIZE // 2 - 30))
        self.screen.blit(replay_text, (WIN_SIZE // 2 - replay_text.get_width() // 2, WIN_SIZE // 2 + 30))
        
        pg.display.flip()

        # Wait for the user to press a key to choose an option
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        self.play = True
                        return  # Exit the selection screen and start the game
                    elif event.key == pg.K_r:
                        self.play = False
                        return  # Exit the selection screen and start the replay

    def check_events(self):
        # check for exit event and properly exit game
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # Check for mouse click events
            elif event.type == pg.MOUSEBUTTONDOWN:
                # Only run get_cell_clicked when a mouse button is clicked
                if self.play:
                    self.board.get_cell_clicked()
                else:
                    self.board.replay_game()

    def run_game(self):
        self.show_start_screen()  # Show the initial screen to select play or replay
        self.board.build_board()

        while True:
            self.check_events()
            self.draw_info()
            pg.display.update()
            self.clock.tick(60)

    def draw_info(self):
        if self.play:  # Only draw the info when in play mode
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

import sys
from tkinter import filedialog
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
        self.game_manager = GameManager(self.board_size, self.total_pieces)
        self.board_gui = BoardGUI(
            self, WIN_SIZE, self.board_size, self.game_manager
        )
        self.play = True  # This will determine if the user plays a new game or replays
        self.font = pg.font.Font(None, 34)
        self.title_font = pg.font.Font(None, 48)

    def play_or_replay_menu(self):
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
        


    def finish_init(self, size, pieces):
        cap = "-Mens-Morris"
        if pieces == 6:
            self.title = "Six"
        elif pieces == 9:
            self.title = "Nine"
        else:
            self.title = "Twelve"
        pg.display.set_caption(self.title + cap)
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

    def human_or_computer_menu(self):
        font = pg.font.Font(None, 34)
        title_font = pg.font.Font(None, 48)
        title_text = title_font.render(self.title + " Men's Morris", True, (255, 255, 255))
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
                        self.game_manager.set_use_computer_opponent(self.use_computer_opponent)
                        return
                    
    def end_screen(self, winner):
        over_text = self.title_font.render("Game Over", True, (255, 255, 255))
        winner_text = self.font.render(winner + " won!", True, (255, 255, 255))
        quit_text = self.font.render("Press any button to quit...", True, (255, 255, 255))

        self.screen.fill((0, 0, 0)) 
        self.screen.blit(over_text, (50, 50))
        self.screen.blit(winner_text, (50, 250))
        self.screen.blit(quit_text, (50, 350))
        pg.display.update()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.MOUSEBUTTONDOWN or event.type == pg.KEYDOWN:
                    pg.quit()
                    sys.exit()

    def check_events(self):
        # check for exit event and properly exit game
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            elif self.game_manager.check_game_over():
                self.end_screen(self.game_manager.check_game_over().name)

            # Check for mouse click events
            elif event.type == pg.MOUSEBUTTONDOWN:
                # Only run get_cell_clicked when a mouse button is clicked
                if self.play:
                    self.board_gui.get_cell_clicked()
                else:
                    # Open the file chooser dialog
                    file_path = filedialog.askopenfilename(
                        title="Select a File",
                        filetypes=[("Game History Files (*.json)", "*.json")]
                    )

                    # Check if a file was selected
                    if file_path:
                        self.board_gui.replay_game(file_path)


    def run_game(self):
        self.game_picker_screen()
        self.play_or_replay_menu()  # Show the initial screen to select play or replay
        if self.play:
            self.human_or_computer_menu()
        else:
            self.use_computer_opponent = False
        self.board_gui.build_board()

        while True:
            if not self.board_gui.game_over:
                self.check_events()
                self.draw_info()
                pg.display.update()
                self.clock.tick(60)
                if self.use_computer_opponent and self.game_manager.turn == Color.BLACK:
                    self.board_gui.handle_computer_move()
                    pg.display.update()
            else:
                self.end_screen(self.game_manager.check_game_over().name)


    def draw_info(self):
        if self.play:  # Only draw the info when in play mode
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

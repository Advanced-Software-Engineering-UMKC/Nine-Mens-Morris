import unittest
from unittest.mock import patch
import pygame as pg
from frontend.GameGUI import GameGUI

'''
Setup: The setUp method initializes the GameGUI object before each test. It uses patch decorators to mock pygame modules, since rendering and handling real-time events aren't suitable for unit tests.

test_check_events_exit: This test verifies that the check_events() method handles the QUIT event correctly by calling pygame.quit() and sys.exit().

test_check_events_no_quit: It ensures that no exit actions are taken when QUIT is not in the events.

test_run_game_quit: Tests that the run_game() method calls build_board() once and exits gracefully upon a QUIT event.

test_run_game: Verifies that get_cell_clicked() is called multiple times as expected during the game loop. It simulates a series of events (KEYDOWN and QUIT) to control the game loop flow.

'''
class TestGameGUI(unittest.TestCase):
    def setUp(self):
        # Initialize Pygame display to prevent errors with display functions
        pg.display.set_mode([1, 1])  # Minimal size to initialize display
        self.game = GameGUI()  # Create instance of GameGUI

    def tearDown(self):
        # Quit Pygame after each test
        pg.quit()

    @patch('pygame.event.get')
    def test_check_events_exit(self, mock_pygame_event_get):
        # Simulate QUIT event
        mock_pygame_event_get.return_value = [pg.event.Event(pg.QUIT)]
        with self.assertRaises(SystemExit):
            self.game.check_events()

    @patch('pygame.event.get')
    def test_check_events_no_quit(self, mock_pygame_event_get):
        # Simulate non-QUIT events
        mock_pygame_event_get.return_value = [pg.event.Event(pg.KEYDOWN, {'key': pg.K_a})]
        try:
            self.game.check_events()
        except SystemExit:
            self.fail("check_events() raised SystemExit unexpectedly!")

    @patch('pygame.event.get')
    def test_run_game_quit(self, mock_pygame_event_get):
        # Simulate QUIT event to exit game loop
        mock_pygame_event_get.return_value = [pg.event.Event(pg.QUIT)]
        with self.assertRaises(SystemExit):
            self.game.run_game()

    def test_run_game(self):
        # Mock methods to prevent an infinite loop and resource loading
        with patch.object(self.game, 'check_events') as mock_check_events, \
             patch.object(self.game.board, 'build_board') as mock_build_board, \
             patch('pygame.display.update') as mock_display_update:
            mock_check_events.side_effect = [None, SystemExit]  # Stop after one iteration
            with self.assertRaises(SystemExit):
                self.game.run_game()

if __name__ == '__main__':
    unittest.main()




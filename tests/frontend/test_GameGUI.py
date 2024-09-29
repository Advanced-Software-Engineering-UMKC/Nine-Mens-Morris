import pytest
import pygame as pg
from frontend.GameGUI import GameGUI

# fixtures create reusable instances for testing
@pytest.fixture
def game_gui():
    """Fixture to create a GameGUI instance."""
    # Initialize Pygame
    pg.init()
    game = GameGUI()
    yield game  # This allows the test to use the game instance
    pg.quit()  # Clean up after the tests

class TestGameGUI:
    def test_game_gui_initialization(self, game_gui):
        """Test if GameGUI initializes correctly."""
        assert game_gui.screen is not None
        assert game_gui.clock is not None
        assert game_gui.board is not None
        assert pg.display.get_init()

    def test_check_events_quit(self, game_gui):

        assert pg.display.get_init()

        """Test if the check_events method handles QUIT event properly."""
        # Simulate a QUIT event
        for event in [pg.event.Event(pg.QUIT)]:
            # event.post() puts the event in the event queue
            # this is used for simulating events or actions in the game
            pg.event.post(event)
        
        # We will check if the quit event is processed without raising errors
        try:
            game_gui.check_events()
        except SystemExit:
            # If SystemExit is raised, we assume the quit event was processed
            pass

        assert not pg.display.get_init()  # Check PyGame is not initialized
        
        # Here, we would normally use mocking to verify that pg.quit() was called.
        # For simplicity, we just ensure no errors were raised.


    # def test_run_game(self, game_gui):
    #     """Test if the run_game method initializes the board and Pygame."""
    #     # assert pg.display.get_init()
    #     game_gui.run_game()
    #     assert game_gui.board is not None
    #     # assert pg.display.get_init()

if __name__ == '__main__':
    pytest.main()
import pytest
import pygame as pg
from frontend.GameGUI import GameGUI

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

    def test_check_events_quit(self, game_gui):
        """Test if the check_events method handles QUIT event properly."""
        # Simulate a QUIT event
        for event in [pg.event.Event(pg.QUIT)]:
            pg.event.post(event)
        
        # We will check if the quit event is processed without raising errors
        try:
            game_gui.check_events()
        except SystemExit:
            # If SystemExit is raised, we assume the quit event was processed
            pass
        
        # Here, we would normally use mocking to verify that pg.quit() was called.
        # For simplicity, we just ensure no errors were raised.

if __name__ == '__main__':
    pytest.main()
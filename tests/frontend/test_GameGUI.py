from unittest.mock import patch, MagicMock
import pygame as pg
import pytest
from frontend.GameGUI import GameGUI

@pytest.fixture(scope="function")
def game_fixture():
    pg.init()
    pg.display.set_mode((640, 480))
    game = GameGUI()
    game.board_gui = MagicMock()
    game.board_gui.build_board = MagicMock()
    
    yield game
    pg.quit()

@pytest.mark.usefixtures("game_fixture")
class TestGameGUI:
    """Test suite for the GameGUI class."""

    def test_check_events_exit(self, game_fixture):
        game = game_fixture
        with patch("pygame.event.get") as mock_pygame_event_get:
            mock_pygame_event_get.return_value = [pg.event.Event(pg.QUIT)]
            with pytest.raises(SystemExit):
                game.check_events()

    def test_check_events_no_quit(self, game_fixture):
        game = game_fixture
        with patch("pygame.event.get") as mock_pygame_event_get:
            mock_pygame_event_get.return_value = [
                pg.event.Event(pg.KEYDOWN, {"key": pg.K_a})
            ]
            try:
                game.check_events()
            except SystemExit:
                pytest.fail("check_events() raised SystemExit unexpectedly!")

    def test_run_game_quit(self, game_fixture):
        game = game_fixture
        with patch("pygame.event.get") as mock_pygame_event_get:
            mock_pygame_event_get.return_value = [pg.event.Event(pg.QUIT)]
            with pytest.raises(SystemExit):
                game.run_game()

    def test_run_game(self, game_fixture):
        game = game_fixture
        with patch.object(game, "check_events") as mock_check_events, patch.object(
            game.board, "build_board"
        ) as mock_build_board, patch("pygame.display.update") as mock_display_update:
            mock_check_events.side_effect = [None, SystemExit]  # Stop after one iteration
            with pytest.raises(SystemExit):
                game.run_game()

import pytest
from unittest.mock import patch
import pygame as pg
from frontend.GameGUI import GameGUI


@pytest.fixture(scope='function')
def game_fixture():
    """Fixture to initialize and clean up the GameGUI instance for each test."""
    # Initialize Pygame display to prevent errors with display functions
    pg.display.set_mode([1, 1])  # Minimal size to initialize display
    game = GameGUI()  # Create instance of GameGUI
    yield game  # Provide the game instance to the test
    pg.quit()  # Quit Pygame after each test


def test_check_events_exit(game_fixture):
    game = game_fixture

    # Patch the pygame event to simulate a QUIT event
    with patch('pygame.event.get') as mock_pygame_event_get:
        mock_pygame_event_get.return_value = [pg.event.Event(pg.QUIT)]
        with pytest.raises(SystemExit):
            game.check_events()


def test_check_events_no_quit(game_fixture):
    game = game_fixture

    # Patch the pygame event to simulate a non-QUIT event
    with patch('pygame.event.get') as mock_pygame_event_get:
        mock_pygame_event_get.return_value = [pg.event.Event(pg.KEYDOWN, {'key': pg.K_a})]
        try:
            game.check_events()
        except SystemExit:
            pytest.fail("check_events() raised SystemExit unexpectedly!")


def test_run_game_quit(game_fixture):
    game = game_fixture

    # Patch the pygame event to simulate a QUIT event
    with patch('pygame.event.get') as mock_pygame_event_get:
        mock_pygame_event_get.return_value = [pg.event.Event(pg.QUIT)]
        with pytest.raises(SystemExit):
            game.run_game()


def test_run_game(game_fixture):
    game = game_fixture

    # Mock methods to prevent an infinite loop and resource loading
    with patch.object(game, 'check_events') as mock_check_events, \
         patch.object(game.board, 'build_board') as mock_build_board, \
         patch('pygame.display.update') as mock_display_update:
        mock_check_events.side_effect = [None, SystemExit]  # Stop after one iteration
        with pytest.raises(SystemExit):
            game.run_game()

import os
import pytest

from backend.Cell import Color
from backend.GameManager import GameManager, history_path

@pytest.fixture
def setup_board():
    # Given the game is Nine Men’s Morris
    board_size = 7
    total_pieces = 4
    game_manager = GameManager(board_size, total_pieces)

    board = game_manager.get_board()
    return game_manager

class TestGameReplay:
    def test_valid_game_replay_file_load(self, setup_board):
        game_manager = setup_board
        history = game_manager.load_history(history_path + 'game_history.json')
        assert history is not None
        is_valid, msg = game_manager.validate_history_data(history)
        assert is_valid

    def test_invalid_game_replay_file_load_1(self, setup_board):
        game_manager = setup_board
        history = game_manager.load_history(history_path + 'gh.json')
        assert history is None

    def test_invalid_game_replay_file_load_2(self, setup_board):
        game_manager = setup_board
        history = game_manager.load_history(history_path + 'game_history_invalid.json')
        assert history is not None
        is_valid, msg = game_manager.validate_history_data(history)
        assert not is_valid

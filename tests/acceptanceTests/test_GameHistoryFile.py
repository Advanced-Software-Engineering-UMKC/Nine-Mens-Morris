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

class TestGameHistoryFile:
    def test_game_history_file_creation(self, setup_board):
        # Given an ongoing game with a complete piece placement phase
        game_manager = setup_board
        game_manager.place_piece(0,0)
        game_manager.place_piece(3,0)
        game_manager.place_piece(0,3)
        game_manager.place_piece(1,1)
        game_manager.end_turn()
        game_manager.place_piece(1,3)
        game_manager.place_piece(3,1)
        game_manager.place_piece(6,0)
        game_manager.place_piece(0,6)
        game_manager.end_turn()

        # history file yet not created
        file_path = history_path + 'game_history_' + game_manager.id + '.json'
        assert not os.path.exists(file_path)

        # Then the game is over
        result = game_manager.check_game_over()

        # And the black piece player has won
        assert result == Color.BLACK

        # history file should exist now
        assert os.path.exists(file_path)

        # deleting history file
        game_manager.delete_history_file(history_path)
        assert not os.path.exists(file_path)

    def test_no_history_file_for_incomplete_game(self, setup_board):
        # Given an ongoing game with a complete piece placement phase
        game_manager = setup_board
        game_manager.place_piece(0,0)
        game_manager.place_piece(3,0)
        game_manager.place_piece(0,3)
        game_manager.place_piece(1,1)
        game_manager.end_turn()
        game_manager.place_piece(1,3)
        game_manager.place_piece(3,1)
        game_manager.place_piece(6,0)
        game_manager.place_piece(0,6)
        game_manager.end_turn()

        # history file yet not created
        file_path = history_path + 'game_history_' + game_manager.id + '.json'
        assert not os.path.exists(file_path)

import pytest

from backend.Cell import Color
from backend.GameManager import GameManager


@pytest.fixture
def setup_board():
    # Given the game is Nine Men’s Morris
    board_size = 7
    total_pieces = 9
    game_manager = GameManager(board_size, total_pieces)
    game_manager.set_use_computer_opponent(True)

    return game_manager


class TestTurnSwitching:
    def test_new_game_start_human(self, setup_board):
        # Given a new game is started
        game_manager = setup_board

        # When a new game is started
        # Then the turn is set to the human
        assert game_manager.get_turn() == Color.WHITE
        assert game_manager.player_1.color == Color.WHITE

    def test_human_switch_computer(self, setup_board):
        # Given an ongoing game on the human's turn
        game_manager = setup_board

        # When a human piece is placed on an empty cell
        game_manager.place_piece(0, 0)
        game_manager.end_turn()

        # Then the turn is the computer's
        assert game_manager.get_turn() == Color.BLACK
        assert game_manager.player_2.color == Color.BLACK

    def test_computer_switch_human(self, setup_board):
        # Given an ongoing game on the computer's turn
        game_manager = setup_board
        game_manager.end_turn()

        # When te computer opponent finishes its turn
        game_manager.handle_computer_turn()

        # Then the turn is the human's
        assert game_manager.get_turn() == Color.WHITE
        assert game_manager.player_1.color == Color.WHITE

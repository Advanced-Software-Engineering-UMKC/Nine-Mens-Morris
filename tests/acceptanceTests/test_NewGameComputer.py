import pytest

from backend.Cell import Color
from backend.GameManager import GameManager


@pytest.fixture
def setup_board():
    # Given the game is Nine Men’s Morris
    board_size = 7
    total_pieces = 9
    game_manager = GameManager(board_size, total_pieces)

    return game_manager


class TestNewGameComputer:
    def test_empty_board_computer(self, setup_board):
        # When a new game is started
        game_manager = setup_board
        # When the player wants to play against a computer opponent
        game_manager.set_use_computer_opponent(True)
        
        # The opponent is controlled by the computer
        assert game_manager.use_computer_opponent == True
        game_manager.end_turn()
        game_manager.handle_computer_turn()
        assert game_manager.player_2.get_placed_pieces_position() != []

    def test_empty_board_human(self, setup_board):
        # When a new game is started
        game_manager = setup_board
        # When the player wants to play against a computer opponent
        game_manager.set_use_computer_opponent(False)

        
        # The opponent is not controlled by the computer
        assert game_manager.use_computer_opponent == False

if __name__ == "__main__":
    pytest.main()

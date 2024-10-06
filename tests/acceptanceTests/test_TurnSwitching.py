import pytest
from backend.Board import Board
from backend.GameManager import GameManager
from backend.Cell import CellType
from backend.Piece import Turn 


@pytest.fixture
def setup_board():
    # Given the game is Nine Men’s Morris
    board_size = 7
    total_pieces = 9
    game_manager = GameManager(board_size, total_pieces)
    
    # When a new game is started
    board_class_instance = game_manager.get_board()
    return board_class_instance, board_size, game_manager

class TestTurnSwitching:
    # Scenario: New Game Starts with White Turn
    def test_new_game_starts_with_white_turn(self, setup_board):
        # Given the game is Nine Men’s Morris
        board_class_instance, board_size, game_manager = setup_board

        # When a new game is started
        # Then the turn is white
        assert game_manager.get_turn() == Turn.WHITE
    
    # Scenario: White Turn Switches to Black
    def test_white_turn_switches_to_black(self, setup_board):
        # Given the game is Nine Men’s Morris
        board_class_instance, board_size, game_manager = setup_board

        # When a white piece is placed on an empty cell
        game_manager.place_piece(0, 0)
        game_manager.end_turn()

        # Then the turn is black
        assert game_manager.get_turn() == Turn.BLACK
    
    # Scenario: Black Turn Switches to White
    def test_black_turn_switches_to_white(self, setup_board):
        # Given the game is Nine Men’s Morris
        board_class_instance, board_size, game_manager = setup_board

        # When a white piece is placed on an empty cell
        game_manager.place_piece(0, 0)
        game_manager.end_turn()
        game_manager.place_piece(1, 1)
        game_manager.end_turn()

        # Then the turn is white
        assert game_manager.get_turn() == Turn.WHITE
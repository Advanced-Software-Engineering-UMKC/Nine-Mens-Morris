import pytest

from backend.Cell import Color
from backend.GameManager import GameManager

@pytest.fixture
def setup_board():
    # Given the game is Nine Men’s Morris
    board_size = 7
    total_pieces = 3
    game_manager = GameManager(board_size, total_pieces)
    game_manager.set_use_computer_opponent(True)

    # Complete the piece placement phase
    game_manager.place_piece(0,0) #w
    game_manager.place_piece(6,0) #w
    game_manager.place_piece(6,3) #w
    game_manager.end_turn()
    game_manager.place_piece(6,6) #b
    game_manager.place_piece(0,6) #b
    game_manager.place_piece(5,5) #b
    board = game_manager.get_board()
    return game_manager

class TestPieceFlight:
    def test_flight_computer(self, setup_board):
        # Given an ongoing game on computer's turn
        game_manager = setup_board
        assert game_manager.get_piece_at(0,0).get_state() == Color.WHITE
        assert game_manager.get_piece_at(2,2).get_state() == Color.EMPTY
        assert game_manager.get_turn() == Color.BLACK

        # And computer has exactly 3 pieces remaining
        assert len(game_manager.player_2.pieces) == 3

        # When a piece is moved to an empty cell
        game_manager.select_piece(6,6)
        game_manager.move_piece(2,2)
        game_manager.end_turn()

        # Then the piece is moved to the cell
        assert game_manager.get_piece_at(6,6).get_state() == Color.EMPTY
        assert game_manager.get_piece_at(2,2).get_state() == Color.BLACK
        
        # And the turn is changed to human
        assert game_manager.get_turn() == Color.WHITE

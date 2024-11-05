import pytest

from backend.Cell import Color
from backend.GameManager import GameManager

@pytest.fixture
def setup_board():
    # Given the game is Nine Men’s Morris
    board_size = 7
    total_pieces = 3
    game_manager = GameManager(board_size, total_pieces)

    # Complete the piece placement phase
    game_manager.place_piece(0,0) #w
    game_manager.place_piece(6,0) #w
    game_manager.place_piece(6,3) #w
    game_manager.end_turn()
    game_manager.place_piece(6,6) #b
    game_manager.place_piece(0,6) #b
    game_manager.place_piece(5,5) #b
    game_manager.end_turn()
    board = game_manager.get_board()
    return game_manager

class TestPieceFlight:
    def test_white_piece_flight(self, setup_board):
        # Given an ongoing game on white's turn
        game_manager = setup_board
        assert game_manager.get_piece_at(0,0).get_state() == Color.WHITE
        assert game_manager.get_piece_at(2,2).get_state() == Color.EMPTY
        assert game_manager.get_turn() == Color.WHITE

        # And white has exactly 3 pieces remaining
        # ...

        # When a white piece is moved to an empty cell
        game_manager.select_piece(0,0)
        game_manager.move_piece(2,2)
        game_manager.end_turn()

        # Then the piece is moved to the cell
        assert game_manager.get_piece_at(0,0).get_state() == Color.EMPTY
        assert game_manager.get_piece_at(2,2).get_state() == Color.WHITE
        
        # And the turn is changed to black
        assert game_manager.get_turn() == Color.BLACK

    
    def test_black_piece_flight(self, setup_board):
        # Given an ongoing game on black's turn
        game_manager = setup_board
        game_manager.end_turn()
        assert game_manager.get_piece_at(6,6).get_state() == Color.BLACK
        assert game_manager.get_piece_at(2,2).get_state() == Color.EMPTY
        assert game_manager.get_turn() == Color.BLACK

        # And black has exactly 3 pieces remaining
        # ...

        # When a black piece is moved to an empty cell
        game_manager.select_piece(6,6)
        game_manager.move_piece(2,2)
        game_manager.end_turn()

        # Then the piece is moved to the cell
        assert game_manager.get_piece_at(6,6).get_state() == Color.EMPTY
        assert game_manager.get_piece_at(2,2).get_state() == Color.BLACK
        
        # And the turn is changed to white
        assert game_manager.get_turn() == Color.WHITE
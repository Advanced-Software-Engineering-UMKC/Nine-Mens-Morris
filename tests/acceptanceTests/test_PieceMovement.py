import pytest

from backend.Cell import Color
from backend.GameManager import GameManager

@pytest.fixture
def setup_board():
    # Given the game is Nine Men’s Morris
    board_size = 7
    total_pieces = 4
    game_manager = GameManager(board_size, total_pieces)

    # Complete the piece placement phase
    game_manager.place_piece(0,0) #w
    game_manager.place_piece(6,0) #w
    game_manager.place_piece(6,3) #w
    game_manager.place_piece(5,1) #w
    game_manager.end_turn()
    game_manager.place_piece(6,6) #b
    game_manager.place_piece(0,6) #b
    game_manager.place_piece(5,5) #b
    game_manager.place_piece(0,3) #b
    game_manager.end_turn()
    board = game_manager.get_board()
    return game_manager

class TestPieceMovement:
    def test_move_white_piece_empty_cell(self, setup_board):
        # Given an ongoing game
        game_manager = setup_board
        assert game_manager.get_piece_at(0,0).get_state() == Color.WHITE
        assert game_manager.get_turn() == Color.WHITE

        # And that there are 4+ white pieces remaining
        assert game_manager.pieces.count_white_remains > 3

        # When the white piece player moves a white piece to an empty and adjacent cell
        game_manager.select_piece(0,0)
        game_manager.move_piece(3,0)
        game_manager.end_turn()

        # Then the piece is placed in the cell
        assert game_manager.get_piece_at(0,0).get_state() == Color.EMPTY
        assert game_manager.get_piece_at(3,0).get_state() == Color.WHITE

        # And the turn is changed to black
        assert game_manager.get_turn() == Color.BLACK
    
    def test_move_black_piece_empty_cell(self, setup_board):
        # Given an ongoing game
        game_manager = setup_board
        game_manager.end_turn()
        assert game_manager.get_piece_at(6,6).get_state() == Color.BLACK
        assert game_manager.get_turn() == Color.BLACK

        # And that there are 4+ black pieces remaining
        assert game_manager.pieces.count_black_remains > 3

        # When the black piece player moves a black piece to an empty and adjacent cell
        game_manager.select_piece(6,6)
        game_manager.move_piece(3,6)
        game_manager.end_turn()

        # Then the piece is placed in the cell
        assert game_manager.get_piece_at(6,6).get_state() == Color.EMPTY
        assert game_manager.get_piece_at(3,6).get_state() == Color.BLACK

        # And the turn is changed to black
        assert game_manager.get_turn() == Color.WHITE

    def test_move_white_piece_occupied_cell(self, setup_board):
        # Given an ongoing game
        game_manager = setup_board
        assert game_manager.get_piece_at(0,0).get_state() == Color.WHITE
        assert game_manager.get_piece_at(0,3).get_state() != Color.EMPTY
        assert game_manager.get_turn() == Color.WHITE

        # And that there are 4+ white pieces remaining
        assert game_manager.pieces.count_white_remains > 3

        # When the white piece player moves a white piece to an adjacent cell that is not empty
        game_manager.select_piece(0,0)
        with pytest.raises(Exception) as result:
            game_manager.move_piece(0,3)
        
        # Then the piece is unmoved
        assert game_manager.get_piece_at(0,0).get_state() == Color.WHITE
        assert game_manager.get_piece_at(0,3).get_state() == Color.BLACK
        assert str(result.value) == "MoveError -- Target position is not empty"

        # And the turn is unchanged
        assert game_manager.get_turn() == Color.WHITE

    def test_move_black_piece_occupied_cell(self, setup_board):
        # Given an ongoing game
        game_manager = setup_board
        game_manager.end_turn()
        assert game_manager.get_piece_at(6,6).get_state() == Color.BLACK
        assert game_manager.get_piece_at(6,3).get_state() != Color.EMPTY
        assert game_manager.get_turn() == Color.BLACK

        # And that there are 4+ black pieces remaining
        assert game_manager.pieces.count_black_remains > 3

        # When the black piece player moves a black piece to an empty and adjacent cell
        game_manager.select_piece(6,6)
        with pytest.raises(Exception) as result:
            game_manager.move_piece(6,3)

        # Then the piece is unmoved
        assert game_manager.get_piece_at(6,6).get_state() == Color.BLACK
        assert game_manager.get_piece_at(6,3).get_state() == Color.WHITE
        assert str(result.value) == "MoveError -- Target position is not empty"

        # And the turn is unchanged
        assert game_manager.get_turn() == Color.BLACK

    def test_move_piece_unadjacent_no_flying(self, setup_board):
        # Given an ongoing game
        game_manager = setup_board
        assert game_manager.get_piece_at(0,0).get_state() == Color.WHITE
        assert game_manager.get_piece_at(2,2).get_state() == Color.EMPTY
        assert game_manager.get_turn() == Color.WHITE

        # And the current player has more than 3 pieces remaining
        assert game_manager.pieces.count_white_remains > 3

        # When the player moves one of their pieces to a non-adjacent cell
        game_manager.select_piece(0,0)
        with pytest.raises(Exception) as result:
            game_manager.move_piece(2,2)
        
        # Then the piece is unmoved
        assert game_manager.get_piece_at(0,0).get_state() == Color.WHITE
        assert game_manager.get_piece_at(2,2).get_state() == Color.EMPTY
        assert str(result.value) == "MoveError -- Invalid move, pieces can only move to adjacent positions"

        # And the turn is unchanged
        assert game_manager.get_turn() == Color.WHITE
    
    def test_move_black_piece_white_turn(self, setup_board):
        # Given an ongoing game on white's turn
        game_manager = setup_board
        assert game_manager.get_turn() == Color.WHITE

        # When the white piece player moves a black piece to a cell
        with pytest.raises(Exception) as result:
            game_manager.select_piece(6,6)

        # Then the piece is unmoved
        assert game_manager.selected_piece == None
        assert str(result.value) == "SelectionError -- Invalid piece selection"

        # And the turn is unchanged
        assert game_manager.get_turn() == Color.WHITE
    
    def test_move_white_piece_black_turn(self, setup_board):
        # Given an ongoing game on black's turn
        game_manager = setup_board
        game_manager.end_turn()
        assert game_manager.get_turn() == Color.BLACK

        # When the black piece player moves a white piece to a cell
        with pytest.raises(Exception) as result:
            game_manager.select_piece(0,0)

        # Then the piece is unmoved
        assert game_manager.selected_piece == None
        assert str(result.value) == "SelectionError -- Invalid piece selection"

        # And the turn is unchanged
        assert game_manager.get_turn() == Color.BLACK
    
    def test_white_piece_flight_remove(self, setup_board):
        # Given an ongoing game on white's turn
        game_manager = setup_board
        assert game_manager.pieces.count_white_remains == 4
        assert game_manager.get_piece_at(6,0).get_state() == Color.WHITE
        game_manager.end_turn()
        game_manager.remove_piece_mill(6,0)
        game_manager.end_turn()
        assert game_manager.get_piece_at(6,0).get_state() == Color.EMPTY
        assert game_manager.get_piece_at(0,0).get_state() == Color.WHITE
        assert game_manager.get_piece_at(2,2).get_state() == Color.EMPTY
        assert game_manager.get_turn() == Color.WHITE

        # And white has exactly 3 pieces remaining
        assert game_manager.pieces.count_white_remains == 3

        # When a white piece is moved to an empty cell
        game_manager.select_piece(0,0)
        game_manager.move_piece(2,2)
        game_manager.end_turn()

        # Then the piece is moved to the cell
        assert game_manager.get_piece_at(0,0).get_state() == Color.EMPTY
        assert game_manager.get_piece_at(2,2).get_state() == Color.WHITE
        
        # And the turn is changed to black
        assert game_manager.get_turn() == Color.BLACK

    
    def test_black_piece_flight_remove(self, setup_board):
        # Given an ongoing game on black's turn
        game_manager = setup_board
        assert game_manager.get_piece_at(0,6).get_state() == Color.BLACK
        game_manager.remove_piece_mill(0,6)
        game_manager.end_turn()
        assert game_manager.get_piece_at(0,6).get_state() == Color.EMPTY
        assert game_manager.get_piece_at(6,6).get_state() == Color.BLACK
        assert game_manager.get_piece_at(2,2).get_state() == Color.EMPTY
        assert game_manager.get_turn() == Color.BLACK

        # And black has exactly 3 pieces remaining
        assert game_manager.pieces.count_black_remains == 3

        # When a black piece is moved to an empty cell
        game_manager.select_piece(6,6)
        game_manager.move_piece(2,2)
        game_manager.end_turn()

        # Then the piece is moved to the cell
        assert game_manager.get_piece_at(6,6).get_state() == Color.EMPTY
        assert game_manager.get_piece_at(2,2).get_state() == Color.BLACK
        
        # And the turn is changed to white
        assert game_manager.get_turn() == Color.WHITE
import pytest

from backend.Cell import Color
from backend.GameManager import GameManager

@pytest.fixture
def setup_board():
    # Given the game is Nine Men’s Morris
    board_size = 7
    total_pieces = 5
    game_manager = GameManager(board_size, total_pieces)
    valid_moves = game_manager.board.get_valid_moves()[:]

    # Do most of the piece placement phase
    game_manager.place_piece(0,0) #w
    game_manager.place_piece(6,0) #w
    game_manager.place_piece(6,3) #w
    game_manager.end_turn()
    game_manager.place_piece(3,6) #b
    game_manager.place_piece(0,6) #b
    game_manager.place_piece(3,5) #b
    game_manager.end_turn()
    board = game_manager.get_board()
    return game_manager, valid_moves

class TestMillFormation:
    #uh... i don't think these behave differently, mill/nonmill wise
    def test_place_new_horizontal_white_mill_non_mill_black(self, setup_board):
        # Given an ongoing game after white has successfully placed a piece
        game_manager, valid_moves = setup_board
        assert game_manager.get_turn() == Color.WHITE
        game_manager.place_piece(3,0)

        # When there are 3 white pieces in a row, where one of those pieces was placed this turn
        assert game_manager.is_mill_formed(3,0) == True

        # And there is at least one black piece not in a mill
        game_manager.end_turn()
        nonmill = 0
        for (row, column) in valid_moves:
            if game_manager.get_piece_at(row, column).get_state() == Color.BLACK and game_manager.is_mill_formed(row, column) == False:
                nonmill = 1
                break
        assert nonmill == 1
        game_manager.end_turn()

        # Then one of the non-mill black pieces can be removed
        assert game_manager.remove_opponent_piece() == True
        game_manager.remove_piece_mill(3,5)
        assert game_manager.get_piece_at(3,5).get_state() == Color.EMPTY
        assert game_manager.get_turn() == Color.WHITE
    
    def test_place_new_horizontal_black_mill_non_mill_white(self, setup_board):
        # Given an ongoing game after black has successfully placed a piece
        game_manager, valid_moves = setup_board
        game_manager.end_turn()
        assert game_manager.get_turn() == Color.BLACK
        game_manager.place_piece(6,6)

        # When there are 3 white pieces in a row, where one of those pieces was placed this turn
        assert game_manager.is_mill_formed(6,6) == True

        # And there is at least one black piece not in a mill
        game_manager.end_turn()
        nonmill = 0
        for (row, column) in valid_moves:
            if game_manager.get_piece_at(row, column).get_state() == Color.WHITE and game_manager.is_mill_formed(row, column) == False:
                nonmill = 1
                break
        assert nonmill == 1
        game_manager.end_turn()

        # Then one of the non-mill black pieces can be removed
        assert game_manager.remove_opponent_piece() == True
        game_manager.remove_piece_mill(0,0)
        assert game_manager.get_piece_at(0,0).get_state() == Color.EMPTY
        assert game_manager.get_turn() == Color.BLACK
    
    def test_place_new_vertical_white_mill_non_mill_black(self, setup_board):
        # Given an ongoing game after white has successfully placed a piece
        game_manager, valid_moves = setup_board
        assert game_manager.get_turn() == Color.WHITE
        game_manager.place_piece(6,6)

        # When there are 3 white pieces in a row, where one of those pieces was placed this turn
        assert game_manager.is_mill_formed(6,6) == True

        # And there is at least one black piece not in a mill
        game_manager.end_turn()
        nonmill = 0
        for (row, column) in valid_moves:
            if game_manager.get_piece_at(row, column).get_state() == Color.BLACK and game_manager.is_mill_formed(row, column) == False:
                nonmill = 1
                break
        assert nonmill == 1
        game_manager.end_turn()

        # Then one of the non-mill black pieces can be removed
        assert game_manager.remove_opponent_piece() == True
        game_manager.remove_piece_mill(3,5)
        assert game_manager.get_piece_at(3,5).get_state() == Color.EMPTY
        assert game_manager.get_turn() == Color.WHITE
    
    def test_place_new_vertical_black_mill_non_mill_white(self, setup_board):
        # Given an ongoing game after black has successfully placed a piece
        game_manager, valid_moves = setup_board
        game_manager.end_turn()
        assert game_manager.get_turn() == Color.BLACK
        game_manager.place_piece(3,4)

        # When there are 3 white pieces in a row, where one of those pieces was placed this turn
        assert game_manager.is_mill_formed(3,4) == True

        # And there is at least one black piece not in a mill
        game_manager.end_turn()
        nonmill = 0
        for (row, column) in valid_moves:
            if game_manager.get_piece_at(row, column).get_state() == Color.WHITE and game_manager.is_mill_formed(row, column) == False:
                nonmill = 1
                break
        assert nonmill == 1
        game_manager.end_turn()

        # Then one of the non-mill black pieces can be removed
        assert game_manager.remove_opponent_piece() == True
        game_manager.remove_piece_mill(0,0)
        assert game_manager.get_piece_at(0,0).get_state() == Color.EMPTY
        assert game_manager.get_turn() == Color.BLACK
    
    def test_place_new_white_mill_only_mill_black(self, setup_board):
        # Given an ongoing game after white has successfully placed a piece
        game_manager, valid_moves = setup_board
        game_manager.remove_piece_mill(3,5)
        game_manager.end_turn()
        game_manager.place_piece(6,6)
        game_manager.end_turn()
        game_manager.place_piece(3,0)
        assert game_manager.get_turn() == Color.WHITE

        # When there are 3 white pieces in a row, where one of those pieces was placed this turn
        assert game_manager.is_mill_formed(3,0) == True

        # And all black pieces are in a mill
        game_manager.end_turn()
        nonmill = 0
        for (row, column) in valid_moves:
            if game_manager.get_piece_at(row, column).get_state() == Color.BLACK and game_manager.is_mill_formed(row, column) == False:
                nonmill = 1
                break
        assert nonmill == 0
        game_manager.end_turn()

        # Then one of the mill black pieces can be removed
        assert game_manager.remove_opponent_piece() == True
        game_manager.remove_piece_mill(6,6)
        assert game_manager.get_piece_at(6,6).get_state() == Color.EMPTY
        assert game_manager.get_turn() == Color.WHITE
    
    # Can be implemented later if we want more holistic tests (or need extra lines of code)
    def test_place_new_black_mill_only_mill_white(self, setup_board):
        # Given an ongoing game after white has successfully placed a piece
        game_manager, valid_moves = setup_board
        game_manager.remove_piece_mill(6,3)
        game_manager.place_piece(3,0)
        game_manager.end_turn()
        game_manager.place_piece(6,6)
        assert game_manager.get_turn() == Color.BLACK

        # When there are 3 white pieces in a row, where one of those pieces was placed this turn
        assert game_manager.is_mill_formed(6,6) == True

        # And all black pieces are in a mill
        game_manager.end_turn()
        nonmill = 0
        for (row, column) in valid_moves:
            if game_manager.get_piece_at(row, column).get_state() == Color.WHITE and game_manager.is_mill_formed(row, column) == False:
                nonmill = 1
                break
        assert nonmill == 0
        game_manager.end_turn()

        # Then one of the mill black pieces can be removed
        assert game_manager.remove_opponent_piece() == True
        game_manager.remove_piece_mill(0,0)
        assert game_manager.get_piece_at(0,0).get_state() == Color.EMPTY
        assert game_manager.get_turn() == Color.BLACK

    def test_move_new_white_mill(self, setup_board):
        # Given an ongoing game after white has successfully moved a piece
        game_manager, valid_moves = setup_board
        game_manager.place_piece(3,1)
        game_manager.place_piece(1,1)
        game_manager.end_turn()
        game_manager.place_piece(5,5)
        game_manager.place_piece(0,3)
        game_manager.end_turn()
        game_manager.select_piece(3,1)
        game_manager.move_piece(3,0)
        assert game_manager.get_turn() == Color.WHITE

        # When there are 3 white pieces in a row, where one of those pieces was placed this turn
        assert game_manager.is_mill_formed(3,0) == True

        # Then one of the black pieces can be removed
        assert game_manager.remove_opponent_piece() == True
        game_manager.remove_piece_mill(3,5)
        assert game_manager.get_piece_at(3,5).get_state() == Color.EMPTY
        assert game_manager.get_turn() == Color.WHITE
    
    def test_move_no_new_mill(self, setup_board):
        # Given an ongoing game where white has a mill from a previous turn
        game_manager, valid_moves = setup_board
        game_manager.place_piece(3,0)

        # When the player moves this turn
        game_manager.place_piece(3,1)

        # The player does not make a new mill
        assert game_manager.is_mill_formed(3,1) == False
    
    def test_place_double_mill(self, setup_board):
        # Given an ongoing game where white has a mill from a previous turn
        game_manager, valid_moves = setup_board
        game_manager.place_piece(3,0)

        # When one mill is from a previous turn
        assert game_manager.is_mill_formed(3,0)

        # And a second mill, connected to the first, is formed this turn
        game_manager.place_piece(6,6)
        assert game_manager.is_mill_formed(6,6)

        # Then one of the black pieces can be removed
        assert game_manager.remove_opponent_piece() == True
        game_manager.remove_piece_mill(3,5)
        assert game_manager.get_piece_at(3,5).get_state() == Color.EMPTY
        assert game_manager.get_turn() == Color.WHITE
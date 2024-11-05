import pytest

from backend.Cell import Color
from backend.GameManager import GameManager

@pytest.fixture
def setup_board():
    # Given the game is Nine Men’s Morris
    board_size = 7
    total_pieces = 4
    game_manager = GameManager(board_size, total_pieces)

    board = game_manager.get_board()
    return game_manager

class TestGameOver:
    def test_white_no_moves(self, setup_board):
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

        # And it's white's turn
        assert game_manager.get_turn() == Color.WHITE

        # When none of the white pieces can move
        assert len(game_manager.get_movable_options(0,0)) == 0
        assert len(game_manager.get_movable_options(3,0)) == 0
        assert len(game_manager.get_movable_options(0,3)) == 0
        assert len(game_manager.get_movable_options(1,1)) == 0

        # Then the game is over
        result = game_manager.check_game_over()

        # And the black piece player has won
        assert result == Color.BLACK

    def test_black_no_moves(self, setup_board):
        # Given an ongoing game with a complete piece placement phase
        game_manager = setup_board
        game_manager.end_turn()
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

        # And it's black's turn
        assert game_manager.get_turn() == Color.BLACK

        # When none of the black pieces can move
        assert len(game_manager.get_movable_options(0,0)) == 0
        assert len(game_manager.get_movable_options(3,0)) == 0
        assert len(game_manager.get_movable_options(0,3)) == 0
        assert len(game_manager.get_movable_options(1,1)) == 0

        # Then the game is over
        result = game_manager.check_game_over()

        # And the white piece player has won
        assert result == Color.WHITE

    def test_white_too_few_pieces(self, setup_board):
        # Given an ongoing game with a complete piece placement phase
        game_manager = setup_board
        game_manager.place_piece(0,0)
        game_manager.place_piece(6,0)
        game_manager.place_piece(6,3)
        game_manager.place_piece(3,1)
        game_manager.end_turn()
        game_manager.place_piece(3,6)
        game_manager.place_piece(0,6)
        game_manager.place_piece(3,5)
        game_manager.place_piece(2,4)
        game_manager.remove_piece_mill(0,0)

        # And it's black's turn
        assert game_manager.get_turn() == Color.BLACK

        # When a black piece mill is formed
        game_manager.select_piece(2,4)
        game_manager.move_piece(3,4)
        assert game_manager.is_mill_formed(3,4) == True

        # And a white piece is removed from the board
        assert game_manager.remove_opponent_piece({(6,0):Color.WHITE,(6,3):Color.WHITE,(3,1):Color.WHITE,(3,6):Color.BLACK,(0,6):Color.BLACK,(3,5):Color.BLACK,(3,4):Color.BLACK}) == True
        game_manager.remove_piece_mill(6,3)
        assert game_manager.get_piece_at(6,3).get_state() == Color.EMPTY

        # And there are less than 3 white pieces remaining 
        assert game_manager.pieces.count_white_remains < 3

        # Then the game is over
        result = game_manager.check_game_over()

        # And the black piece player has won    
        assert result == Color.BLACK

    def test_black_too_few_pieces(self, setup_board):
        # Given an ongoing game with a complete piece placement phase
        game_manager = setup_board
        game_manager.place_piece(0,0)
        game_manager.place_piece(6,0)
        game_manager.place_piece(6,3)
        game_manager.place_piece(3,1)
        game_manager.end_turn()
        game_manager.place_piece(3,6)
        game_manager.place_piece(0,6)
        game_manager.place_piece(3,5)
        game_manager.place_piece(2,4)
        game_manager.end_turn()
        game_manager.remove_piece_mill(3,6)

        # And it's white's turn
        assert game_manager.get_turn() == Color.WHITE

        # When a white piece mill is formed
        game_manager.select_piece(3,1)
        game_manager.move_piece(3,0)
        assert game_manager.is_mill_formed(3,0) == True

        # And a black piece is removed from the board
        assert game_manager.remove_opponent_piece({(0,0):Color.WHITE,(6,0):Color.WHITE,(6,3):Color.WHITE,(3,0):Color.WHITE,(0,6):Color.BLACK,(3,5):Color.BLACK,(3,4):Color.BLACK}) == True
        game_manager.remove_piece_mill(2,4)
        assert game_manager.get_piece_at(2,4).get_state() == Color.EMPTY

        # And there are less than 3 black pieces remaining 
        assert game_manager.pieces.count_black_remains < 3

        # Then the game is over
        result = game_manager.check_game_over()

        # And the white piece player has won    
        assert result == Color.WHITE
        
    def test_place_white_game_over(self, setup_board):
        # Given an ongoing game in the piece placement phase
        game_manager = setup_board

        # When a white piece is placed
        game_manager.place_piece(0,0)

        # And less than 3 white pieces have been placed
        assert game_manager.pieces.count_white_placed < 3

        # Then the game is not over
        assert game_manager.check_game_over() == None

    def test_place_black_game_over(self, setup_board):
        # Given an ongoing game in the piece placement phase
        game_manager = setup_board
        game_manager.end_turn()

        # When a black piece is placed
        game_manager.place_piece(0,0)

        # And less than 3 black pieces have been placed
        assert game_manager.pieces.count_black_placed < 3

        # Then the game is not over
        assert game_manager.check_game_over() == None

    def test_place_black_mill_white_game_over(self, setup_board):
        # Given an ongoing game in the piece placement phase
        game_manager = setup_board
        game_manager.place_piece(0,0)
        game_manager.place_piece(3,0)
        game_manager.place_piece(0,3)
        game_manager.end_turn()
        game_manager.place_piece(6,6)
        game_manager.place_piece(3,6)

        # And it's black's turn
        assert game_manager.get_turn() == Color.BLACK

        # When a black mill is formed
        game_manager.place_piece(0,6)
        assert game_manager.is_mill_formed(0,6) == True

        # And a white piece is removed from the board
        assert game_manager.remove_opponent_piece({(0,0):Color.WHITE,(3,0):Color.WHITE,(0,3):Color.WHITE,(0,6):Color.BLACK,(3,6):Color.BLACK,(6,6):Color.BLACK}) == True
        game_manager.remove_piece_mill(0,3)
        assert game_manager.get_piece_at(0,3).get_state() == Color.EMPTY

        # And less than 3 white pieces remain on the board
        assert game_manager.pieces.count_white_remains < 3

        # Then the game is not over
        assert game_manager.check_game_over() == None

        game_manager.end_turn()

        # And the turn is changed to white
        assert game_manager.get_turn() == Color.WHITE

    def test_place_white_mill_black_game_over(self, setup_board):
        # Given an ongoing game in the piece placement phase
        game_manager = setup_board
        game_manager.place_piece(0,0)
        game_manager.place_piece(3,0)
        game_manager.place_piece(0,3)
        game_manager.end_turn()
        game_manager.place_piece(6,6)
        game_manager.place_piece(3,6)
        game_manager.place_piece(3,5)
        game_manager.end_turn()

        # And it's white's turn
        assert game_manager.get_turn() == Color.WHITE

        # When a white mill is formed
        game_manager.place_piece(6,0)
        assert game_manager.is_mill_formed(6,0) == True

        # And a black piece is removed from the board
        assert game_manager.remove_opponent_piece({(0,0):Color.WHITE,(3,0):Color.WHITE,(0,3):Color.WHITE,(6,0):Color.WHITE,(3,5):Color.BLACK,(3,6):Color.BLACK,(6,6):Color.BLACK}) == True
        game_manager.remove_piece_mill(6,6)
        assert game_manager.get_piece_at(6,6).get_state() == Color.EMPTY

        # And less than 3 black pieces remain on the board
        assert game_manager.pieces.count_black_remains < 3

        # Then the game is not over
        assert game_manager.check_game_over() == None
        
        game_manager.end_turn()

        # And the turn is changed to black
        assert game_manager.get_turn() == Color.BLACK
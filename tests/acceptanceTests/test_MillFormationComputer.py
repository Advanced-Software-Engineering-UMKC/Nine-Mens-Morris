import pytest

from backend.Cell import Color
from backend.GameManager import GameManager

@pytest.fixture
def setup_board():
    # Given the game is Nine Men’s Morris
    board_size = 7
    total_pieces = 5
    game_manager = GameManager(board_size, total_pieces)
    game_manager.set_use_computer_opponent(True)

    # Do most of the piece placement phase
    game_manager.place_piece(0,0) #w
    game_manager.place_piece(6,0) #w
    game_manager.place_piece(6,3) #w
    game_manager.end_turn()
    game_manager.place_piece(3,6) #b
    game_manager.place_piece(0,6) #b
    game_manager.place_piece(3,5) #b
    board = game_manager.get_board()
    return game_manager

class TestMillFormationComputer:
    def test_mill_computer_human_mills_only(self, setup_board):
        # Given an ongoing game
        game_manager = setup_board
        game_manager.end_turn()
        game_manager.place_piece(3,0)
        game_manager.place_piece(6,6)
        game_manager.end_turn()
        init_pos = game_manager.player_1.get_placed_pieces_position()
        assert game_manager.get_turn() == Color.BLACK

        # When there are 3 computer pieces in a row, where one of those pieces was placed this turn
        game_manager.handle_piece_placement(3,4)

        # And there is at least one human piece not in a mill
        assert len(init_pos) > 0

        # Then one of the millec human pieces can be removed
        results = []
        for piece in init_pos:
            results.append(game_manager.board.check_position(piece[0], piece[1]) == Color.EMPTY)

        assert True in results

    def test_mill_computer_free_human_piece(self, setup_board):
        # Given an ongoing game
        game_manager = setup_board
        nonmill = game_manager.player_1.get_placed_pieces_position()
        assert game_manager.get_turn() == Color.BLACK

        # When there are 3 computer pieces in a row, where one of those pieces was placed this turn
        game_manager.handle_piece_placement(6,6)

        # And there is at least one human piece not in a mill
        assert len(nonmill) > 0

        # Then one of the non-mill human pieces can be removed
        results = []
        for piece in nonmill:
            results.append(game_manager.board.check_position(piece[0], piece[1]) == Color.EMPTY)

        assert True in results
    
    def test_previous_mill_computer(self, setup_board):
         # Given an ongoing game where the computer has a mill from a previous turn
        game_manager = setup_board
        game_manager.place_piece(6,6)
        game_manager.end_turn()
        game_manager.place_piece(3,4) # block (3,4) so no mills are made
        game_manager.end_turn()
        init_pos = game_manager.player_1.get_placed_pieces_position()

        # When there are 3 computer pieces in a row, where one of those pieces was placed this turn
        game_manager.handle_computer_turn()

        # No pieces are removed
        results = []
        for piece in init_pos:
            results.append(game_manager.board.check_position(piece[0], piece[1]) == Color.EMPTY)

        assert True not in results
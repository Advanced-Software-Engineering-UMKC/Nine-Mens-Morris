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

class TestPiecePlacement:
    # Scenario: Placing a white piece on an empty cell
    def test_place_white_piece_on_empty_cell(self, setup_board):
        # Given the game is Nine Men’s Morris
        board_class_instance, board_size, game_manager = setup_board

        # When a white piece is placed on an empty cell
        game_manager.place_piece(0, 0)
        game_manager.end_turn()

        # Then the cell is occupied by a white piece
        assert board_class_instance.check_position(0, 0) == CellType.WHITE

        # And the turn is changed to black
        assert game_manager.get_turn() == Turn.BLACK

    # Scenario: Placing a black piece on an empty cell
    def test_place_black_piece_on_empty_cell(self, setup_board):
        # Given the game is Nine Men’s Morris
        board_class_instance, board_size, game_manager = setup_board

        # When a black piece is placed on an empty cell
        game_manager.place_piece(0, 0)
        game_manager.end_turn()
        game_manager.place_piece(1, 1)
        game_manager.end_turn()

        # Then the cell is occupied by a black piece
        assert board_class_instance.check_position(1, 1) == CellType.BLACK

        # And the turn is changed to white
        assert game_manager.get_turn() == Turn.WHITE
    
    # Scenario: Placing a piece on an occupied cell
    def test_place_piece_on_occupied_cell(self, setup_board):
        # Given the game is Nine Men’s Morris
        board_class_instance, board_size, game_manager = setup_board

        # When a piece is placed on an occupied cell
        game_manager.place_piece(0, 0)
        game_manager.end_turn()
        res = game_manager.place_piece(0, 0)

        # Then an error message is returned
        assert res == "GameManagerError -- invalid piece placement position"


    # Scenario: Placing a piece on a cell that is out of bounds
    def test_place_piece_out_of_bounds(self, setup_board):
        # Given the game is Nine Men’s Morris
        board_class_instance, board_size, game_manager = setup_board

        # When a piece is placed on a cell that is out of bounds
        res = game_manager.place_piece(7, 0)

        # Then an error message is returned
        assert res == "GameManagerError -- invalid piece placement position"

    # Scenario: Placing white piece after all pieces have been placed
    def test_place_white_piece_after_all_pieces_placed(self, setup_board):
        # Given the game is Nine Men’s Morris
        board_class_instance, board_size, game_manager = setup_board

        # When all pieces have been placed
        for i in range(9):
            game_manager.place_piece(i, i)
            game_manager.end_turn()

        # Then an error message is returned
        res = game_manager.place_piece(0, 0)
        assert res == "GameManagerError -- invalid piece placement position"
    
    # Scenario: Placing black piece after all pieces have been placed
    def test_place_black_piece_after_all_pieces_placed(self, setup_board):
        # Given the game is Nine Men’s Morris
        board_class_instance, board_size, game_manager = setup_board

        # When all pieces have been placed
        for i in board_class_instance.get_valid_moves():
            game_manager.place_piece(i[0], i[1])
            game_manager.end_turn()

        # Then an error message is returned
        res = game_manager.place_piece(0, 0)
        assert res == "GameManagerError -- invalid piece placement position"
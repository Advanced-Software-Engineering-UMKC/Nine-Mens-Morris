import pytest

from backend.Cell import Color
from backend.GameManager import GameManager


@pytest.fixture
def setup_board():
    # Given the game is Twelve Men’s Morris
    board_size = 7
    total_pieces = 12
    game_manager = GameManager(board_size, total_pieces)

    # When a new game is started
    board_class_instance = game_manager.get_board()
    return board_class_instance, board_size, game_manager


class TestTwelveMen:
    # Scenario: New game starts with an empty board
    def test_empty_board(self, setup_board):
        # Given a Twelve Men’s Morris board
        # When a new game is started
        board_class_instance, board_size, _ = setup_board

        # Then there will be an empty 5x5 Twelve Men’s Morris board
        assert len(board_class_instance.board) == board_size
        assert len(board_class_instance.board[0]) == board_size
        assert board_class_instance.get_valid_moves() is not []

        for row_index, row in enumerate(board_class_instance.board):
            for cell_index, cell in enumerate(row):
                assert cell.state != Color.BLACK and cell.state != Color.WHITE
                cell_position = (row_index, cell_index)
                if cell_position in board_class_instance.get_valid_moves():
                    assert cell.state == Color.EMPTY
                else:
                    assert cell.state == Color.VOID

    def test_twelve_piece_placement(self, setup_board):
        # Given a ongoing Twelve Men’s Morris game in piece placement phase
        board_class_instance, board_size, game_manager = setup_board
        assert game_manager.placement_complete() == False
        
        # When all pieces are placed
        game_manager.place_piece(0,0)
        game_manager.place_piece(3,0)
        game_manager.place_piece(6,0)
        game_manager.place_piece(0,3)
        game_manager.place_piece(0,6)
        game_manager.place_piece(6,3)
        game_manager.place_piece(6,6)
        game_manager.place_piece(3,6)
        game_manager.place_piece(1,1)
        game_manager.place_piece(1,3)
        game_manager.place_piece(1,5)
        game_manager.place_piece(3,1)
        game_manager.end_turn()

        game_manager.place_piece(3,5)
        game_manager.place_piece(5,1)
        game_manager.place_piece(5,3)
        game_manager.place_piece(5,5)
        game_manager.place_piece(2,2)
        game_manager.place_piece(2,3)
        game_manager.place_piece(2,4)
        game_manager.place_piece(3,2)
        game_manager.place_piece(3,4)
        game_manager.place_piece(4,2)
        game_manager.place_piece(4,3)
        game_manager.place_piece(4,4)

        # The placement phase is complete
        assert game_manager.placement_complete() == True


if __name__ == "__main__":
    pytest.main()

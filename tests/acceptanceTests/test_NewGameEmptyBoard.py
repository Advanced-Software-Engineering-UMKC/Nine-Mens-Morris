import pytest

from backend.Board import Board
from backend.Cell import CellType
from backend.GameManager import GameManager


@pytest.fixture
def setup_board():
    # Given the game is Nine Men’s Morris
    board_size = 7
    total_pieces = 9
    game_manager = GameManager(board_size, total_pieces)

    # When a new game is started
    board_class_instance = game_manager.get_board()
    return board_class_instance, board_size


class TestNewGameEmptyBoard:
    # Scenario: New game starts with an empty board
    def test_empty_board(self, setup_board):
        # Given a Nine Men’s Morris board
        # When a new game is started
        board_class_instance, board_size = setup_board

        # Then there will be an empty 7x7 Nine Men’s Morris board
        assert len(board_class_instance.board) == board_size
        assert len(board_class_instance.board[0]) == board_size
        assert board_class_instance.get_valid_moves() is not []

        for row_index, row in enumerate(board_class_instance.board):
            for cell_index, cell in enumerate(row):
                assert cell.state != CellType.BLACK and cell.state != CellType.WHITE
                cell_position = (row_index, cell_index)
                if cell_position in board_class_instance.get_valid_moves():
                    assert cell.state == CellType.EMPTY
                else:
                    assert cell.state == CellType.VOID

    # Scenario: Invalid Row Index
    def test_invalid_row(self, setup_board):
        # Given a Nine Men’s Morris board
        board_class_instance, board_size = setup_board
        # When a cell is referenced by a row index greater than 6
        row_index = 7
        # Then an IndexError exception is raised
        with pytest.raises(IndexError):
            board_class_instance.board[row_index][0]

    # Scenario: Invalid Column Index
    def test_invalid_column(self, setup_board):
        # Given a Nine Men’s Morris board
        board_class_instance, board_size = setup_board
        # When a cell is referenced by a column index greater than 6
        column_index = 7
        # Then an IndexError exception is raised
        with pytest.raises(IndexError):
            board_class_instance.board[0][column_index]


if __name__ == "__main__":
    pytest.main()
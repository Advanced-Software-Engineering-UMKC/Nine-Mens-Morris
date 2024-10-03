import backend.Board as Board
import pytest
import pygame as pg
from backend.Cell import Cell, CellType

# fixtures create reusable instances for testing
@pytest.fixture
def board():
    """Fixture to create a Board instance."""
    # Initialize Pygame
    pg.init()
    board = Board.Board(7)
    yield board
    pg.quit()

class TestBoard:
    # def test_add_tile(self, board):
    #     """Test if add_tile method works correctly."""
    #     board.add_tile()
    #     assert board.game_over
    #     assert board.won


    def test_board_initialization(self, board):
        # Test if the board is initialized with the correct size
        assert len(board.board) == board.board_size
        assert all(len(row) == board.board_size for row in board.board)


    def test_valid_moves_initialization(self, board):
        # Test if the valid moves are initialized properly
        valid_moves = board.get_valid_moves()
        assert isinstance(valid_moves, list)
        assert all(isinstance(move, tuple) for move in valid_moves)


    def test_empty_board_valid_moves(self, board):
        # Check that valid cells are set to EMPTY initially
        for row, column in board.get_valid_moves():
            assert board.check_position(row, column) == "empty"


    def test_set_position(self, board):
        board.set_position(0, 0, "white")
        state = board.check_position(0, 0)
        assert state == "white"


'''
    def test_create_board_indices_array(self, board):
        """Test if create_board_indices_array method works correctly."""
        num_lines = 7
        board_of_cells = board.create_board_indices_array(num_lines)

        # assert board_indicies_array is a list of coordinates
        assert isinstance(board_of_cells, list)
        for line in board_of_cells:
            assert isinstance(line, list)
            for cell in line:
                assert isinstance(cell, Cell.Cell)
            assert len(line) == num_lines
        assert len(board_of_cells) == num_lines
'''
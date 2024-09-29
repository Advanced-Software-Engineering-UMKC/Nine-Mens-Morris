import backend.Board as Board
import pytest
import pygame as pg
import backend.Cell as Cell

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
    # def test_board_initialization(self, board):
    #     """Test if Board initializes correctly."""


    # def test_add_tile(self, board):
    #     """Test if add_tile method works correctly."""
    #     board.add_tile()
    #     assert board.game_over
    #     assert board.won

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
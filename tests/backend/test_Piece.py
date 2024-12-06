import pytest

from backend.Piece import *
from backend.Player import Player
from backend.GameManager import GameManager


@pytest.fixture
def piece():
    piece = Piece(Color.WHITE)
    yield piece


@pytest.fixture
def pieces():
    game_manager = GameManager(7, 9)
    yield game_manager


class TestPiece:
    def test_piece_initialization(self, piece):
        # Test if the piece is initialized with the expected values
        assert piece.get_color() == Color.WHITE
        assert piece.get_position() == (-1, -1)

    def test_piece_set_turn(self, piece):
        piece.set_turn(Color.BLACK)
        assert piece.get_color() == Color.BLACK

    def test_piece_set_position(self, piece):
        piece.set_position((1, 1))
        assert piece.get_position() == (1, 1)

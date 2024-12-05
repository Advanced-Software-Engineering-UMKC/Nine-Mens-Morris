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


# class TestPieces:
#     def test_all_pieces_placed(self, pieces):
#         # at initialization all pieces are not expected to be placed
#         assert not game_manager.player_1.all_pieces_placed()
#         assert not game_manager.player_2.all_pieces_placed()

#         # placing all pieces
#         pieces.set_white_piece(0, 0)
#         pieces.set_white_piece(0, 3)
#         pieces.set_white_piece(0, 6)
#         pieces.set_white_piece(1, 1)
#         pieces.set_white_piece(1, 3)
#         pieces.set_white_piece(1, 5)
#         pieces.set_white_piece(2, 2)
#         pieces.set_white_piece(2, 3)
#         pieces.set_white_piece(2, 4)

#         pieces.set_black_piece(3, 0)
#         pieces.set_black_piece(3, 1)
#         pieces.set_black_piece(3, 2)
#         pieces.set_black_piece(3, 4)
#         pieces.set_black_piece(3, 5)
#         pieces.set_black_piece(3, 6)
#         pieces.set_black_piece(4, 2)
#         pieces.set_black_piece(4, 3)
#         pieces.set_black_piece(4, 4)

#         # all pieces are expected to be placed
#         assert pieces.all_pieces_placed()

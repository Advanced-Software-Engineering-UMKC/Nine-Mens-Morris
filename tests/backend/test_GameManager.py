import pytest

from backend.GameManager import *


def place_test_pieces(game_manager):
    # Test piece placement
    game_manager.place_piece(0, 0)
    game_manager.end_turn()
    game_manager.place_piece(0, 6)
    game_manager.end_turn()
    game_manager.place_piece(3, 0)
    game_manager.end_turn()
    game_manager.place_piece(3, 6)
    game_manager.end_turn()
    game_manager.place_piece(6, 0)
    game_manager.end_turn()
    game_manager.place_piece(6, 3)
    game_manager.end_turn()
    game_manager.place_piece(6, 6)
    game_manager.end_turn()
    game_manager.place_piece(1, 1)
    game_manager.end_turn()
    game_manager.place_piece(1, 3)
    game_manager.end_turn()
    game_manager.place_piece(1, 5)
    game_manager.end_turn()
    game_manager.place_piece(3, 1)
    game_manager.end_turn()
    game_manager.place_piece(3, 5)
    game_manager.end_turn()
    game_manager.place_piece(5, 1)
    game_manager.end_turn()
    game_manager.place_piece(5, 3)
    game_manager.end_turn()
    game_manager.place_piece(5, 5)
    game_manager.end_turn()
    game_manager.place_piece(2, 2)
    game_manager.end_turn()
    game_manager.place_piece(2, 3)
    game_manager.end_turn()
    game_manager.place_piece(2, 4)
    game_manager.end_turn()
    return game_manager


@pytest.fixture
def game_manager():
    game_manager = GameManager(7, 9)
    yield game_manager


class TestGameManager:
    def test_initial_turn(self, game_manager):
        # Test if the initial turn is WHITE
        assert game_manager.get_turn() == Color.WHITE

    def test_all_pieces_placed(self, game_manager):
        # Test at initialization all pieces are not expected to be placed
        assert not game_manager.placement_complete()

    def test_place_piece(self, game_manager):
        # Test piece placement
        res = game_manager.place_piece(0, 0)
        assert res == 1

        game_manager.end_turn()
        res = game_manager.place_piece(0, 0)
        assert res == "GameManagerError -- invalid piece placement position"

    def test_end_turn(self, game_manager):
        # Test if the turn changes
        turn = game_manager.get_turn()
        game_manager.end_turn()
        assert game_manager.get_turn() != turn

    def test_move_piece(self, game_manager):
        # placing all 9 pieces for both players
        game_manager = place_test_pieces(game_manager)

        try:
            # selecting piece (0, 0) for player WHITE
            move_options = game_manager.select_piece(0, 0)
            assert move_options[0] == (0, 3)

            # moving to (0, 3)
            assert game_manager.move_piece(0, 3)
        except Exception as e:
            pytest.fail(f"Test failed due to unexpected exception: {e}")

    def test_fly_piece(self, game_manager):
        # placing all 9 pieces for both players
        game_manager = place_test_pieces(game_manager)

        # decreasing the black piece count to 3
        for i in range(6):
            game_manager.pieces.decrease_black_piece_count()

        game_manager.end_turn()

        assert game_manager.can_fly(game_manager.turn)

    def test_end_game(self, game_manager):
        # placing all 9 pieces for both players
        game_manager = place_test_pieces(game_manager)

        # decreasing the black piece count to 3
        for i in range(6):
            game_manager.pieces.decrease_black_piece_count()

        assert game_manager.check_game_over() is None

        # decreasing the black piece count to 2
        game_manager.pieces.decrease_black_piece_count()

        assert game_manager.check_game_over() is Color.WHITE

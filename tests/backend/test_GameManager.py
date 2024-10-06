from backend.GameManager import *
import pytest


@pytest.fixture
def game_manager():
    game_manager = GameManager(7, 9)
    yield game_manager

class TestGameManager:
    def test_initial_turn(self, game_manager):
        # Test if the initial turn is WHITE
        assert game_manager.get_turn() == Turn.WHITE

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


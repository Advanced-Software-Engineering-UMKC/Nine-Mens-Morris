import pytest

from backend.Cell import Color
from backend.GameManager import GameManager


@pytest.fixture
def setup_board():
    # Given the game is Nine Men’s Morris
    board_size = 7
    total_pieces = 9
    game_manager = GameManager(board_size, total_pieces)
    game_manager.set_use_computer_opponent(True)

    return game_manager


class TestPiecePlacementComputer:
    def test_piece_placed_computer(self, setup_board):
        game_manager = setup_board
        open_moves = game_manager.open_moves
        mills = game_manager.mills
        board = game_manager.board
        
        # When the comptuer places a piece
        game_manager.end_turn()
        place = game_manager.player_2.decide_piece_placement(open_moves, mills, board)

        # And the chosen cell is empty
        assert board.check_position(place[0], place[1]) == Color.EMPTY

        # And there have been less than 9 computer pieces placed
        assert game_manager.placement_complete() == False

        # Then the piece is placed
        game_manager.handle_piece_placement(place[0], place[1])
        assert place in game_manager.player_2.get_placed_pieces_position()
        assert game_manager.get_turn() != game_manager.player_2.color

    def test_place_occupied_cell_computer(self, setup_board):
        # Given an ongoing game
        game_manager = setup_board
        game_manager.place_piece(0,0)
        game_manager.end_turn()

        # When the computer places a piece on a non-empty cell
        game_manager.handle_piece_placement(0,0)

        # Then the cell and turn are unchanged
        assert game_manager.board.check_position(0,0) == Color.WHITE
        assert game_manager.get_turn() == Color.BLACK

    def test_place_extra_computer(self, setup_board):
        # Given an ongoing Nine Men's Morris game
        game_manager = setup_board

        game_manager.place_piece(0,0)
        game_manager.place_piece(3,0)
        game_manager.place_piece(6,0)
        game_manager.place_piece(0,3)
        game_manager.place_piece(0,6)
        game_manager.place_piece(6,3)
        game_manager.place_piece(6,6)
        game_manager.place_piece(3,6)
        game_manager.place_piece(1,1)
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

        # When the computer places a piece
        game_manager.handle_piece_placement(4,4)

        # And the placement phase is over
        assert game_manager.placement_complete() == True

        # The board and turn are unchanged
        assert game_manager.board.check_position(4,4) == Color.EMPTY
        assert game_manager.get_turn() == Color.BLACK


if __name__ == "__main__":
    pytest.main()

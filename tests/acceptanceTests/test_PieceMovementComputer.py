import pytest

from backend.Cell import Color
from backend.GameManager import GameManager
from backend.Piece import Piece

@pytest.fixture
def setup_board():
    # Given the game is Nine Men’s Morris
    board_size = 7
    total_pieces = 4
    game_manager = GameManager(board_size, total_pieces)
    game_manager.set_use_computer_opponent(True)

    # Complete the piece placement phase
    game_manager.place_piece(0,0) #w
    game_manager.place_piece(6,0) #w
    game_manager.place_piece(6,3) #w
    game_manager.place_piece(5,1) #w
    game_manager.end_turn()
    game_manager.place_piece(6,6) #b
    game_manager.place_piece(0,6) #b
    game_manager.place_piece(5,5) #b
    game_manager.place_piece(0,3) #b
    return game_manager

class TestPieceMovement:
    def test_movement_computer(self, setup_board):
        # Given an ongoing game on the computer opponent's turn
        game_manager = setup_board
        mills = game_manager.mills
        board = game_manager.board

        # And that there are 4+ computer pieces remaining
        assert len(game_manager.player_2.pieces) > 3

        # When the computer player moves a piece to a cell
        selected, open_moves = game_manager.player_2.decide_piece_to_move(mills, board, game_manager.can_fly(game_manager.player_2))
        game_manager.selected_piece = selected.position
        move = game_manager.player_2.decide_move_target(mills, open_moves, board)
        # And the chosen cell is empty and adjacent
        assert move in board.find_empty_adjacents(selected.position[0], selected.position[1])

        # Then the piece is moved to the cell
        game_manager.move_piece(move[0], move[1])
        game_manager.end_turn()
        # And the turn is changed to human
        assert game_manager.get_turn() == Color.WHITE
    
    def test_no_flying_non_adjacent_computer(self, setup_board):
        # Given an ongoing game on the computer opponent's turn
        game_manager = setup_board
        mills = game_manager.mills
        board = game_manager.board
        adj = board.adjacent_positions_map

        # And that there are 4+ computer pieces remaining
        assert len(game_manager.player_2.pieces) > 3

        # When the computer player moves a piece to a cell
        selected, open_moves = game_manager.player_2.decide_piece_to_move(mills, board, game_manager.can_fly(game_manager.player_2))
        game_manager.selected_piece = selected.position
        moves = board.find_empty_adjacents(selected.position[0], selected.position[1])
        move = (-1,-1)
        for cell in adj:
            if cell not in moves and board.check_position(cell[0], cell[1]) == Color.EMPTY:
                move = cell
                break
        # And the chosen cell is empty but not adjacent
        assert board.check_position(move[0], move[1]) == Color.EMPTY
        assert move not in board.find_empty_adjacents(selected.position[0], selected.position[1])

        # Then the piece is not moved to the cell
        with pytest.raises(Exception) as result:
            game_manager.move_piece(move[0], move[1])
            
        assert board.check_position(move[0], move[1]) == Color.EMPTY
        # And the turn is unchanged
        assert game_manager.get_turn() == Color.BLACK
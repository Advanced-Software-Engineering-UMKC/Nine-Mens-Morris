import pytest
from backend.GameManager import GameManager

def test_acceptance_test_1_1():
    # Given the game is Nine Men’s Morris
    board_size = 7
    total_pieces = 9
    game_manager = GameManager(board_size, total_pieces)
    
    # When a new game is started
    board = game_manager.get_board()
    
    # Then there will be an empty 7x7 Nine Men’s Morris board
    assert len(board.board) == board_size
    assert len(board.board[0]) == board_size
    
    for row in board.board:
        for cell in row:
            assert cell.state == "empty"

if __name__ == '__main__':
    pytest.main()
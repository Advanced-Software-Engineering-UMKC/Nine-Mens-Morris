import pytest
from unittest.mock import Mock, patch
import pygame as pg
from backend.GameManager import GameManager
from frontend.BoardGUI import BoardGUI


@pytest.fixture
def board_gui_fixture():
    mock_game = Mock()
    mock_game.screen = Mock()
    
    # Mock Pygame image and transformation methods
    pg.image.load = Mock()
    pg.transform.smoothscale = Mock(return_value=Mock())
    
    board_size = 8
    win_size = 640
    total_pieces = 16
    
    board_gui = BoardGUI(mock_game, win_size, board_size, total_pieces)
    return board_gui, mock_game


def test_initialization(board_gui_fixture):
    board_gui, _ = board_gui_fixture
    assert board_gui.cell_size == board_gui.win_size // board_gui.board.board_size
    assert isinstance(board_gui.backend_game, GameManager)
    assert board_gui.count == 0


@patch('pygame.image.load')
@patch('pygame.transform.smoothscale')
def test_get_scaled_image(mock_smoothscale, mock_load, board_gui_fixture):
    board_gui, _ = board_gui_fixture
    mock_image = Mock()
    mock_load.return_value = mock_image
    mock_smoothscale.return_value = mock_image

    # Call the method with a mock path and resolution and assert the calls were made correctly
    path = 'resources/board/board.png'
    resolution = [100, 100]
    image = board_gui.get_scaled_image(path, resolution)

    mock_load.assert_called_once_with(path)
    mock_smoothscale.assert_called_once_with(mock_image.convert_alpha(), resolution)
    assert image == mock_image


@patch('pygame.mouse.get_pos', return_value=(100, 100))
@patch('pygame.mouse.get_pressed', return_value=(1, 0, 0))
def test_get_cell_clicked(mock_get_pressed, mock_get_pos, board_gui_fixture):
    board_gui, _ = board_gui_fixture
    cell = board_gui.get_cell_clicked()
    expected_cell = pg.Vector2(100, 100) // board_gui.cell_size
    assert cell == expected_cell
    mock_get_pos.assert_called_once()
    mock_get_pressed.assert_called_once()


def test_draw_piece(board_gui_fixture):
    board_gui, mock_game = board_gui_fixture
    position = (100, 100)

    # Test drawing a black piece
    board_gui.draw_piece('black', position)
    mock_game.screen.blit.assert_called_once_with(board_gui.black_piece_image, position)

    # Reset mock and test drawing a white piece
    mock_game.screen.blit.reset_mock()
    board_gui.draw_piece('white', position)
    mock_game.screen.blit.assert_called_once_with(board_gui.white_piece_image, position)


def test_draw_board(board_gui_fixture):
    board_gui, mock_game = board_gui_fixture
    board_gui.draw_board()
    mock_game.screen.blit.assert_called_once_with(board_gui.board_image, (0, 0))

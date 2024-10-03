import unittest
from unittest.mock import Mock, patch
import pygame as pg
from backend.GameManager import GameManager 
from frontend.BoardGUI import BoardGUI 


class TestBoardGUI(unittest.TestCase):
    def setUp(self):
       
        self.mock_game = Mock()
        self.mock_game.screen = Mock()
        
        pg.image.load = Mock()
        pg.transform.smoothscale = Mock(return_value=Mock()) 
       
        self.board_size = 8  
        self.win_size = 640  
        self.total_pieces = 16
        self.board_gui = BoardGUI(self.mock_game, self.win_size, self.board_size, self.total_pieces)

    def tearDown(self):
        # Auto cleanup done by unittest
        pass

    def test_initialization(self):
        self.assertEqual(self.board_gui.cell_size, self.win_size // self.board_size)
        self.assertIsInstance(self.board_gui.backend_game, GameManager)
        self.assertEqual(self.board_gui.count, 0)

    @patch('pygame.image.load')
    @patch('pygame.transform.smoothscale')
    def test_get_scaled_image(self, mock_smoothscale, mock_load):
        mock_image = Mock()
        mock_load.return_value = mock_image
        mock_smoothscale.return_value = mock_image

        # Call the method with a mock path and resolution and assert the calls were made correctly
        path = 'resources/board/board.png'
        resolution = [100, 100]
        image = self.board_gui.get_scaled_image(path, resolution)

        mock_load.assert_called_once_with(path)
        mock_smoothscale.assert_called_once_with(mock_image.convert_alpha(), resolution)
        self.assertEqual(image, mock_image)

    @patch('pygame.mouse.get_pos', return_value=(100, 100))
    @patch('pygame.mouse.get_pressed', return_value=(1, 0, 0))  
    def test_get_cell_clicked(self, mock_get_pressed, mock_get_pos):

        cell = self.board_gui.get_cell_clicked()
        expected_cell = pg.Vector2(100, 100) // self.board_gui.cell_size
        self.assertEqual(cell, expected_cell)
        mock_get_pos.assert_called_once()
        mock_get_pressed.assert_called_once()

    def test_draw_piece(self):
 
        position = (100, 100)
        self.board_gui.draw_piece('black', position)
        self.mock_game.screen.blit.assert_called_once_with(self.board_gui.black_piece_image, position)

        self.mock_game.screen.blit.reset_mock()  
        self.board_gui.draw_piece('white', position)
        self.mock_game.screen.blit.assert_called_once_with(self.board_gui.white_piece_image, position)

    def test_draw_board(self):
        self.board_gui.draw_board()
        self.mock_game.screen.blit.assert_called_once_with(self.board_gui.board_image, (0, 0))


if __name__ == '__main__':
    unittest.main()

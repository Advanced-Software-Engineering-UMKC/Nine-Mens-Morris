import unittest
from unittest.mock import patch, MagicMock
# from GameGUI import GameGUI

class testGameGUI(unittest.TestCase):

    def setUp(self):
        pass


    # @patch('module.ClassName.method_name')
    def test_first(self):
        self.assertEqual(1, 2)

    # @patch('GameGUI.pg.display.update')
    # @patch('GameGUI.GameGUI.check_events')
    # @patch('GameGUI.GameGUI.clock')
    # @patch('GameGUI.GameGUI.board')
    # def test_run_game(self, mock_board, mock_clock, mock_check_events, mock_pg_update):
    #     # Create an instance of the GameGUI class
    #     game_gui = GameGUI()

    #     # Set up the mocks
    #     mock_check_events.side_effect = [None, Exception("Stop Loop")]  # Stop the loop after one iteration
    #     mock_clock.tick.side_effect = [None]
    #     mock_board.build_board.side_effect = [None]

    #     # Run the method
    #     with self.assertRaises(Exception) as context:
    #         game_gui.run_game()

    #     # Verify the method calls
    #     mock_check_events.assert_called()
    #     mock_pg_update.assert_called()
    #     mock_clock.tick.assert_called_with(60)
    #     mock_board.build_board.assert_called()

    #     # Verify the loop was stopped by the exception
    #     self.assertEqual(str(context.exception), "Stop Loop")

if __name__ == '__main__':
    unittest.main()
import pygame as pg
import time


from backend.Board import Board
from backend.Cell import Color
import sys
vec2 = pg.math.Vector2 


class BoardGUI:
    def __init__(self, game, WIN_SIZE, board_size, game_manager):
        self.game = game
        self.board_image = self.get_scaled_image(
            "resources/board/board.png", [WIN_SIZE] * 2
        )
        self.cell_size = WIN_SIZE // board_size
        self.black_piece_image = self.get_scaled_image(
            "resources/pieces/black_piece.png", [self.cell_size] * 2
        )
        self.white_piece_image = self.get_scaled_image(
            "resources/pieces/white_piece.png", [self.cell_size] * 2
        )
        self.game_manager = None
        self.board = None
        self.count = 0
        self.win_size = WIN_SIZE
        self.game_manager = game_manager
        self.board = game_manager.board

    def draw_board(self):
        self.game.screen.blit(self.board_image, (0, 0))
        # Draw all pieces currently on the board
        for position, turn in self.board.pieces_on_board.items():
            self.draw_piece(turn, (position[1] * self.cell_size, position[0] * self.cell_size))


    @staticmethod
    def get_scaled_image(path, resolution):
        image = pg.image.load(path)
        return pg.transform.smoothscale(image.convert_alpha(), resolution)

    def build_board(self):
        self.draw_board()

    def draw_piece(self, turn, position):
        if turn == Color.BLACK:
            self.game.screen.blit(self.black_piece_image, position)
        else:
            self.game.screen.blit(self.white_piece_image, position)

    def remove_piece_from_board(self,row, col):
        if (row, col) in self.game_manager.removable_pieces:
            # THIS IS A TEMPORARY PATCH. PLEASE DEBUG NEXT SPRINT
            self.game_manager.end_turn()
            # Valid piece selected to remove
            print(f"Removing opponent's piece at ({row}, {col})")
            self.board.remove_piece(row, col)  # Remove the piece from the board
            self.draw_board()  # Redraw the board after removal
            status = self.game_manager.remove_piece_mill(row, col)
            if status:
                print(f"Removed opponent's piece at ({row}, {col})")
                # THIS IS A TEMPORARY PATCH. PLEASE DEBUG NEXT SPRINT
                if self.game_manager.check_game_over():
                    print('Game Over winner is',self.game_manager.check_game_over())
                    sys.exit()
                self.game_manager.end_turn()
        else:
            print(f"Invalid selection. Please select a piece from: {self.game_manager.removable_pieces}")
    
    def handle_moment_phase(self,row, col):
        if self.game_manager.selected_piece is None:
            # No piece selected, attempt to select a piece
            piece_at_cell = self.game_manager.get_piece_at(row, col)
            if piece_at_cell and piece_at_cell.get_state().name == self.game_manager.turn.name:
                # Only allow selection if the piece belongs to the current player's turn
                self.game_manager.selected_piece = (row, col)
                print(f"Piece selected at ({row}, {col})")
            else:
                print("Cannot select piece: not current player's turn or empty cell")
        else:
            # A piece is already selected, attempt to move it
            selected_row, selected_col = self.game_manager.selected_piece

            # Check if the move is valid (adjacent and empty)
            try:
                # Move the piece to the new location
                move_success = self.game_manager.move_piece(row, col)
                if move_success:
                    print(f"Piece moved to ({row}, {col})")
                    # # Remove the piece from the old position
                    # self.board.remove_piece(selected_row, selected_col)

                    # # Add the piece to the new position
                    # self.board.pieces_on_board[(row, col)] = self.game_manager.turn
                    self.draw_board()  # Redraw board to show updated pieces

                    # Check if the move forms a mill
                    if self.game_manager.is_mill_formed(row, col):
                        print("Mill formed! Remove opponent's piece.")
                        self.game_manager.remove_opponent_piece()

                    self.game_manager.end_turn()  # End turn after successful move
                else:
                    print(f"Invalid move to ({row}, {col})")
            except Exception as e:
                print(e)

            # Clear the selected piece regardless of move success
            self.game_manager.selected_piece = None
    
    
    def get_cell_clicked(self):
        current_cell = vec2(pg.mouse.get_pos()) // self.cell_size
        col, row = map(int, current_cell)
        mouse_buttons = pg.mouse.get_pressed()
        self.count += 1

        # Handle opponent's piece removal if mill is formed
        if self.game_manager.waiting_for_removal:
            if mouse_buttons[0]:
                self.remove_piece_from_board(row , col)
            return current_cell

        # Left click - Select or move piece
        if mouse_buttons[0]:
            if not self.game_manager.placement_complete():
                # Handle piece placement
                self.game_manager.handle_piece_placement(row, col)
                self.draw_board()
                return current_cell  # Return the current cell for left click
            else:
                # Movement phase
                self.handle_moment_phase(row , col)
            
            if self.game_manager.check_game_over():
                print('Game Over winner is',self.game_manager.check_game_over())
                sys.exit()
                

        # Right click - Deselect piece
        if mouse_buttons[2]:
            if self.game_manager.selected_piece:
                print(f"Deselected piece at {self.game_manager.selected_piece}")
                self.game_manager.selected_piece = None

        return None
    
    def handle_computer_move(self): 
        if self.game_manager.waiting_for_removal:
            return
        self.game_manager.handle_computer_turn()
        time.sleep(0.3)
        self.draw_board()
        if self.game_manager.placement_complete():
            if self.game_manager.check_game_over():
                    print('Game Over winner is',self.game_manager.check_game_over())
                    sys.exit()
            self.game_manager.end_turn()



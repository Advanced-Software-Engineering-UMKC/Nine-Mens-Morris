import pygame as pg

from backend.Board import Board
from backend.Cell import Color

vec2 = pg.math.Vector2 


class BoardGUI:
    def __init__(self, game, WIN_SIZE, board_size, total_pieces, gameManager):
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
        self.game_manager = gameManager
        self.board = Board(board_size)
        self.count = 0
        self.win_size = WIN_SIZE
        self.pieces_on_board = {}

    def draw_board(self):
        self.game.screen.blit(self.board_image, (0, 0))
        # Draw all pieces currently on the board
        for position, turn in self.pieces_on_board.items():
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

    def remove_piece(self, row, col):
        # Remove the piece from the internal structure
        if (row, col) in self.pieces_on_board:
            del self.pieces_on_board[(row, col)]

    
    def get_cell_clicked(self):
        current_cell = vec2(pg.mouse.get_pos()) // self.cell_size
        col, row = map(int, current_cell)
        mouse_buttons = pg.mouse.get_pressed()
        self.count += 1

        # Left click - Select or move piece
        if mouse_buttons[0]:
            if not self.game_manager.placement_complete():
                # Handle piece placement
                is_piece_placed = self.game_manager.place_piece(row, col)
                if is_piece_placed == 1:
                    self.pieces_on_board[(row, col)] = self.game_manager.get_turn()  # Add piece to the board
                    self.draw_board()  # Redraw board to show new piece
                    self.game_manager.end_turn()  # End turn after placing a piece
                return current_cell  # Return the current cell for left click

            else:
                # Movement phase
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
                    if self.game_manager.is_adjacent_and_empty(selected_row, selected_col, row, col):
                        # Move the piece to the new location
                        move_success = self.game_manager.move_piece(row, col)
                        if move_success:
                            print(f"Piece moved to ({row}, {col})")
                            # Remove the piece from the old position
                            self.remove_piece(selected_row, selected_col)
                            # Add the piece to the new position
                            self.pieces_on_board[(row, col)] = self.game_manager.turn
                            self.draw_board()  # Redraw board to show updated pieces
                            self.game_manager.end_turn()  # End turn after successful move
                        else:
                            print(f"Invalid move to ({row}, {col})")
                    else:
                        print(f"Cell ({row}, {col}) is not adjacent or not empty")

                    # Clear the selected piece regardless of move success
                    self.game_manager.selected_piece = None

        # Right click - Deselect piece
        if mouse_buttons[2]:
            if self.game_manager.selected_piece:
                print(f"Deselected piece at {self.game_manager.selected_piece}")
                self.game_manager.selected_piece = None

        return None
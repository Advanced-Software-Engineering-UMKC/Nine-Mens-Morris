# import pygame as pg
from backend.Board import Board
from backend.Piece import Pieces
from backend.Cell import Color


class GameManager:
    def __init__(self, size, pieces):
        self.board = Board(size)
        self.pieces = Pieces(pieces)
        self.turn = Color.WHITE
        self.selected_piece = None
        self.open_moves = self.board.get_valid_moves()

        # Mill variables
        self.mills = [
            [(0, 0), (0, 3), (0, 6)],  # Horizontal mills
            [(1, 1), (1, 3), (1, 5)],
            [(2, 2), (2, 3), (2, 4)],
            [(3, 0), (3, 1), (3, 2)],
            [(3, 4), (3, 5), (3, 6)],
            [(4, 2), (4, 3), (4, 4)],
            [(5, 1), (5, 3), (5, 5)],
            [(6, 0), (6, 3), (6, 6)],

            # Vertical mills
            [(0, 0), (3, 0), (6, 0)],
            [(1, 1), (3, 1), (5, 1)],
            [(2, 2), (4, 2), (5, 2)],
            [(0, 3), (1, 3), (2, 3)],
            [(4, 3), (5, 3), (6, 3)],
            [(2, 4), (4, 4), (5, 4)],
            [(1, 5), (3, 5), (5, 5)],
            [(0, 6), (3, 6), (6, 6)]
        ]
        self.waiting_for_removal = False
        self.removable_pieces = []

    def get_board(self, row=-1, col=-1):
        if row == -1 or col == -1:
            return self.board
        return self.board.check_position(row, col)

    def get_turn(self):
        return self.turn

    def get_turn_as_string(self):
        return self.turn.name.lower()

    def placement_complete(self):
        return self.pieces.all_pieces_placed()

    def place_piece(self, row, column):
        if (row, column) in self.open_moves:
            if self.board.check_position(row, column) != Color.EMPTY:
                print(self.board.check_position(row, column))
                return "GameManagerError -- position not empty"

            is_piece_placed = 0
            if self.turn == Color.WHITE:
                is_piece_placed = self.pieces.set_white_piece(row, column)
            else:
                is_piece_placed = self.pieces.set_black_piece(row, column)

            if is_piece_placed == 1:
                self.board.set_position(row, column, self.turn.name.lower())
                self.open_moves.remove((row, column))
                return 1
            # else error -- figure out handling. are we making error classes?
            return 0

        else:
            return "GameManagerError -- invalid piece placement position"

    # function for getting the current amount of pieces left to be placed
    def get_pieces_left(self):
        # dictionary for black and white pieces left to be placed
        return {
            "white": self.pieces.size - self.pieces.count_white_placed,
            "black": self.pieces.size - self.pieces.count_black_placed,
        }

    def end_turn(self):
        self.turn = Color.swap_turn(self.turn)
        return 1

    def is_adjacent(self, current_row, current_col, target_row, target_col):
        """ Check if the target position is adjacent to the current position """
        return (target_row, target_col) in self.board.adjacent_positions_map.get((current_row, current_col), [])

    def is_empty(self, row, col):
        """ Check if the cell at (row, col) is empty """
        return self.board.board[row][col] is None

    def is_adjacent_and_empty(self, current_row, current_col, target_row, target_col):
        """ Check if the target cell is adjacent to the current cell and is empty """
        if self.is_adjacent(current_row, current_col, target_row, target_col):
            if (target_row, target_col) in self.open_moves:
                return True
        return False

    def find_empty_adjacents(self, row, col):
        empty_adjacent_positions = []
        all_adjacent_positions = self.board.adjacent_positions_map[(row, col)]

        for row, col in all_adjacent_positions:
            position_state = self.board.check_position(row, col)
            if position_state == Color.EMPTY or position_state == Color.VOID:
                empty_adjacent_positions.append((row, col))

        return empty_adjacent_positions

    def can_fly(self, player):
        can_fly = False
        if player == Color.WHITE and self.pieces.count_white_remains == 3:
            can_fly = True
        elif player == Color.BLACK and self.pieces.count_black_remains == 3:
            can_fly = True
        return can_fly

    def get_movable_options(self, row, col):
        # calculate the available adjacent positions
        if self.can_fly(self.turn):
            # if can fly, return all open positions
            return self.open_moves
        else:
            # if more than 3 pieces left, user can only move to empty adjacent positions
            return self.find_empty_adjacents(row, col)

    # Returns winner if game is over, or None
    def check_game_over(self):
        my_pieces = []

        # Check if opponent has 2 pieces left, if so then current player wins
        if self.pieces.all_pieces_placed():
            if self.turn == Color.WHITE:
                if self.pieces.count_black_remains == 2:
                    return self.turn
                my_pieces = self.pieces.white_pieces
            elif self.turn == Color.BLACK:
                if self.pieces.count_white_remains == 2:
                    return self.turn
                my_pieces = self.pieces.black_pieces

            # Check if the current player don't have any valid movable options
            for piece in my_pieces:
                movable_options = self.get_movable_options(piece.position[0], piece.position[1])
                if movable_options is not None and len(movable_options) > 0:
                    # At-least found one movable option
                    return None
        else:
            return None

        # Return opponent as Winner
        return Color.BLACK if self.get_turn() == Color.WHITE else Color.WHITE

    '''
    the select_piece func should return the available empty adjacent positions to where the piece can be moved 
    or throw exception if it should be selectable
    '''
    def select_piece(self, row, col):
        if not self.placement_complete():
            raise Exception("SelectionError -- Cannot select pieces during placement phase")

        cell = self.board.get_cell(row, col)
        self.selected_piece = (row, col)

        if self.turn == cell.get_state():
            return self.get_movable_options(row, col)

        self.selected_piece = None
        raise Exception("SelectionError -- Invalid piece selection")

    def move_piece(self, target_row, target_col):
        if not self.selected_piece:
            raise Exception("MoveError -- No piece selected")

        start_row, start_col = self.selected_piece

        # Validate the target position is empty and adjacent
        if self.board.check_position(target_row, target_col) != Color.EMPTY:
            raise Exception("MoveError -- Target position is not empty")

        if not self.can_fly(self.turn):
            if not self.is_adjacent_and_empty(start_row, start_col, target_row, target_col):
                raise Exception("MoveError -- Invalid move, pieces can only move to adjacent positions")

        # Perform the move
        self.board.set_position(target_row, target_col, self.turn.name.lower())
        self.board.set_position(start_row, start_col, Color.EMPTY)
        # self.board.board[start_row][start_col] = None

        # removing the new position from open move and adding the previous position to it
        self.open_moves.append((start_row, start_col))
        self.open_moves.remove((target_row, target_col))

        self.selected_piece = None
        return True

    def get_piece_at(self, row, col):
        return self.board.board[row][col]

        # def is_mill_formed(self, row, col, turn):

    #     for mill in self.mills:
    #         if (row, col) in mill:
    #             # Check if all three positions in this mill belong to the current player
    #             first = self.get_piece_at(r, c)

    #             if all(self.get_piece_at(r, c) == turn for r, c in mill):
    #                 return True
    #     return False

    def is_mill_formed(self, row, col):
        for mill in self.mills:
            if (row, col) in mill:
                # Create an empty list to store comparison results
                pieces_in_mill = []

                # Loop through each position in the mill
                for r, c in mill:
                    piece_at_position = self.get_piece_at(r, c)  # Get the piece at the mill position
                    is_current_turn_piece = (
                                piece_at_position.get_state().name == self.get_turn().name)  # Check if it's the current player's turn
                    pieces_in_mill.append(is_current_turn_piece)  # Append the result (True/False) to the list

                # Now use 'all' to check if all the values in the list are True
                if all(pieces_in_mill):
                    return True

        return False

    def remove_piece_mill(self, row, col):
        self.open_moves.append((row, col))
        self.board.set_position(row, col, Color.EMPTY)

        if self.turn == Color.WHITE:
            self.pieces.decrease_black_piece_count()
        else:
            self.pieces.decrease_white_piece_count()

        self.waiting_for_removal = False  # Reset the removal state
        self.removable_pieces = []  # Clear the list of removable pieces
        self.end_turn()  # End the turn after removal
        self.end_turn()  # swap the turn to opponent
        return True

    def remove_opponent_piece(self, pieces_on_board):
        opponent_turn = Color.BLACK if self.get_turn() == Color.WHITE else Color.WHITE

        # Get all opponent's pieces
        opponent_pieces = [
            (row, col) for (row, col), piece_turn in pieces_on_board.items()
            if piece_turn == opponent_turn
        ]

        # Try to remove non-mill pieces first - logic is wrong but it works as user select write piece
        opponent_pieces_non_mill = [(row, col) for row, col in opponent_pieces if not self.is_mill_formed(row, col)]

        if opponent_pieces_non_mill:
            print('Select a piece to remove from these non-mill options: ', opponent_pieces_non_mill)
            self.waiting_for_removal = True
            self.removable_pieces = opponent_pieces_non_mill
            return True

        # If no non-mill pieces, remove a mill piece
        if opponent_pieces and not opponent_pieces_non_mill:
            print('All opponent pieces are in mills. Select one to remove: ', opponent_pieces)
            self.waiting_for_removal = True
            self.removable_pieces = opponent_pieces
            return True

        if opponent_pieces:
            print('you can only select non mill peices sice opponent has it...')

        return False

    def handle_piece_placement(self, row, col, pieces_on_board):
        is_piece_placed = self.place_piece(row, col)
        if is_piece_placed == 1:
            pieces_on_board[(row, col)] = self.get_turn()  # Add piece to the board
            # self.draw_board()  

            # Check if the piece forms a mill
            if self.is_mill_formed(row, col):
                print("Mill formed! Remove opponent's piece.")
                self.remove_opponent_piece(pieces_on_board)

            self.end_turn()

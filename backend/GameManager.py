# import pygame as pg
import uuid

from backend.Board import Board
from backend.Cell import Color
from backend.Player import Player
from backend.ComputerPlayer import ComputerPlayer
import json
import os

history_path = 'resources/history/'  # change file name every time if want to record new game


class GameManager:
    def __init__(self, size, pieces):
        self.id = str(uuid.uuid4())
        self.board = Board(size, pieces)
        self.player_1 = Player(pieces, Color.WHITE)
        self.player_2 = Player(pieces, Color.BLACK)
        self.human_player = Player(pieces, Color.WHITE)
        self.computer_player = ComputerPlayer(pieces, Color.BLACK)
        self.turn = Color.WHITE
        self.selected_piece = None
        self.open_moves = self.board.get_valid_moves()
        self.use_computer_opponent = False
        self.move_history = []
        self.saved = False

        # Mill variables
        self.mills = self.gen_mill_list()
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
    
    def get_game_type(self):
        return self.board.board_info["type"]

    def placement_complete(self):
        return self.get_current_player().all_of_players_pieces_placed() and \
               self.get_opponent().all_of_players_pieces_placed()
    
    def gen_mill_list(self):
        mills = []
        row_size = self.board.board_info["row_size"]

        # intramills
        for offset in range(row_size, 0, -1):
            ini = row_size - offset
            sec = ini + offset
            thi = ini + offset*2

            mills.append([(ini, ini), (ini, sec), (ini, thi)])
            mills.append([(thi, ini), (thi, sec), (thi, thi)])

            mills.append([(ini, ini), (sec, ini), (thi, ini)])
            mills.append([(ini, thi), (sec, thi), (thi, thi)])
        
        # intermills, if applicable
        if row_size > 2:
            ini = 0
            mid = row_size
            fin = self.board.board_info["size"]

            mills.append([(mid, ini), (mid, ini+1), (mid, ini+2)])
            mills.append([(mid, fin-mid), (mid, fin-mid+1), (mid, fin-mid+2)])

            mills.append([(ini, mid), (ini+1, mid), (ini+2, mid)])
            mills.append([(fin-mid, mid), (fin-mid+1, mid), (fin-mid+2, mid)])

        
        # diagonals, if applicable
        if self.board.board_info["diagonals"]:
            ini = 0
            fin = row_size*2

            mills.append([(ini, ini), (ini+1, ini+1), (ini+2, ini+2)])
            mills.append([(fin, fin), (fin-1, fin-1), (fin-2, fin-2)])

            mills.append([(ini, fin), (ini+1, fin-1), (ini+2, fin-2)])
            mills.append([(fin, ini), (fin-1, ini+1), (fin-2, ini+2)])

        return mills
    
    def place_piece(self, row, column):
        if (row, column) in self.open_moves:
            if self.board.check_position(row, column) != Color.EMPTY:
                print(self.board.check_position(row, column))
                return "GameManagerError -- position not empty"

            self.move_history.append({
                'action': 'place',
                'player': self.turn.name,
                'position': (row, column)
            })

            is_piece_placed = 0
            current_player = self.get_current_player()
            is_piece_placed = current_player.set_players_piece(row, column)

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
            "white": self.player_1.starting_piece_count - self.player_1.pieces_placed,
            "black": self.player_2.starting_piece_count - self.player_2.pieces_placed,
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
    
    def can_fly(self, player):
        if len(player.pieces) == 3:
            return True
    
    def get_current_player(self):
        if self.turn == Color.WHITE:
            return self.player_1
        else:
            return self.player_2
        
    def get_opponent(self):
        if self.turn == Color.WHITE:
            return self.player_2
        else:
            return self.player_1

    # Returns winner if game is over, or None
    def check_game_over(self):
        current_player_pieces = []
        current_player = self.get_current_player()
        opponent = self.get_opponent()

        if self.placement_complete():
            if len(opponent.pieces) == 2:
                if not self.saved:
                    self.save_history_to_json(history_path)
                    self.saved = True
                return self.turn
            current_player_pieces = current_player.pieces

            # Check if the current player don't have any valid movable options
            for piece in current_player_pieces:
                movable_options = self.board.get_movable_options(piece.position[0], piece.position[1], self.can_fly(current_player))
                if movable_options is not None and len(movable_options) > 0:
                    # At-least found one movable option
                    return None
        else:
            return None

        if not self.saved:
            self.save_history_to_json(history_path)
            self.saved = True
        return self.get_opponent().get_color()

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
            return self.board.get_movable_options(row, col, self.can_fly(self.get_current_player()))

        self.selected_piece = None
        raise Exception("SelectionError -- Invalid piece selection")

    def move_piece(self, target_row, target_col):
        if not self.selected_piece:
            raise Exception("MoveError -- No piece selected")

        start_row, start_col = self.selected_piece

        # Validate the target position is empty and adjacent
        if self.board.check_position(target_row, target_col) != Color.EMPTY:
            raise Exception("MoveError -- Target position is not empty")

        if not self.can_fly(self.get_current_player()):
            if not self.is_adjacent_and_empty(start_row, start_col, target_row, target_col):
                raise Exception("MoveError -- Invalid move, pieces can only move to adjacent positions")

        self.move_history.append({
            'action': 'move',
            'player': self.turn.name,
            'from_position': (start_row, start_col),
            'to_position': (target_row, target_col)
        })

        # Perform the move
        self.board.set_position(target_row, target_col, self.turn.name.lower())
        self.board.set_position(start_row, start_col, Color.EMPTY)

        # update piece position in the player object
        current_player = self.get_current_player()
        for piece in current_player.pieces:
            if piece.position == (start_row, start_col):
                piece.set_position((target_row, target_col))
                break

        # self.board.board[start_row][start_col] = None

        # removing the new position from open move and adding the previous position to it
        self.open_moves.append((start_row, start_col))
        self.open_moves.remove((target_row, target_col))

        self.selected_piece = None

                # Remove the piece from the old position
        self.board.remove_piece(start_row, start_col)

        # Add the piece to the new position
        self.board.pieces_on_board[(target_row, target_col)] = self.turn
        return True

    def get_piece_at(self, row, col):
        return self.board.board[row][col]

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

    def does_opp_mill_exist(self, row, col):
        opponent_turn = Color.BLACK if self.get_turn() == Color.WHITE else Color.WHITE
        for mill in self.mills:
            if (row, col) in mill:
                # Create an empty list to store comparison results
                pieces_in_mill = []

                # Loop through each position in the mill
                for r, c in mill:
                    piece_at_position = self.get_piece_at(r, c)  # Get the piece at the mill position
                    is_current_turn_piece = (
                            piece_at_position.get_state().name == opponent_turn.name)  # Check if it's the current player's turn
                    pieces_in_mill.append(is_current_turn_piece)  # Append the result (True/False) to the list

                # Now use 'all' to check if all the values in the list are True
                if all(pieces_in_mill):
                    return True

        return False

    def remove_piece_mill(self, row, col):
        self.open_moves.append((row, col))
        self.board.set_position(row, col, Color.EMPTY)
        opponent = self.get_opponent()

        opponent.remove_piece(row, col)

        self.move_history.append({
            'action': 'remove',
            'player': self.turn.name,
            'position': (row, col)}
        )

        self.waiting_for_removal = False  # Reset the removal state
        self.removable_pieces = []  # Clear the list of removable pieces
        self.end_turn()  # End the turn after removal
        self.end_turn()  # swap the turn to opponent
        return True

    def remove_opponent_piece(self):
        # Get all opponent's pieces
        opponent_pieces = self.get_opponent().get_placed_pieces_position()
        # opponent_pieces = [
        #     (row, col) for (row, col), piece_turn in self.board.pieces_on_board.items()
        #     if piece_turn == opponent_turn
        # ]

        # Try to remove non-mill pieces first - logic is wrong but it works as user select write piece
        opponent_pieces_non_mill = [(row, col) for row, col in opponent_pieces if
                                    not self.does_opp_mill_exist(row, col)]

        # set self.removable_pieces to opponent_pieces_non_mill if its not empty else opponent_pieces
        self.removable_pieces = opponent_pieces_non_mill if opponent_pieces_non_mill else opponent_pieces

        if self.use_computer_opponent and self.player_2.color == self.turn:
            piece_to_remove = self.player_2.decide_piece_to_remove(self.removable_pieces, self.board, self.mills)
            self.board.remove_piece(piece_to_remove[0], piece_to_remove[1])
            self.player_1.remove_piece(piece_to_remove[0], piece_to_remove[1])
            self.open_moves.append((piece_to_remove[0], piece_to_remove[1]))
            self.board.set_position(piece_to_remove[0], piece_to_remove[1], Color.EMPTY)
            self.removable_pieces = []
            return True

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

    def handle_piece_placement(self, row, col):
        is_piece_placed = self.place_piece(row, col)
        if is_piece_placed == 1:


            self.board.pieces_on_board[(row, col)] = self.get_turn()  # Add piece to the board
            # self.draw_board()  

            # Check if the piece forms a mill
            if self.is_mill_formed(row, col):
                print("Mill formed! Remove opponent's piece.")
                self.remove_opponent_piece()
                # if self.use_computer_opponent and self.get_turn() == Color.WHITE or not self.use_computer_opponent:
                #     self.remove_opponent_piece()
                

            self.end_turn()

    def set_use_computer_opponent(self, use_computer_opponent):
        self.use_computer_opponent = use_computer_opponent
        self.player_2 = ComputerPlayer(self.player_2.starting_piece_count, Color.BLACK)

    def handle_computer_turn(self):
        if self.check_game_over():
            return
        elif self.placement_complete():
            self.selected_piece, open_moves = self.player_2.decide_piece_to_move(self.mills, self.board, self.can_fly(self.get_current_player()))
            # while len(open_moves) == 0:
            #     self.selected_piece = self.player_2.decide_piece_to_move(self.mills, self.board)
            #     open_moves = self.board.get_movable_options(self.selected_piece[0], self.selected_piece[1], self.can_fly(self.get_current_player()))
            target_cell = self.player_2.decide_move_target(self.mills, open_moves, self.board)
            self.selected_piece = self.selected_piece.position
            print(f"Computer moving piece from {self.selected_piece} to {target_cell}")
            self.move_piece(target_cell[0], target_cell[1])
            self.selected_piece = None
            if self.is_mill_formed(target_cell[0], target_cell[1]):
                        print("Mill formed! Remove opponent's piece.")
                        self.remove_opponent_piece()
            self.end_turn()
            return
        else:
            selected_piece = self.player_2.decide_piece_placement(self.open_moves, self.mills, self.board)
            self.handle_piece_placement(selected_piece[0], selected_piece[1])
            
    def save_history_to_json(self, file_path):
        # Ensure the directory exists
        file_path = file_path + 'game_history_' + self.id + '.json'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as file:
            json.dump(self.move_history, file, indent=4)

        print(f"Game history saved to {file_path}")

        return file_path

    def delete_history_file(self, file_path):
        file_path = file_path + 'game_history_' + self.id + '.json'
        if os.path.exists(file_path):
            os.remove(file_path)

    def load_history(self, file_path):
        """Load the game history from a JSON file."""
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        return None

    def validate_history_data(self, history_data):
        # Define the expected keys for each action type
        valid_structure = {
            "place": {"required_keys": {"action", "player", "position"}, "optional_keys": set()},
            "remove": {"required_keys": {"action", "player", "position"}, "optional_keys": set()},
            "move": {"required_keys": {"action", "player", "from_position", "to_position"}, "optional_keys": set()},
        }

        try:
            # Check if the root is an array
            if not isinstance(history_data, list):
                return False, "The root element is not an array."

            if len(history_data) == 0:
                return False, f"Empty history"

            # Validate each object in the array
            for obj in history_data:
                if not isinstance(obj, dict):
                    return False, "Array contains non-object elements."

                # Check if 'action' is a valid key
                action = obj.get("action")
                if action not in valid_structure:
                    return False, f"Invalid action '{action}' in object: {obj}"

                # Validate required and optional keys
                required_keys = valid_structure[action]["required_keys"]
                optional_keys = valid_structure[action]["optional_keys"]
                actual_keys = set(obj.keys())

                missing_keys = required_keys - actual_keys
                extra_keys = actual_keys - (required_keys | optional_keys)

                if missing_keys:
                    return False, f"Missing keys {missing_keys} in object: {obj}"
                if extra_keys:
                    return False, f"Unexpected keys {extra_keys} in object: {obj}"

                # Validate the 'player' field
                if obj["player"] not in {"WHITE", "BLACK"}:
                    return False, f"Invalid player '{obj['player']}' in object: {obj}"

                # Validate positions are lists of two integers
                for key in {"position", "from_position", "to_position"} & actual_keys:
                    if not (isinstance(obj[key], list) and len(obj[key]) == 2 and all(
                            isinstance(x, int) for x in obj[key])):
                        return False, f"Invalid format for {key} in object: {obj}"

            # If all checks pass
            return True, "JSON content is valid."

        except json.JSONDecodeError as e:
            return False, f"Invalid JSON format: {e}"
        except Exception as e:
            return False, f"An error occurred: {e}"

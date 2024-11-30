import random
from backend.Player import Player
from backend.Piece import Color

class ComputerPlayer(Player):
    def __init__(self, max_piece_count, color):
        super().__init__(max_piece_count, color)

    def decide_piece_placement(self, valid_moves, possible_mills, current_board):
        chosen_position = self.attempt_to_find_mill(possible_mills, valid_moves, current_board)
        if chosen_position is None:
            chosen_position = random.choice(valid_moves)
        else:
            chosen_position = chosen_position
            # chosen_position = (chosen_position[1], chosen_position[0])  # For some reason the check in GameManager.place_piece() is reversed
        return chosen_position

    def decide_piece_to_move(self, possible_mills, current_board, can_fly):
        # if piece is not in possible_mills then move it else random
        # we need to find the mills that have computer pieces in them, dont use pieces in these mills if we can
        chosen_position = None
        for piece in self.pieces:
            chosen_position = self.attempt_to_find_mill(possible_mills, [piece.position], current_board)
            if chosen_position is not None:
                open_moves = current_board.get_movable_options(chosen_position[0], chosen_position[1], can_fly)
                if len(open_moves) > 0:
                    chosen_position = piece
                    return chosen_position, open_moves
            else:
                chosen_position = piece
                open_moves = current_board.get_movable_options(piece.position[0], piece.position[1], can_fly)      
        return chosen_position, open_moves
    
    def share_no_values(self, array1, array2):
        set1 = set(array1)
        set2 = set(array2)
        return set1.isdisjoint(set2)

    def decide_move_target(self, possible_mills, valid_moves, current_board):
        chosen_position = self.attempt_to_find_mill(possible_mills, valid_moves, current_board)
        if chosen_position is None:
            chosen_position = random.choice(valid_moves)
        else:
            chosen_position = chosen_position
        return chosen_position
    
    def attempt_to_find_mill(self, possible_mills, valid_moves, current_board):
        # add to piece_to_check the pieces that positions is not (-1, -1)
        active_pieces_to_evaluate = [piece.position for piece in self.pieces if piece.position != (-1, -1)]

        # pieces_to_check should be the available positions to place a piece
        valid_move = None

        for placed_piece in active_pieces_to_evaluate:
            mill_index, inner_array = self.find_piece_in_mill(possible_mills, placed_piece)
            if mill_index is not None:
                # if opponents pieces are in this mill then dont place piece in this mill
                active_pieces_to_evaluate.remove(placed_piece)
                if self.check_if_any_other_piece_is_in_mill(inner_array, current_board):
                    return self.find_open_position_in_mill(possible_mills[mill_index], valid_moves)
                else:
                    valid_move = None
        return valid_move
    
    def find_piece_in_mill(self, possible_mills, piece):
        for outer_index, inner_array in enumerate(possible_mills):
            if piece in inner_array:
                return outer_index, inner_array
        return None
    
    def check_if_any_other_piece_is_in_mill(self, inner_array, current_board):
        no_white_pieces_and_black_piece_exists = False
        black_piece_found = False
        for piece in inner_array:
            piece_color = current_board.check_position(piece[0], piece[1])
            if piece_color == Color.WHITE:
                return False
            elif piece_color == Color.BLACK:
                if black_piece_found:
                    return True
                black_piece_found = True
            no_white_pieces_and_black_piece_exists = True
        return no_white_pieces_and_black_piece_exists
                

    def find_open_position_in_mill(self, mill, valid_moves):
        for valid_move in valid_moves:
            if valid_move in mill:
                return valid_move
        return None
    
    def decide_piece_to_remove(self, opponent_pieces, board, mills):
        random_piece = random.choice(opponent_pieces)
        return random_piece
    

    def are_other_computer_pieces_in_mill(self, inner_array, current_board):
        other_black_pieces_in_mill = False
        for piece in inner_array:
            piece_color = current_board.check_position(piece[0], piece[1])
            if piece_color == Color.BLACK:
                other_black_pieces_in_mill = True
        return other_black_pieces_in_mill
    
    def other_pieces_in_mill(self, inner_array, current_board):
        open_positions = []
        black_pieces_in_mill = []
        for piece in inner_array:
            if current_board.check_position(piece[0], piece[1]) == Color.EMPTY:
                open_positions.append(piece)
            elif current_board.check_position(piece[0], piece[1]) == Color.BLACK:
                black_pieces_in_mill.append(piece)
        return open_positions, black_pieces_in_mill
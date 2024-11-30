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

    def decide_piece_to_move(self, possible_mills, current_board):
        # if piece is not in possible_mills then move it else random
        # we need to find the mills that have computer pieces in them, dont use pieces in these mills if we can
        pieces_in_mills = []
        chosen_position = None
        for piece in self.pieces:
            chosen_position = self.attempt_to_find_mill(possible_mills, [piece.position], current_board)
            if chosen_position is not None:
                return chosen_position
            # mill_index, found_mill_with_piece = self.find_piece_in_mill(possible_mills, piece.position)

            # pieces_in_mills.append(piece)
            # computers_pieces_minus_the_one_found = [piece_2.position for piece_2 in self.pieces if piece_2 not in pieces_in_mills]
            # if self.share_no_values(computers_pieces_minus_the_one_found, found_mill_with_piece):
            #     return piece
            # pieces_in_mills.remove(piece)
        if chosen_position is None:
            chosen_position = random.choice(self.pieces)
        return chosen_position
    
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
        for piece in inner_array:
            if current_board.check_position(piece[0], piece[1]) == Color.WHITE:
                return False
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
import random
from backend.Player import Player

class ComputerPlayer(Player):
    def __init__(self, max_piece_count, color):
        super().__init__(max_piece_count, color)

    def decide_piece_placement(self, valid_moves, possible_mills):
        chosen_position = self.attempt_to_find_mill(possible_mills, valid_moves)
        if chosen_position is None:
            chosen_position = random.choice(valid_moves)
        else:
            chosen_position = chosen_position
            # chosen_position = (chosen_position[1], chosen_position[0])  # For some reason the check in GameManager.place_piece() is reversed
        return chosen_position

    def decide_piece_to_move(self):
        random_piece = random.choice(self.pieces)
        return random_piece

    def decide_move_target(self, valid_moves):
        random_cell = random.choice(valid_moves)
        return random_cell
    
    def attempt_to_find_mill(self, possible_mills, valid_moves):
        piece_in_mill = None

        # add to piece_to_check the pieces that positions is not (-1, -1)
        placed_pieces_to_check = [piece.position for piece in self.pieces if piece.position != (-1, -1)]

        # pieces_to_check should be the available positions to place a piece
        valid_move = None

        for already_placed_piece in placed_pieces_to_check:
            mill_index = self.find_piece_in_mill(possible_mills, already_placed_piece)
            if mill_index is not None:
                # if opponents pieces are in this mill then dont place piece in this mill
                placed_pieces_to_check.remove(already_placed_piece)
                if self.check_if_any_other_piece_is_in_mill(possible_mills, placed_pieces_to_check):
                    return self.find_open_position_in_mill(possible_mills[mill_index], valid_moves)
                else:
                    return self.find_open_position_in_mill(possible_mills[mill_index], valid_moves)
        return valid_move
    
    def find_piece_in_mill(self, possible_mills, piece):
        for outer_index, inner_array in enumerate(possible_mills):
            if piece in inner_array:
                return outer_index
        return None
    
    def check_if_any_other_piece_is_in_mill(self, possible_mills, pieces_to_check):
        for piece in pieces_to_check:
            for inner_array in possible_mills:
                if piece in inner_array:
                    return True
                

    def find_open_position_in_mill(self, mill, valid_moves):
        for valid_move in valid_moves:
            if valid_move in mill:
                return valid_move
        return None
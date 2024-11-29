import random
from backend.Player import Player

class ComputerPlayer(Player):
    def __init__(self, max_piece_count, color):
        super().__init__(max_piece_count, color)

    def decide_piece_placement(self, valid_moves):
        random_cell = random.choice(valid_moves)
        return random_cell

    def decide_piece_to_move(self):
        random_piece = random.choice(self.pieces)
        return random_piece

    def decide_move_target(self, valid_moves):
        random_cell = random.choice(valid_moves)
        return random_cell
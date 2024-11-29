import random
from backend.Player import Player

class ComputerPlayer(Player):
    def __init__(self, max_piece_count, color):
        super().__init__(max_piece_count, color)

    def decide_piece_placement(self, valid_moves):
        # Place piece in random empty cell
        # pick random number from 0 to len(valid_moves) - 1
        random_index = random.randint(0, len(valid_moves) - 1)
        random_cell = valid_moves[random_index]
        return random_cell

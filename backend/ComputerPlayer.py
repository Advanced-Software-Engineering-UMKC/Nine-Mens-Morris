from backend.Player import Player

class ComputerPlayer(Player):
    def __init__(self, max_piece_count, color):
        super().__init__(max_piece_count, color)

    def decide_piece_placement(self, valid_moves):
        # Place piece in random empty cell
        random_cell = valid_moves[0]
from backend.Player import Player

class ComputerPlayer(Player):
    def __init__(self, max_piece_count, color):
        super().__init__(max_piece_count, color)

    def place_piece(self, board):
        # Place piece in random empty cell
        empty_cells = board.get_empty_cells()
        random_cell = empty_cells[0]
        board.place_piece(random_cell, self.color)
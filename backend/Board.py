class Board:
    def __init__(self, size):
        self.game_over = False
        self.won = False

    def add_tile(self):
        pass
                       
    def create_board_indices_array(size):
        # """
        # Creates an array of indices representing lines in a grid.

        # Args:
        #     num_lines: The number of lines in the grid.

        # Returns:
        #     A 2D array of tuples representing the indices for each line.
        # """

        indices_array = []
        for i in range(size):
            # Create horizontal lines
            horizontal_line = [(i, j) for j in range(size)]
            indices_array.append(horizontal_line)

            # Create vertical lines
            vertical_line = [(j, i) for j in range(size)]
            indices_array.append(vertical_line)

            # Create diagonal lines (top-left to bottom-right)
            diagonal_line = [(j, i + j) for j in range(size)]
            indices_array.append(diagonal_line)

            # Create diagonal lines (top-right to bottom-left)
            reverse_diagonal_line = [(j, size - 1 - i + j) for j in range(size)]
            indices_array.append(reverse_diagonal_line)

        return indices_array

# Example usage:
num_lines = 3
line_indices_array = create_line_indices_array(num_lines)
print(line_indices_array)
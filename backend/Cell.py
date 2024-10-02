from enum import Enum

class CellType(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    VOID = -1

class Cell:
    def __init__(self):
        self.state = CellType.VOID

    def get_state(self):
        return self.state
    
    def set_state(self, state):
        self.state = state

    
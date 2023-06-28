from enum import Enum

class Events(Enum):
    START = 1,
    NO_VALID_CELLS = 2,
    WAIT_FOR_NEXT_MOVE = 3,
    GRID_CHANGED = 4,
    GAME_OVER = 5

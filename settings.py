from enum import Enum
from gameSprites import Cell

directions = {
    "left": 1,
    "up": 0,
    "right": 3,
    "down": 2
}

class Events(Enum):
    START = 1,
    NO_VALID_CELLS = 2,
    WAIT_FOR_NEXT_MOVE = 3,
    GRID_CHANGED = 4,
    GAME_OVER = 5

GRID_SIZE = 4
WINDOW_SIZE = 100 * GRID_SIZE



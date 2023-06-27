from enum import Enum
from gameSprites import Cell

class Direction(Enum):
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4

class Move:
    def __init__(self, _i: int, _j: int):
        self.i = _i 
        self.j = _j

moves = {
    Direction.DOWN: Move(1, 0),
    Direction.UP: Move(-1, 0),
    Direction.LEFT: Move(0, -1),
    Direction.RIGHT: Move(0, 1)
}


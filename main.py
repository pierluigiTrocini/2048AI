import sys
import pygame
from pygame.locals import *
from moves import *
import gameSprites
from gameEvents import Events

import random

# -------------------------- CONFIG ------------------------ #
GRID_SIZE = 4
WINDOW_SIZE = 100 * GRID_SIZE

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
screen.fill(color=(187, 173, 160))

clock = pygame.time.Clock()
running = True

turn = 0
currentEvent = Events.START

# Grid initialization
grid = [
    [gameSprites.Cell(i, j, 0, WINDOW_SIZE, GRID_SIZE) for i in range(GRID_SIZE)]
    for j in range(GRID_SIZE)
]

# ---------------------------------------------------------- #

def move(turn: int, direction: Direction, grid: list[list[gameSprites.Cell]]):
    print(f"[GAME][TURN - {turn}] [MOVE] Direction: {direction}")

    # for i in range(GRID_SIZE):
    #     for j in range(GRID_SIZE):
    #         if grid[i][j].value != 0:
    #             print(f"[GAME][TURN - {turn}] [CELL - {i} {j}]")

    #             _i, _j  = i, j

    #             while _j >= 0 and _j < GRID_SIZE - 1 and \
    #                 _i >= 0 and _i < GRID_SIZE - 1 and grid[_i + moves[direction].i][_j + moves[direction].j].value == 0:
                    
    #                 grid[_i][_j].value, grid[_i + moves[direction].i][_j + moves[direction].j].value = grid[_i + moves[direction].i][_j + moves[direction].j].value, grid[_i][_j].value

    #                 _i += moves[direction].i
    #                 _j += moves[direction].j



    return grid
    # print(f"[GAME][TURN - {turn}] [MOVE] Direction: {direction} [RETURN]")
    # print(f"[GAME][TURN - {turn}] [CELL - {i} {j}] [MOVE] Direction: {direction} _i: {_i}\t _j: {_j}")


def updateGame(turn: int, event: Events):
    if turn == 0:       # TODO debug
        for _ in range(random.choice([1, 2]) if turn == 0 else 1):
            validCells = [
                (i, j)
                for i, row in enumerate(grid)
                for j, cell in enumerate(row)
                if cell.value == 0
            ]

            if len(validCells) == 0:
                event = Events.NO_VALID_CELLS
            else:
                coords = random.choice(validCells)
                grid[coords[0]][coords[1]].value = random.choice([2, 4])
                event = Events.WAIT_FOR_NEXT_MOVE

    turn += 1

    print(f"[GAME][TURN - {turn} ]")

    drawGrid()

    return turn, event

def drawGrid():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            grid[i][j].draw(screen)

if __name__ == "__main__":
    while running:
        pygame.event.clear()
        event = pygame.event.wait()
        if event.type == KEYDOWN and event.key == K_q:
            running = False
        if event.type == KEYDOWN and event.key == K_SPACE:
            if turn == 0:
                turn, currentEvent = updateGame(turn, currentEvent)
        if turn != 0 and event.type == KEYDOWN and event.key == K_w :
            grid = move(turn, Direction.UP, grid)
        if turn != 0 and event.type == KEYDOWN and event.key == K_a :
            grid = move(turn, Direction.LEFT, grid)
        if turn != 0 and event.type == KEYDOWN and event.key == K_s :
            grid = move(turn, Direction.DOWN, grid)
        if turn != 0 and event.type == KEYDOWN and event.key == K_d :
            grid = move(turn, Direction.RIGHT, grid)

        updateGame(turn, currentEvent)

        pygame.display.flip()
        clock.tick(60)
            

    pygame.quit()
    sys.exit()

import sys
import pygame
from pygame.locals import *
import gameSprites
from gameEvents import Events

import random
# -------------------------- CONFIG ------------------------ #
GRID_SIZE = 4
WINDOW_SIZE = 100 * GRID_SIZE

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
screen.fill(color=(187,173,160))

clock = pygame.time.Clock()
running = True 

turn = 0

random.seed(0)

# Grid initialization
grid = [[gameSprites.Cell(i, j, 0, WINDOW_SIZE, GRID_SIZE) for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]

# ---------------------------------------------------------- #     

def updateGame(turn):
    for _ in range(random.choice([1,2]) if turn == 0 else 1):
        validCells = [ (i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell.value == 0 ]

        if len(validCells) == 0:
            event = Events.NO_VALID_CELLS
        else:
            coords = random.choice(validCells)
            grid[coords[0]][coords[1]].value = random.choice([2, 4])
            event = Events.WAIT_FOR_NEXT_MOVE

    return event    

if __name__ == "__main__":
    updateGame(turn)
    turn += 1

    pygame.event.clear()
    while running:     
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                grid[i][j].draw(screen)

        pygame.display.flip()
        clock.tick(60)

        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE:
            update = updateGame(turn)
            if update == Events.NO_VALID_CELLS:
                pygame.quit()
                sys.exit()
            elif update == Events.WAIT_FOR_NEXT_MOVE:
                turn += 1

    pygame.quit()
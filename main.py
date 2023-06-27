import sys
import pygame
from pygame.locals import *
from moves import *
import gameSprites
from gameEvents import Events

import random

import numpy as np 
from numpy import zeros, array, rot90


# -------------------------- CONFIG ------------------------ #
GRID_SIZE = 4
WINDOW_SIZE = 100 * GRID_SIZE
# ---------------------------------------------------------- #

class Game():
    def __init__(self):
        self.grid = zeros((GRID_SIZE, GRID_SIZE))
        self.gameOver = False 
        self.turn = 0
        self.currentEvent = None

        # ---- pygame setup ---- #
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        self.screen.fill(color=(187, 173, 160))
        self.clock = pygame.time.Clock()
        

    def move(self, direction):
        rotatedGrid = rot90(self.grid, direction)
        columns = [rotatedGrid[i, :] for i in range(GRID_SIZE) ]

        newGrid = array([self.moveLeft(column) for column in columns])

        self.grid = rot90(newGrid, -direction)

    def isGameOver(self):
        pass 

    def putRandomValue(self):
        i, j = (self.grid == 0).nonzero()
        if i.size != 0:
            rnd = random.randint(0, i.size - 1)
            self.grid[i[rnd], j[rnd]] = random.choice([2, 4])
    
    def moveLeft(self, column):
        newColumn = zeros((GRID_SIZE), dtype=column.dtype)

        j = 0
        previous = None 

        for i in range(column.size):
            if column[i] != 0:
                if previous == None:
                    previous = column[i]
                else:
                    if previous == column[i]:
                        newColumn[j] = 2 * column[i]
                        j += 1 
                        previous = None
                    else:
                        newColumn[j] = previous
                        j += 1 
                        previous = column[i]
        if previous != None:
            newColumn[j] = previous
        return newColumn
    
    def drawGrid(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                Cell(i, j, self.grid[i][j], WINDOW_SIZE, GRID_SIZE).draw(self.screen)

    def updateGame(self):
        self.drawGrid()
        if self.currentEvent == Events.START:
            for _ in range(random.choice([1, 2])):
                self.putRandomValue()
            self.currentEvent = Events.WAIT_FOR_NEXT_MOVE
        elif self.currentEvent == Events.WAIT_FOR_NEXT_MOVE:            
            self.putRandomValue()

        print(f"[GAME] [TURN - {self.turn}] [STATUS - {self.currentEvent}]")

        self.turn += 1


if __name__ == "__main__":
    game = Game()

    while not game.gameOver:
        pygame.event.clear()
        event = pygame.event.wait()
        if event.type == KEYDOWN and event.key == K_q:
            game.gameOver = True
        if event.type == KEYDOWN and event.key == K_SPACE:
            game.currentEvent = Events.START
        if game.turn != 0 and event.type == KEYDOWN and event.key == K_w :
            print(directions["up"])
            game.move(directions["up"])
        if game.turn != 0 and event.type == KEYDOWN and event.key == K_a :
            print(directions["left"])
            game.move(directions["left"])
        if game.turn != 0 and event.type == KEYDOWN and event.key == K_s :
            print(directions["down"])
            game.move(directions["down"])
        if game.turn != 0 and event.type == KEYDOWN and event.key == K_d :
            print(directions["right"])
            game.move(directions["right"])

        game.updateGame()
        
        pygame.display.flip()
        game.clock.tick(60)

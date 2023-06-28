from numpy import rot90, zeros, array
import numpy as np
import pygame
import random

from settings import *


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

        newGrid = rot90(array([self.moveLeft(column) for column in columns]), -direction)

        # print(f"[GAME] [ GRID CHANGED - {'no' if np.array_equal(self.grid, newGrid) else 'yes'} ]")

        if not np.array_equal(self.grid, newGrid):
            self.currentEvent = Events.GRID_CHANGED
            self.grid = newGrid
        else:
            self.currentEvent = Events.WAIT_FOR_NEXT_MOVE

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
        # print(f"[GAME] [TURN - {self.turn}] [STATUS - {self.currentEvent}]")

        if self.currentEvent == Events.START:
            for _ in range(random.choice([1, 2])):
                self.putRandomValue()
            self.currentEvent = Events.WAIT_FOR_NEXT_MOVE
        elif self.currentEvent == Events.GRID_CHANGED:
            self.putRandomValue()

        if self.checkGameOver() == Events.GAME_OVER:
            self.gameOver = True

        self.drawGrid()

        self.turn += 1


    def checkGameOver(self):
        noMoves = True

        #se trovo una griglia diversa passa a false

        for dir in directions.values():
            rotatedGrid = rot90(self.grid, dir)
            columns = [rotatedGrid[i, :] for i in range(GRID_SIZE) ]

            tmpGrid = rot90(array([self.moveLeft(column) for column in columns]), -dir)

            if not np.array_equal( self.grid, tmpGrid ):
                noMoves = False

        if noMoves:
            return Events.GAME_OVER
        else:
            return Events.WAIT_FOR_NEXT_MOVE
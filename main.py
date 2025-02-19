#!/usr/bin/python3

import sys
import os
import pygame
import random
import time
from ai_module import AIManager
from ai_module import MinimaxNode

sys.path.append(os.path.join(os.path.dirname(__file__), 'model'))

from model import main

class Game(main.Py2048):
    def __init__(self):
        super().__init__()
        self.AIManager = AIManager()


    def AIPlay(self):
        self.new_number(k = 2)

        running = True

        while running:
            print(self.grid)

            self.draw_game()
            pygame.display.flip()

            cmd = self.AIManager.AIMove(self.grid)

            old_grid = self.grid.copy()
            self.make_move(cmd)

            print(self.grid)
            if self.game_over():
                print("GAME OVER!")
                break

            if not all((self.grid == old_grid).flatten()):
                self.new_number()
            
            # time.sleep(0.25)
    
    def Expectiminimax(self):
        self.new_number(k = 2)
        MinimaxNode(grid = self.grid, state = "current", depth = 0, type = MinimaxNode.Type.RANDOM_TILE, evaluation = 0)

if __name__ == '__main__':
    game = Game()

    # game.AIPlay()

    game.Expectiminimax()

            



#!/usr/bin/python3

import sys
import os
import pygame # type: ignore
import random
import time
from ai_module import AIManager
import utility

sys.path.append(os.path.join(os.path.dirname(__file__), 'model'))

from model import main

class Game(main.Py2048):
    def __init__(self, time_sleep = 0):
        super().__init__()
        self.AIManager = AIManager()
        self.time_sleep = float(time_sleep)


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
            
            time.sleep(self.time_sleep)

if __name__ == '__main__':
    if(len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']):
        print(utility.HELP)
    else:
        game = Game(time_sleep = sys.argv[2] if len(sys.argv) > 1 and ((sys.argv[1] == '-t' or sys.argv[1] == '--time') and sys.argv[2]) else 0)
        game.AIPlay()

            



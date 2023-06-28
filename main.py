import pygame
from pygame.locals import *
from game import Game
from settings import *

from settings import Events


# -------------------------- CONFIG ------------------------ #
GRID_SIZE = 5
WINDOW_SIZE = 100 * GRID_SIZE
# ---------------------------------------------------------- #
if __name__ == "__main__":
    game = Game()

    while not game.gameOver:
        pygame.event.clear()
        event = pygame.event.wait()
        if event.type == KEYDOWN:
            if event.key == K_q:
                game.gameOver = True
            if event.key == K_SPACE:
                game.currentEvent = Events.START
            if game.turn != 0 and event.key == K_w :
                print(directions["up"])
                game.move(directions["up"])
            if game.turn != 0 and event.key == K_a :
                print(directions["left"])
                game.move(directions["left"])
            if game.turn != 0 and event.key == K_s :
                print(directions["down"])
                game.move(directions["down"])
            if game.turn != 0 and event.key == K_d :
                print(directions["right"])
                game.move(directions["right"])
            
            game.updateGame()
        
        pygame.display.flip()
        game.clock.tick(60)

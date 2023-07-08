import pygame
from pygame.locals import *
from game import Game
from settings import *

if __name__ == "__main__":
    game = Game()
    # game.start(game.screen, WINDOW_SIZE)

    while not game.gameOver:
        pygame.event.clear()
        event = pygame.event.wait()
        if event.type == KEYDOWN:
            if event.key == K_q:
                game.gameOver = True
            if event.key == K_SPACE:
                game.currentEvent = Events.START
            if game.turn != 0 and event.key == K_w or event.key == K_UP:
                print(directions["up"])
                game.move(directions["up"])
            if game.turn != 0 and event.key == K_a or event.key == K_LEFT:
                print(directions["left"])
                game.move(directions["left"])
            if game.turn != 0 and event.key == K_s or event.key == K_DOWN:
                print(directions["down"])
                game.move(directions["down"])
            if game.turn != 0 and event.key == K_d or event.key == K_RIGHT:
                print(directions["right"])
                game.move(directions["right"])
            
            game.updateGame()
        
        pygame.display.flip()
        game.clock.tick(60)

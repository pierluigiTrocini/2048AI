

import pygame


def drawStartingPanel(screen, windowSize):
    pygame.draw.rect(
        surface=screen,
        color = pygame.color.Color(243,178,122),
        rect=( 0, 0, windowSize, windowSize )
    )
    font = pygame.font.SysFont(None, 30)
    text_surface = font.render(
        "Tocca SPACE per iniziare",
        True,
        (0, 0, 0)
    )
    text_rect = text_surface.get_rect(
        center = ( windowSize // 2, windowSize // 2 )
    )

    screen.blit(text_surface, text_rect)
    
    return
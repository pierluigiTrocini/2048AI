import pygame

FONT_SIZE = 30
MARGIN = 5

COLOR_0 = pygame.color.Color(205,193,180)
COLOR_2 = pygame.color.Color(238,228,218)
COLOR_4 = pygame.color.Color(238,225,201)
COLOR_8 = pygame.color.Color(243,178,122)
COLOR_16 = pygame.color.Color(246,150,100)
COLOR_32 = pygame.color.Color(247,124,95)
COLOR_64 = pygame.color.Color(247,95,59)
COLOR_128 = pygame.color.Color(237,208,115)
COLOR_256_MORE = pygame.color.Color(237,204,98)

class Cell:
    def __init__(self, x, y, value, windowSize, gridSize): 
        self.value = value
        self.width = windowSize // gridSize
        self.height = windowSize // gridSize

        self.x = x * self.width
        self.y = y * self.height

        self.color = COLOR_0

    def setColor(self):
        if self.value == 0:
            self.color = COLOR_0
        elif self.value == 2:
            self.color = COLOR_2
        elif self.value == 4:
            self.color = COLOR_4
        elif self.value == 8:
            self.color = COLOR_8
        elif self.value == 16:
            self.color = COLOR_16
        elif self.value == 32:
            self.color = COLOR_32
        elif self.value == 64:
            self.color = COLOR_64
        elif self.value == 128:
            self.color = COLOR_128
        else:
            self.color = COLOR_256_MORE

    
    def draw(self, screen: pygame.Surface):
        self.setColor()
        pygame.draw.rect(
            surface = screen,
            color = self.color,
            rect = ( self.x + MARGIN, 
                    self.y + MARGIN, 
                    self.width - 2 * MARGIN, 
                    self.height - 2 * MARGIN )
        )

        font = pygame.font.SysFont(None, FONT_SIZE)
        text_surface = font.render(
            str(self.value) if self.value != 0 else f"({self.x // self.width} {self.y // self.height})",
            True,
            (0, 0, 0)
        )
        text_rect = text_surface.get_rect(
            center=(
                self.x + self.width / 2,
                self.y + self.height / 2,
            )
        )

        screen.blit(text_surface, text_rect)



import pygame
from pygame.locals import * # QUIT, etc.

class PygameGui:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480), 0, 32)
        self.clock = pygame.time.Clock()

    def _draw(self):
        color = (255,0,0)
        rect = Rect(100,100,100,100)
        pygame.draw.rect(self.screen, color, rect)
    
    def render(self):
        
        self.clock.tick(3)

        for event in pygame.event.get():
            if event.type == QUIT:
                return False
        
        self.screen.fill((255,255,255))
        self._draw()
        
        pygame.display.update()
        return True
    
    def quit(self):
        pygame.quit()
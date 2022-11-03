import pygame
from pygame.locals import * # QUIT, etc.

class PygameGui:
    def __init__(self):
        pygame.init()
        self.screen_width = 640
        self.screen_height = 480
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)
        self.clock = pygame.time.Clock()

    def _world2screen(self, world_coords):
        """ Converts world coordinates to coordinates as they appear on screen
        params:
            world_coords: [2]
        return:
            screen_coords: [2]
        """

        screen_coords = world_coords.copy()
        screen_coords[1] *= -1
        screen_coords[1] += self.screen_height
        return screen_coords

    def _draw(self, agent_list):
        color = (255,0,0)
        
        for agent in agent_list:
            screen_pos = self._world2screen(agent.position)
            pygame.draw.circle(self.screen, color, center=screen_pos, radius=50)
    
    def render(self, agent_list):
        
        self.clock.tick(3)

        for event in pygame.event.get():
            if event.type == QUIT:
                return False
        
        self.screen.fill((255,255,255))
        self._draw(agent_list)
        
        pygame.display.update()
        return True
    
    def quit(self):
        pygame.quit()
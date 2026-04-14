import pygame
import pygame.gfxdraw
from .circleshape import CircleShape
from configuration import CIRCLE_RADIUS

class Circle(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
    def draw(self, screen):
        # pygame.draw.circle(screen, "white", self.position, self.radius, 2)
        # Draw nicer circle
        pygame.gfxdraw.aacircle(screen, int(self.position.x), 
                                int(self.position.y), self.radius, (255, 255, 255))
        
        
    # This will be used to update the position of the circle later
    def update(self, dt):
        pass
        
    
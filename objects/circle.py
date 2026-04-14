import pygame
import pygame.gfxdraw
from .circleshape import CircleShape
from configuration import CIRCLE_RADIUS

class Circle(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.color = (255, 255, 255)
        
    def draw(self, screen):
        # pygame.draw.circle(screen, "white", self.position, self.radius, 2)
        # Draw nicer circle
        pygame.gfxdraw.filled_circle(screen, int(self.position.x),
                                  int(self.position.y), self.radius, self.color)
        pygame.gfxdraw.aacircle(screen, int(self.position.x), 
                                int(self.position.y), self.radius, self.color)
        
    # This needs to be reworked to take advantage of the distance from mouse field
    def under_mouse(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        mouse_collision = self.position.distance_squared_to(mouse_pos) < self.r_squared
        if mouse_collision:
            self.color = (255, 0, 0)
            
        elif not mouse_collision and self.color == (255, 0, 0) and not self.is_selected:
            self.color = (255, 255, 255)
        
    # This will be used to update the position of the circle later
    def update(self, dt):
        self.under_mouse()
        self.update_distance_from_mouse(pygame.mouse.get_pos())
    
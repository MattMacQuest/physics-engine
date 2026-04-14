import pygame
import pygame.gfxdraw

class Circle(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.color = (255, 255, 255)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

        # Circle radius
        self.radius = radius
        self.r_squared = radius * radius
        
        # For adding selection capability
        self.is_selected = False
        
        self.mouse_distance = 0.0
        
    def draw(self, screen):
        # pygame.draw.circle(screen, "white", self.position, self.radius, 2)
        # Draw nicer circle
        pygame.gfxdraw.filled_circle(screen, int(self.position.x),
                                  int(self.position.y), self.radius, self.color)
        pygame.gfxdraw.aacircle(screen, int(self.position.x), 
                                int(self.position.y), self.radius, self.color)
        
    # This needs to be reworked to take advantage of the distance from mouse field
    def under_mouse(self, mouse_pos):
        mouse_collision = self.position.distance_squared_to(mouse_pos) < self.r_squared
        if mouse_collision:
            self.color = (255, 0, 0)
            return True
            
        elif not mouse_collision and self.color == (255, 0, 0) and not self.is_selected:
            self.color = (255, 255, 255)
        
    # This will be used to update the position of the circle later
    def update(self, dt, mouse_pos):
        self.under_mouse(mouse_pos)
        self.update_distance_from_mouse(mouse_pos)
    
    def is_colliding(self, other):
        if pygame.Vector2.distance_squared_to(self.position, other.position) < (self.radius + other.radius) * (self.radius + other.radius):
            return True
        return False
    
    def update_distance_from_mouse(self, mouse_pos: pygame.Vector2):
        self.mouse_distance = pygame.Vector2.distance_to(self.position, mouse_pos)
        return self.mouse_distance
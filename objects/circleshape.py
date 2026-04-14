import pygame

class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        
        # These will probable be replaced later depending on C++ implementation
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        
        # Circle radius
        self.radius = radius
        self.r_squared = radius * radius
        
        # For adding selection capability
        self.is_selected = False
        
        self.mouse_distance = self.update_distance_from_mouse(pygame.Vector2(pygame.mouse.get_pos()))
        
    def draw(self, screen):
        pass
    
    def update(self, dt):
        pass
    
    def is_colliding(self, other):
        if pygame.Vector2.distance_squared_to(self.position, other.position) < (self.radius + other.radius) * (self.radius + other.radius):
            return True
        return False
    
        
    def update_distance_from_mouse(self, mouse_pos: pygame.Vector2):
        self.mouse_distance = pygame.Vector2.distance_to(self.position, mouse_pos)
        return self.mouse_distance
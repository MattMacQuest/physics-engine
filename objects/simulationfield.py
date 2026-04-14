import pygame
import random
from .circle import Circle
from configuration import *
from logger import log_event

class SimulationField(pygame.sprite.Sprite):
    # Sets the edges of the field, with normals included
    edges = [
        {"normal": pygame.Vector2(1, 0), "d": SCREEN_WIDTH},
        {"normal": pygame.Vector2(-1, 0), "d": 0},
        {"normal": pygame.Vector2(0, 1), "d": SCREEN_HEIGHT},
        {"normal": pygame.Vector2(0, -1), "d": 0},
    ]
    
    def __init__(self):
        # Calls the parent constructor
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        # Set maximum amount of objects on field
        self.max_objects = MAX_OBJECTS
        
    # Function to spawn new circles into the circles group
    def spawn(self, radius: int, position: pygame.Vector2, velocity: pygame.Vector2) -> Circle:
        # Creates new circle object
        circle = Circle(position.x, position.y, radius)
        
        # Sets velocity (should be 0)
        circle.velocity = velocity
        
        # Logs it
        log_event(f"Circle spawned at {position.x}, {position.y}")
        return circle
        
    # Defines update behavior
    def update(self, position: pygame.Vector2, circles: pygame.sprite.Group) -> None:
        # Checks if you're clicking on an existing circle. In the future this will be
        # used to drag circles around
        for circle in circles:
            if position.distance_squared_to(circle.position) < circle.radius * circle.radius:
                log_event(f"Clicked on circle at {position.x}, {position.y}")
                return
        
        # If there is space for more objects, create a new circle
        if len(circles) < self.max_objects:
            new_circle = self.spawn(CIRCLE_RADIUS, position, pygame.Vector2())
            circles.add(new_circle)
            
        
        # If there are already the maximum permitted objects, cull the oldest the
        # spawn a new one
        else:
            oldest = circles.sprites()[0]
            oldest.kill()
            new_circle = self.spawn(CIRCLE_RADIUS, position, pygame.Vector2())
            circles.add(new_circle)
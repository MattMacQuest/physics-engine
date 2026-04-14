import pygame
import sys
from objects.circle import Circle
from objects.simulationfield import SimulationField
from logger import log_state, log_event

from configuration import SCREEN_HEIGHT, SCREEN_WIDTH, TARGET_FPS

# Could move this to the circle class
def is_circle_under_mouse(circle: Circle):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    mouse_collision = mouse_pos.distance_squared_to(circle.position) < circle.r_squared
    if mouse_collision:
        circle.color = (255, 0, 0)
    elif not mouse_collision and circle.color == (255, 0, 0):
        circle.color = (255, 255, 255)
        
def get_closest_circle(circles: pygame.sprite.Group, closest_circle: Circle, mouse_pos: pygame.Vector2):
    for circle in circles:
        if not closest_circle or closest_circle == circle:
            closest_circle = circle
            continue
        if circle.update_distance_from_mouse(mouse_pos) < closest_circle.update_distance_from_mouse(mouse_pos):
            closest_circle = circle
    return closest_circle

def main():
    pygame.init()
    
    # Initialize the clock and dt
    clock = pygame.time.Clock()
    dt = 0
    
    # Setting up sprite groups
    circles = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    updateable = pygame.sprite.Group()
    spawnable = pygame.sprite.Group()
    
    # Create containers
    Circle.containers = (updateable, drawable, circles)
    # Maybe create a Surface here instead of a SimulationField
    SimulationField.containers = (spawnable)
    
    # Set screen mode (in this case only changing size)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    closest_circle = None
    
    # Initializing the field
    simulationfield = SimulationField()
    
    while True:
        # Log function here
        log_state()
        
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        
        # Get circle closest to mouse. All events should only be able
        # to happen to that object
        closest_circle = get_closest_circle(circles, closest_circle, mouse_pos)
        
        # Iterate over events since last frame
        for event in pygame.event.get():
            # Quit events
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                
            # On-click events. I need to modify this to add
            # the ability to click and drag to move circles
            # around the field if clicking on an existing circle,
            # or to spawn and drag a new circle
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    spawnable.update(mouse_pos, circles)
            
        # Fills the surface with a color
        pygame.Surface.fill(screen, "black")
        
        # Update the updateables. This is where the calls to the C++
        # functions will go as well, to update the location instead of
        # just updating with dt
        updateable.update(dt)
        
        # Check collisions
        
        # Draw objects
        for item in drawable:
            item.draw(screen)
        
        # Update all elements on the screen (flip image buffers)
        pygame.display.flip()
        
        dt = clock.tick(60) * .001 * TARGET_FPS
    
if __name__ == "__main__":
    main()
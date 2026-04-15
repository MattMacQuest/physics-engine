import pygame
import sys
from objects.circle import Circle
from objects.simulationfield import SimulationField
from logger import log_state, log_event

from configuration import SCREEN_HEIGHT, SCREEN_WIDTH, TARGET_FPS
        
def get_closest_circle(circles: pygame.sprite.Group, closest_circle: Circle) -> Circle:
    for circle in circles:
        if not closest_circle or closest_circle == circle:
            closest_circle = circle
            continue
        if circle.mouse_distance_square < closest_circle.mouse_distance_square:
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
    fields = pygame.sprite.Group()
    
    # Set containers for each class
    Circle.containers = (updateable, drawable, circles)
    SimulationField.containers = (fields)
    
    # Set screen mode (in this case only changing size)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Create persistent closest_circle
    closest_circle: Circle = None
    
    # Initializing the field
    simulationfield = SimulationField()
    
    while True:
        # Log function here
        log_state()
        
        # Get mouse position for this tick
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        
        # Get circle closest to mouse. All click/select events should only be able
        # to happen to that object. This is unnecessary if I simply cared about
        # spawning objects without the possibility to manipulate them in the future
        closest_circle = get_closest_circle(circles, closest_circle)
        
        # Iterate over events since last frame
        for event in pygame.event.get():
            # Quit events
            if event.type == pygame.QUIT:
                log_event("Game exit by QUIT event")
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    log_event("Game exit by keypress", key=pygame.key.name(event.key))
                    return
                
            # On-click events. I need to modify this to add
            # the ability to click and drag to move circles
            # around the field if clicking on an existing circle,
            # or to spawn and drag a new circle
            
            # This should be changed to check if there's a circle under already, and if so, call
            # the circle's update function, if not, call the spawner
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    fields.update(mouse_pos, circles)
            
        # Fills the surface with a color
        pygame.Surface.fill(screen, "black")
        
        # Update the updateables. This is where the calls to the C++
        # functions will go as well, to update the location instead of
        # just updating with dt
        updateable.update(dt, mouse_pos)
        
        # Check collisions (C++ function as well)
        
        # Draw objects
        for item in drawable:
            item.draw(screen)
        
        # Should wrap this in a debug mode, as it's only there for debug purposes. Draws
        # a green line to the center of the nearest circle if circles exist, the mouse
        # is on the window, and the mouse is not over the circle
        if (closest_circle and pygame.mouse.get_focused() 
            and closest_circle.mouse_distance_square > closest_circle.radius):
            pygame.draw.aaline(screen, "green", mouse_pos, closest_circle.position)
        # Update all elements on the screen (flip image buffers)
        pygame.display.flip()
        
        dt = clock.tick(60) * .001 * TARGET_FPS
    
if __name__ == "__main__":
    main()
    
# For the C++ functions, it will be necessary to extract the data that I'll need from the
# pygame objects themselves as I can't pass the actual pygame objects into the C++ functions.
# This means I'll have to figure out which types convert to which, for example, how Lists
# convert automatically to vectors. For collisions this will mean passing in things like
# the object's current velocity, position, radius (since I'm only using circles at the
# moment), height and width (when I add rectangles), dt, potentially the gravity constant
# and probably other things I can't think of at the moment. To avoid absurdly long function
# signatures I might use numpy arrays or some other data structure to simplify it on this 
# side. I already know the C++ will be complicated.
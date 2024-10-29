import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Click to Move Object")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Create a class for movable objects
class MovableObject:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)  # Create a rectangle for the object

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)  # Draw the object

    def move(self):
        # Move the object randomly within the screen bounds
        self.rect.x = random.randint(0, screen_width - 50)
        self.rect.y = random.randint(0, screen_height - 50)

# Create a list of five objects
objects = [MovableObject(random.randint(0, screen_width - 50), random.randint(0, screen_height - 50)) for _ in range(5)]

# Main loop
running = True
while running:
    screen.fill(WHITE)  # Clear the screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked_on_object = False

            # Check if an object was clicked
            for obj in objects:
                if obj.rect.collidepoint(event.pos):
                    obj.move()  # Move only the clicked object
                    clicked_on_object = True
                    break

            # End the game if no object was clicked
            if not clicked_on_object:
                running = False

    # Draw all objects
    for obj in objects:
        obj.draw()

    pygame.display.flip()  # Update the display

# Clean up
pygame.quit()


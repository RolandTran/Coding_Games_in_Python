from random import randint
import pgzrun  # Import Pygame Zero for running the game

WIDTH, HEIGHT = 400, 400  # Set the game window size

dots = []  # List to hold dot actors
lines = []  # List to hold the lines that will connect dots

next_dot = 0  # Keeps track of the next dot to connect

# Create 10 dots at random positions
for dot in range(0, 10):
    actor = Actor("dot")  # Create a dot actor (ensure "dot" image is available in the images folder)
    actor.pos = randint(20, WIDTH - 20), randint(20, HEIGHT - 20)  # Random position within bounds
    dots.append(actor)  # Add dot to the list


def draw():
    """Draws the dots and lines on the screen."""
    screen.fill("black")  # Set background color to black

    # Draw dots with their numbers
    number = 1
    for dot in dots:
        screen.draw.text(str(number), (dot.pos[0], dot.pos[1] + 12), color="white")  # Number each dot
        dot.draw()  # Draw the dot actor
        number += 1

    # Draw lines between connected dots
    for line in lines:
        screen.draw.line(line[0], line[1], (100, 0, 0))  # Draw a red line between two points


def on_mouse_down(pos):
    """Handles mouse clicks and connects dots."""
    global next_dot

    # Check if the clicked position is within the next dot
    if dots[next_dot].collidepoint(pos):
        if next_dot > 0:  # Add a line to connect the previous dot to the current dot
            lines.append((dots[next_dot - 1].pos, dots[next_dot].pos))

        next_dot += 1  # Move to the next dot

    # End the game if all dots are connected
    if next_dot == len(dots):
        print("Game Over! All dots connected!")


pgzrun.go()  # Run the game

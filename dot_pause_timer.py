from random import randint
import pgzrun  # Import Pygame Zero for running the game
import time  # Import time for pause functionality

WIDTH, HEIGHT = 400, 400  # Set the game window size

dots = []  # List to hold dot actors
lines = []  # List to hold the lines that will connect dots

next_dot = 0  # Keeps track of the next dot to connect
remaining_time = 60  # Total game time in seconds
paused = False  # Indicates whether the game is paused
game_over = False  # Indicates whether the game is over


# Create 10 dots at random positions
for dot in range(0, 10):
    actor = Actor("dot")  # Create a dot actor (ensure "dot" image is available in the images folder)
    actor.pos = randint(20, WIDTH - 20), randint(20, HEIGHT - 20)  # Random position within bounds
    dots.append(actor)  # Add dot to the list


def draw():
    """Draws the dots, lines, and game status on the screen."""
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

    # Display remaining time
    screen.draw.text(f"Time Left: {remaining_time} s", topleft=(10, 10), color="white")

    # Show "Paused" message if the game is paused
    if paused:
        screen.draw.text("Paused", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="red")

    # Display "Game Over" if the game has ended
    if game_over:
        screen.fill("black")
        screen.draw.text("Game Over! All dots connected!", center=(WIDTH // 2, HEIGHT // 2), fontsize=20, color="white")


def update_timer():
    """Updates the timer every second."""
    global remaining_time, game_over, paused

    if paused or game_over:
        return  # Stop the timer if the game is paused or over

    remaining_time -= 1  # Decrement the timer
    if remaining_time <= 0:  # Check if the timer has reached 0
        game_over = True  # End the game
        print("Time's up! Game Over!")
    else:
        clock.schedule_unique(update_timer, 1.0)  # Schedule the timer to update after 1 second


def on_mouse_down(pos):
    """Handles mouse clicks and connects dots."""
    global next_dot, lines, game_over

    # Check if the clicked position is within the next dot
    if not game_over and dots[next_dot].collidepoint(pos):
        if next_dot:  # Add a line to connect the previous dot to the current dot
            lines.append((dots[next_dot - 1].pos, dots[next_dot].pos))
        next_dot += 1  # Move to the next dot

        # Check if all dots are connected
        if next_dot == len(dots):
            print("Game Over! All dots connected!")
            game_over = True  # Set game over flag to True
            exit()
    else:
        print("Ouch, out of order dot!")  # If the wrong dot is clicked
        lines = []  # Reset lines
        next_dot = 0  # Reset to the first dot


def update():
    """Handles keyboard input for pausing the game."""
    global paused, game_over

    # Toggle pause when the spacebar is pressed
    if keyboard.space and not game_over:
        paused = not paused
        if paused:
            print("Game Paused")
        else:
            print("Game Resumed")
            clock.schedule_unique(update_timer, 1.0)  # Resume the timer if unpaused


# Start the game
clock.schedule_unique(update_timer, 1.0)  # Start the timer
pgzrun.go()  # Run the game

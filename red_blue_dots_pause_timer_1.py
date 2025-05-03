from random import randint
import pgzrun  # Import Pygame Zero for running the game

WIDTH, HEIGHT = 700, 700  # Set the game window size

red_dots = []  # List to hold red dot actors
blue_dots = []  # List to hold blue dot actors
red_lines = []  # List to hold the lines connecting red dots
blue_lines = []  # List to hold the lines connecting blue dots

next_red_dot = 0  # Tracks the next red dot to connect
next_blue_dot = 0  # Tracks the next blue dot to connect
remaining_time = 60  # Total game time in seconds
paused = False  # Indicates whether the game is paused
game_over = False  # Indicates whether the game is over
game_reason = ""  # Tracks the reason for the game ending


# Create 10 red dots at random positions
for _ in range(10):
    actor = Actor("dot")  # Create a dot actor (ensure "dot" image is available in the images folder)
    actor.pos = randint(20, WIDTH - 20), randint(20, HEIGHT - 20)  # Random position within bounds
    red_dots.append(actor)  # Add red dot to the list

# Create 10 blue dots at random positions
for _ in range(10):
    actor = Actor("dot")  # Create a dot actor (ensure "dot" image is available in the images folder)
    actor.pos = randint(20, WIDTH - 20), randint(20, HEIGHT - 20)  # Random position within bounds
    blue_dots.append(actor)  # Add blue dot to the list


def draw():
    """Draws the dots, lines, and game status on the screen."""
    screen.fill("black")  # Set background color to black

    # Draw red dots with their numbers
    number = 1
    for dot in red_dots:
        screen.draw.text(str(number), (dot.pos[0], dot.pos[1] + 12), color="red")  # Number each red dot
        dot.draw()  # Draw the dot actor
        number += 1

    # Draw lines between connected red dots
    for line in red_lines:
        screen.draw.line(line[0], line[1], (255, 0, 0))  # Red lines

    # Draw blue dots with their numbers
    number = 1
    for dot in blue_dots:
        screen.draw.text(str(number), (dot.pos[0], dot.pos[1] + 12), color="blue")  # Number each blue dot
        dot.draw()  # Draw the dot actor
        number += 1

    # Draw lines between connected blue dots
    for line in blue_lines:
        screen.draw.line(line[0], line[1], (0, 0, 255))  # Blue lines

    # Display remaining time
    screen.draw.text(f"Time Left: {remaining_time} s", topleft=(10, 10), color="white")

    # Show "Paused" message if the game is paused
    if paused:
        screen.draw.text("Paused", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="red")

    # Display "Game Over" with the reason when the game ends
    if game_over:
        screen.fill("black")
        screen.draw.text(
            game_reason, center=(WIDTH // 2, HEIGHT // 2), fontsize=20, color="white"
        )
def close_game():
    """Closes the game after a delay."""
    print("Closing game...")
    quit()  # Proper way to exit Pygame Zero

def update_timer():
    """Updates the timer every second."""
    global remaining_time, game_over, paused, game_reason

    if paused or game_over:
        return  # Stop the timer if the game is paused or over

    remaining_time -= 1  # Decrement the timer
    if remaining_time <= 0:  # Check if the timer has reached 0
        game_over = True  # End the game
        game_reason = "Time is up! Game Over!"  # Set the reason
        print(game_reason)
        clock.schedule_unique(close_game, 5.0)  # Schedule the game to close after 5 seconds
    else:
        clock.schedule_unique(update_timer, 1.0)  # Schedule the timer to update after 1 second


def on_mouse_down(pos):
    """Handles mouse clicks and connects dots."""
    global next_red_dot, next_blue_dot, red_lines, blue_lines, game_over, game_reason

    # Check if the clicked position is within the next red dot
    if not game_over and next_red_dot < len(red_dots) and red_dots[next_red_dot].collidepoint(pos):
        if next_red_dot:  # Add a line to connect the previous red dot to the current red dot
            red_lines.append((red_dots[next_red_dot - 1].pos, red_dots[next_red_dot].pos))
        next_red_dot += 1  # Move to the next red dot
        print(f"Red dot {next_red_dot} clicked")  # Debugging message for progress

    # Check if the clicked position is within the next blue dot
    elif not game_over and next_blue_dot < len(blue_dots) and blue_dots[next_blue_dot].collidepoint(pos):
        if next_blue_dot:  # Add a line to connect the previous blue dot to the current blue dot
            blue_lines.append((blue_dots[next_blue_dot - 1].pos, blue_dots[next_blue_dot].pos))
        next_blue_dot += 1  # Move to the next blue dot

    else:
        print("Ouch, out of order dot!")  # If the wrong dot is clicked
        red_lines = []  # Reset red lines
        blue_lines = []  # Reset blue lines
        next_red_dot = 0  # Reset to the first red dot
        next_blue_dot = 0  # Reset to the first blue dot

    # Check if all dots in both sets are connected
    if next_red_dot == len(red_dots) and next_blue_dot == len(blue_dots):
        game_over = True  # Set game over flag to True
        game_reason = "Game Over! All dots connected!"  # Set the reason
        print(game_reason)
        clock.schedule_unique(close_game, 5.0)  # Schedule the game to close after 5 seconds


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

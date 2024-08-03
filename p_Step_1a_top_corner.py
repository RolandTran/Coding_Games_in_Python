import pgzrun

# Set the width and height of the window
WIDTH = 800
HEIGHT = 600

# Load the apple actor
apple = Actor("apple")

# Position the apple in the top-left corner
apple.pos = (40, 55)

def draw():
    # Clear the screen
    screen.clear()
    # Draw the apple actor
    apple.draw()

# Start the Pygame Zero loop
pgzrun.go()

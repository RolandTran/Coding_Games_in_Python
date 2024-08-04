import pgzrun

# Define the width and height of the game window
WIDTH = 800
HEIGHT = 600

# Create an apple Actor
apple = Actor("apple")

# Define a function to place the apple at a specific position
def place_apple():
    apple.x = 300  # Set the x-coordinate of the apple
    apple.y = 200  # Set the y-coordinate of the apple

# Define the draw function that is called to render the screen
def draw():
    screen.clear()  # Clear the screen before drawing
    place_apple()   # Call the function to position the apple
    apple.draw()    # Draw the apple on the screen

# Start the game
pgzrun.go()

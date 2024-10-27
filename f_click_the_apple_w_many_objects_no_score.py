import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 600

apple = Actor("apple")
orange = Actor("orange")
pineapple = Actor("pineapple")

def draw():
    screen.clear()
    # Set random positions for each fruit
    apple.pos = (randint(10, WIDTH - 10), randint(10, HEIGHT - 10))
    orange.pos = (randint(10, WIDTH - 10), randint(10, HEIGHT - 10))
    pineapple.pos = (randint(10, WIDTH - 10), randint(10, HEIGHT - 10))
    
    # Draw each fruit
    apple.draw()
    orange.draw()
    pineapple.draw()

def on_mouse_down(pos):
    clicked_on_object = False  # Flag to check if any object was clicked

    # Check if any fruit was clicked
    if apple.collidepoint(pos):
        print("Good shot! You clicked on the apple.")
        clicked_on_object = True
    if orange.collidepoint(pos):
        print("Oops! You clicked on the orange by mistake.")
        clicked_on_object = True
    if pineapple.collidepoint(pos):
        print("Oops! You clicked on the pineapple by mistake.")
        clicked_on_object = True

    # If no object was clicked, end the game
    if not clicked_on_object:
        print("You missed. Game over!")
        quit()  # End the game

pgzrun.go()

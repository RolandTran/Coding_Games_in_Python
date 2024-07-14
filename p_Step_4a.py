# start of notes;
# p = prototype;
# Step 4a: set the apple iamge at (300,200) when player clicks mouse
# prints "Good shott!" and "You missed! Game over!" when miss click; variation

import pgzrun
import sys

WIDTH = 800
HEIGHT = 600

apple = Actor("apple")

def draw():
    screen.clear()
    apple.pos = (300, 200)
    apple.draw()

def on_mouse_down(pos):
    if apple.collidepoint(pos):
        print("Good shot! You hit the apple!")
    else:
        print("You missed! Game over!")
        sys.exit() # exit games when miss click; also can use quit()

pgzrun.go()

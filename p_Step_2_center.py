# start of notes;
# p = prototype;
# Step 2: set the apple.png at position (300,200) near center

import pgzrun

WIDTH = 800
HEIGHT = 600

apple = Actor("apple")

def draw():
    screen.clear()
    apple.pos = (300, 200)  # Set the position of the apple
    apple.draw()

pgzrun.go()

# start of notes;
# p = prototype;
# Step 4: set the apple iamge at (300,200) when player clicks mouse
# prints "Good shott!" and "You missed! Game over!" when miss click

import pgzrun


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
        quit() # exit games when miss click

pgzrun.go()

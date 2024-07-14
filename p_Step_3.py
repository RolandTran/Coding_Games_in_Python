# start of notes;
# p = prototype;
# Step 3: set the apple iamge at (300,200) when player clicks mouse
# prints "Good shott!" on terminal

import pgzrun

WIDTH = 800
HEIGHT = 600

apple = Actor("apple")

def draw():
    screen.clear()
    apple.pos = (300, 200) # set x and y pos of apple
    apple.draw()

def on_mouse_down(pos): #defines new fxn on_mouse_down()
    # event handler that gets triggered when mouse is clicked
    # (pos) represents the position (coordinates
    print("Good shot!")

# event trigger: on_mouse_down() function is called automatically
# Pygame Zero whenever mouse button is pressed down. the pos argument
# contains the (x,y) of the mouse cursor at time of click

pgzrun.go()

# on_mouse_down() funciton is a callback that responds to mouse clicks
# in game. When player clicks mouse, it prints "Good shot!" to console

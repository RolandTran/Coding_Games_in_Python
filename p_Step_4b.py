# start of notes;
# p = prototype;
# python -m idlelib -e 
# The command python -m idlelib -e in the Linux terminal is used to
# open the IDLE editor for Python scripts.
# 1) Python module invocation:
    # -m : stands for "module" and used to invoke Python module directly
    # from command line
# 2) IDLE Editor (Integrated development and learning environoment)
    # Python IDE ceates interactive shell, a code editor, and other tools
    # -e option tells IDLE to open editor mode, allowing to edit in Python scripts

import pgzrun

WIDTH = 800
HEIGHT = 600

apple = Actor("apple")

def draw():
    screen.clear()
    apple.draw()

def place_apple(): # def a new function called place.apple()
    apple.x = WIDTH // 2  # Set x-coordinate to the center of the screen       
    apple.y = HEIGHT // 2  # Set y-coordinate to the center of the screen      
    # // ensures division is an integer

def on_mouse_down(pos):
    if apple.collidepoint(pos):
        print("Good shot!")
    else:
        print("You missed! Game over!")
        quit() # exit games when miss click

place_apple()  # Call place_apple() to move the image to the center
# calculates center coordinates and updates x and y properties of apple        

pgzrun.go()





    

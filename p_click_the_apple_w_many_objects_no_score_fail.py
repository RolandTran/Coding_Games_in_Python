import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 600

apple = Actor("apple")
orange= Actor("orange")
pineapple = Actor("pineapple")

def draw():
    screen.clear()
    apple.pos = (randint(10, 800), randint(10, 600))  # Set random position for the apple
    apple.draw()
    orange.pos = (randint(10, 800), randint(10, 600))  # Set random position for the orange
    orange.draw()
    pineapple.pos = (randint(10, 800), randint(10, 600))  # Set random position for the pineapple
    pineapple.draw()

def on_mouse_down(pos):
    if apple.collidepoint(pos):
        print("Good shot! You clicked on the apple.")
    if orange.collidepoint(pos):
        print("Good shot! You clicked on the orange.")
    if pineapple.collidepoint(pos):
        print("Good shot! You clicked on the pineapple.") 
    else:
        print("You missed. Game over!")
        quit() # leaves screen open; no difference

pgzrun.go()

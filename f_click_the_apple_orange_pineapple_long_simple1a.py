import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 600

apple = Actor("apple")
apple.pos = (randint(10, 800), randint(10, 600))  # Set random position for the apple

orange = Actor("orange")
orange.pos = (randint(10, 800), randint(10, 600))  # Set random position for the orange

pineapple = Actor("pineapple")
pineapple.pos = (randint(10, 800), randint(10, 600))  # Set random position for the pineapple

def draw():
    screen.clear()
    apple.draw()
    orange.draw()
    pineapple.draw()

def place_apple():
    apple.x = randint(15, WIDTH - 25)
    apple.y = randint(15, HEIGHT - 25)

def place_orange():
    orange.x = randint(15, WIDTH - 25)
    orange.y = randint(15, HEIGHT - 25)

def place_pineapple():
    pineapple.x = randint(15, WIDTH - 25)
    pineapple.y = randint(15, HEIGHT - 25)

def on_mouse_down(pos):
    hit = False
    if apple.collidepoint(pos):
        print("Good shot! You hit the apple!")
        place_apple()
        hit = True
    if orange.collidepoint(pos):
        print("Good shot! You hit the orange!")
        place_orange()
        hit = True
    if pineapple.collidepoint(pos):
        print("Good shot! You hit the pineapple!")
        place_pineapple()
        hit = True
    if not hit:
        print("Game over!")
        quit()


pgzrun.go()

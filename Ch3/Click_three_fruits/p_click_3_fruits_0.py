import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 600

# Define actors
apple = Actor("apple")
pineapple = Actor("pineapple")
orange = Actor("orange")
actors = [apple, pineapple, orange]  # List of all actors


def draw():
    # Clear the screen and draw all actors
    screen.clear()
    for actor in actors:
        actor.draw()

def place_actors():
    # Place each actor at a random position
    for actor in actors:
        actor.pos = (randint(10, WIDTH - 10), randint(10, HEIGHT - 10))

def close_game():
    print("Closing game...")
    quit()

def on_mouse_down(pos):
    actor_clicked = False  # Flag to track if any actor was clicked

    # Check if any actor was clicked
    for actor in actors:
        if actor.collidepoint(pos):
            if actor == apple:
                print("Good shot! You hit the apple!")
            elif actor == pineapple:
                print("Oops! You clicked on the pineapple by mistake!")
            elif actor == orange:
                print("Oops! You clicked on the orange by mistake!")      
            place_actors()  # Reset actor positions after clicking
            actor_clicked = True
            break
    if not actor_clicked:
        print("You missed! Game over!")
        clock.schedule_unique(close_game, 3.0)

place_actors()  # Place actors at random positions initially       
pgzrun.go()

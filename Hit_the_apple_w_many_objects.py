import pgzrun
from random import choice, randint

WIDTH = 800
HEIGHT = 600

apple = Actor("apple")
pineapple = Actor("pineapple")
orange = Actor("orange")
kiwi = Actor("kiwi")
roland = Actor ("roland")
actors = [apple, pineapple, orange, kiwi, roland]  # List of all actors

score = 0  # Initialize the score variable

def draw():
    screen.clear()
    for actor in actors:
        actor.draw()
    print("Score:", score)  # Print the score

def place_actors():
    for actor in actors:
        actor.pos = (randint(10, WIDTH), randint(10, HEIGHT))

def on_mouse_down(pos):
    global score  # Declare score as global to modify it within the function      
    # The score variable is declared as global so that it can be modified within the on_mouse_down() function.
    actor_clicked = False  # Flag to track if any actor was clicked
    for actor in actors:
        if actor.collidepoint(pos):
            if actor == apple:
                print("Good shot! You hit the apple!")
                score += 1
            elif actor == pineapple:
                print("Oops! You clicked on the pineapple by mistake!")
            elif actor == orange:
                print("Oops! You clicked on the orange by mistake!")
            elif actor == roland:
                print("Oops! You clicked on the roland by mistake!")
            elif actor == kiwi:
                print("Oops! You clicked on the kiwi by mistake!")
            place_actors()  # Reset actor position
            actor_clicked = True
            break

    if not actor_clicked:
        print("You missed! Game over!")
        quit()

place_actors()  # Place the actors at random positions initially
pgzrun.go()

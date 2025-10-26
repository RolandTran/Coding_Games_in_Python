import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 600

# Define actors
coin = Actor("coin")
penny = Actor("penny")
nickel = Actor("nickel")
dime = Actor("dime")
quarter = Actor("quarter")
halfdollar = Actor("halfdollar")
dollar = Actor("dollar")
actors = [coin, penny, nickel, dime, quarter, halfdollar, dollar]  # List of all actors

def draw():
    # Clear the screen and draw all actors
    screen.clear()
    for actor in actors:
        actor.draw()

def place_actors():
    # Place each actor at a random position
    for actor in actors:
        actor.pos = (randint(10, WIDTH - 10), randint(10, HEIGHT - 10))

def on_mouse_down(pos):
    actor_clicked = False  # Flag to track if any actor was clicked

    # Check if any actor was clicked
    for actor in actors:
        if actor.collidepoint(pos):
            if actor == coin:
                print("You hit the coin!")
            elif actor == penny:
                print("You clicked on the penny!")
            elif actor == nickel:
                print("You clicked on the nickel!")
            elif actor == dime:
                print("You clicked on the dime!")
            elif actor == quarter:
                print("You clicked on the quarater!")
            elif actor == halfdollar:
                print("You clicked on the halfdollar!")
            elif actor == dollar:
                print("You clicked on the dollar!")       
            place_actors()  # Reset actor positions after clicking
            actor_clicked = True
            break
    if not actor_clicked:
        print("You missed! Game over!")
        pgzrun.exit()  # Gracefully exit the game loop

place_actors()  # Place actors at random positions initially       
pgzrun.go()
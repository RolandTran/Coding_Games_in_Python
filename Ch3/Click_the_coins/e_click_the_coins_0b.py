import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 800

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
    screen.fill("white")
    for actor in actors.value():
        actor.draw()

def place(actor, margin=20):
    actor.pos = (randint(margin, WIDTH - margin), randint(margin, HEIGHT - margin))

def close_game():
    print("Closing game...")
    quit()

def on_mouse_down(pos):
    for name, actor in actors.items():
        if actor.collidepoint(pos):
            if name == "coin":
                print("Good shot! You hit the coin!")
            else:
                print(f"Oops! You clicked on the {name} by mistake!")
            place(actor)
            return
    print("You missed! Game over!")
    clock.schedule_unique(close_game, 3.0)

# Initial placement with optional margins
place(actors["coin"], 20)
place(actors["penny"], 25)
place(actors["nickel"], 15)
place(actors["dime"], 30)
place(actors["quarter"], 35)
place(actors["halfdollar"], 40)
place(actors["dollar"], 45)


pgzrun.go()

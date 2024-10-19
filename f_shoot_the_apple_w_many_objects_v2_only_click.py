import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 600

# Define actors
apple = Actor("apple")
pineapple = Actor("pineapple")
orange = Actor("orange")
kiwi = Actor("kiwi")
roland = Actor("roland")
kid = Actor("kid")
actors = [apple, pineapple, orange, kiwi, roland, kid]

score = 0  # Initialize score

def draw():
    screen.clear()
    for actor in actors:
        actor.draw()
    screen.draw.text(f"Score: {score}", (10, 10), fontsize=30, color="white")

def move_actor(actor):
    actor.pos = (randint(10, WIDTH - 10), randint(10, HEIGHT - 10))

def on_mouse_down(pos):
    global score
    for actor in actors:
        if actor.collidepoint(pos):
            if actor == apple:
                score += 1
                print("Good shot! You hit the apple!")
            else:
                print(f"Oops! You clicked on the {actor.image} by mistake!")
            move_actor(actor)  # Move only the clicked actor
            return  # Exit the function after an actor is clicked

    print("You missed! Game over!")
    pgzrun.exit()

# Place actors at random positions initially
for actor in actors:
    move_actor(actor)

pgzrun.go()

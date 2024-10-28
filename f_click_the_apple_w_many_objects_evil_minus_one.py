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
bash = Actor("bash")
evil_android = Actor("evil_android")
actors = [evil_android, bash, apple, pineapple, orange, kiwi, roland, kid]  # List of all actors

# Initialize score
score = 0

def draw():
    # Clear the screen and draw all actors
    screen.clear()
    for actor in actors:
        actor.draw()
    # Display the score
    screen.draw.text(f"Score: {score}", (10, 10), fontsize=30, color="white")

def place_actors():
    # Place each actor at a random position
    for actor in actors:
        actor.pos = (randint(10, WIDTH - 10), randint(10, HEIGHT - 10))

def on_mouse_down(pos):
    global score  # Declare score as global to modify it within the function
    actor_clicked = False  # Flag to track if any actor was clicked

    # Check if any actor was clicked
    for actor in actors:
        if actor.collidepoint(pos):
            if actor == apple:
                print("Good shot! You hit the apple!")
                score += 1
            elif actor == evil_android:
                print("Bad shot! Evil android took away a point")
                score -= 1
            elif actor == pineapple:
                print("Oops! You clicked on the pineapple by mistake!")
            elif actor == orange:
                print("Oops! You clicked on the orange by mistake!")   
            elif actor == roland:
                print("Oops! You clicked on roland by mistake!")       
            elif actor == kid:
                print("Oops! You clicked on the kid by mistake!")      
            elif actor == kiwi:
                print("Oops! You clicked on the kiwi by mistake!")     
            place_actors()  # Reset actor positions after clicking
            actor_clicked = True
            break

    if not actor_clicked:
        print("You missed! Game over!")
        pgzrun.exit()  # Gracefully exit the game loop

place_actors()  # Place actors at random positions initially       
pgzrun.go()

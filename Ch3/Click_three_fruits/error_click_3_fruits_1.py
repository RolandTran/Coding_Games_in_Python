import pgzrun
from random import randint

score = 0
WIDTH = 800
HEIGHT = 800

# Define actors
apple = Actor("apple")
pineapple = Actor("pineapple")
orange = Actor("orange")

# Initial random positions
apple.pos = (randint(10, WIDTH), randint(10, HEIGHT))
pineapple.pos = (randint(10, WIDTH), randint(10, HEIGHT))
orange.pos = (randint(10, WIDTH), randint(10, HEIGHT))


def draw():
    screen.clear()
    apple.draw()
    pineapple.draw()
    orange.draw()
    screen.draw.text(f"Score: {score}", topright=(WIDTH-15, 10), fontsize=30, color="white")

def place_apple():
    apple.x = randint(20, WIDTH - 20)
    apple.y = randint(20, HEIGHT - 20)

def place_orange():
    orange.x = randint(25, WIDTH - 15)
    orange.y = randint(25, HEIGHT - 15)

def place_pineapple():
    pineapple.x = randint(15, WIDTH - 25)
    pineapple.y = randint(15, HEIGHT - 25)

def close_game():
    print("Closing game...")
    quit()

def on_mouse_down(pos):
    if apple.collidepoint(pos):
        print("Good shot! You hit the apple!")
        score += 1
        place_apple()
    elif pineapple.collidepoint(pos):
        print("Oops! You clicked on the pineapple by mistake!")
        place_pineapple()
    elif orange.collidepoint(pos):
        print("Oops! You clicked on the orange by mistake!")
        place_orange()
    else:
        print("You missed! Game over!")
        clock.schedule_unique(close_game, 3.0)

place_apple()
place_pineapple()
place_orange()

# Remove or define update_timer if needed
# clock.schedule_unique(update_timer, 1.0)

pgzrun.go()

import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 600

apple = Actor("apple")
pineapple = Actor("pineapple")
orange = Actor("orange")
actors = [apple, pineapple, orange]

def draw():
    screen.clear()
    for actor in actors:
        actor.draw()

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
    actor_clicked = False
    for actor in actors:
        if actor.collidepoint(pos):
            if actor == apple:
                print("Good shot! You hit the apple!")
                place_apple()
            elif actor == pineapple:
                print("Oops! You clicked on the pineapple by mistake!")
                place_pineapple()
            elif actor == orange:
                print("Oops! You clicked on the orange by mistake!")
                place_orange()
            actor_clicked = True
            break
    if not actor_clicked:
        print("You missed! Game over!")
        clock.schedule_unique(close_game, 3.0)

place_apple()
place_pineapple()
place_orange()

# Remove or define update_timer if needed
# clock.schedule_unique(update_timer, 1.0)

pgzrun.go()

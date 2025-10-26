import pgzrun
from random import randint

score = 0
WIDTH = 800
HEIGHT = 600

apple = Actor("apple")
apple.pos = (randint(10, 800), randint(10, 600))

def place_apple():
    apple.pos = (randint(10, 800), randint(10, 600))

def draw():
    screen.clear()
    apple.draw()
    screen.draw.text(f"Score: {score}", topright=(WIDTH-15, 10), fontsize=30, color="white")

# ─── Close Game ────────────────────────
def close_game():
    print("Closing game...")
    quit()

def on_mouse_down(pos):
    global score
    if apple.collidepoint(pos):
        score += 1
        print("Good shot!")
        place_apple()
    else:
        print("Game over!")
        clock.schedule_unique(close_game, 2.0)

pgzrun.go()


import pgzrun
from random import randint

WIDTH, HEIGHT = 800, 800
score, time_left = 0, 60
paused = game_over = space_pressed = False

# Create Actor objects first
coin     = Actor("coin")
penny    = Actor("penny")
nickel   = Actor("nickel")
dime     = Actor("dime")
quarter  = Actor("quarter")
halfdollar = Actor("halfdollar")
dollar   = Actor("dollar")

# Coin values and margin
coins = {
    "coin": (1.00, 20), "penny": (0.01, 25), "nickel": (0.05, 15),
    "dime": (0.10, 20), "quarter": (0.25, 25), "halfdollar": (0.50, 15), "dollar": (1.00, 15)
}
actors = {name: Actor(name) for name in coins}

rules = """PAUSED - GAME RULES:

- Click coins to earn USD.
- Don't miss or it's game over!
- Press SPACE to pause/resume.
- Highest score wins when time runs out.
"""

def place_all():
    for name, actor in actors.items():
        m = coins[name][1]
        actor.pos = (randint(m, WIDTH - m), randint(m, HEIGHT - m))

def draw():
    screen.fill("white")
    for actor in actors.values(): actor.draw()
    screen.draw.text(f"Score: {round(score,2)}", topright=(WIDTH - 15, 10), fontsize=30, color="black")
    screen.draw.text(f"Time: {time_left}s", topleft=(10, 10), fontsize=30, color="black")
    if paused:
        screen.draw.filled_rect(Rect(100, 100, WIDTH - 200, HEIGHT - 200), (0, 0, 0, 180))
        screen.draw.textbox(rules, Rect(150, 150, WIDTH - 300, HEIGHT - 300), color="white", align="left")
    if game_over:
        screen.draw.text(f"Time's up! Final score: {round(score,2)}", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")

def close_game():
    print("Closing game...")
    quit()

def update():
    global paused, space_pressed
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
    elif not keyboard.space:
        space_pressed = False

def update_timer():
    global time_left, game_over
    if not paused and not game_over:
        time_left -= 1
        if time_left <= 0:
            game_over = True
            print(f"Time's up! Final score: {round(score,2)}")
            clock.schedule_unique(close_game, 3.0)
    clock.schedule_unique(update_timer, 1.0)

def on_mouse_down(pos):
    global score
    if paused or game_over: return
    for name, actor in actors.items():
        if actor.collidepoint(pos):
            score += coins[name][0]
            print(f"You clicked {name}! Score: {round(score,2)}")
            m = coins[name][1]
            actor.pos = (randint(m, WIDTH - m), randint(m, HEIGHT - m))
            return
    print(f"Missed! Game over. Final score: {round(score,2)}")
    clock.schedule_unique(close_game, 3.0)

place_all()
clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

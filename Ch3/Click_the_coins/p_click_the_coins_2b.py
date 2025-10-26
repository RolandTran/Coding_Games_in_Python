import pgzrun
from random import randint

WIDTH, HEIGHT, score, remaining_time = 800, 800, 0, 60
paused, game_over, space_pressed = False, False, False

# Define coin values and margins
coins = {
    "coin": (1.00, 20),
    "penny": (0.01, 25),
    "nickel": (0.05, 15),
    "dime": (0.10, 20),
    "quarter": (0.25, 25),
    "halfdollar": (0.50, 15),
    "dollar": (1.00, 15),
}

# Create Actor objects and assign to dictionary
actors = {name: Actor(name) for name in coins}

# -------- Rules text ---------------------
rules_text = """
PAUSED - GAME RULES:

- Click the coins by moving the mouse cursor over it and clicking.
- The game will end if you click outside the coins.
- Acquire the most USD
- Press SPACE to pause or resume the game.
"""

# Place all coins randomly with margin
def place_all():
    for name, actor in actors.items():
        margin = coins[name][1]
        actor.pos = (randint(margin, WIDTH - margin), randint(margin, HEIGHT - margin))

def close_game():
    print("Closing game...")
    quit()

def draw():
    screen.fill("white")
    for actor in actors.values():
        actor.draw()
    screen.draw.text(f"Score: {round(score,2)}", topright=(WIDTH-15, 10), fontsize=30, color="black")
    screen.draw.text(f"Time: {remaining_time}s", topleft=(10, 10), fontsize=30, color="black")
    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150, 150, WIDTH - 300, HEIGHT - 300), color="white", align="left")
    if game_over:
        screen.draw.text(f"Time's up! Final score is {round(score,2)}", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")

def update_timer():
    global remaining_time, game_over
    if not paused and not game_over:
        remaining_time -= 1
        if remaining_time <= 0:
            game_over = True
            print(f"Time's up! Your final score was {score}.")
            clock.schedule_unique(close_game, 3.0)
        else:
            clock.schedule_unique(update_timer, 1.0)
    else:
        # Keep checking every second while paused
        clock.schedule_unique(update_timer, 1.0)

def update():
    global paused, space_pressed
    # allow pause/suesm toggle always when not game_over
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
    elif not keyboard.space:
        space_pressed = False
    if paused or game_over: # stop all other updateds if puased or game is over
        return # skip any game logic

def on_mouse_down(pos):
    global score # score is global level and must be declared
    if paused or game_over:
        return # ignore all clicks if the game is paused or over
    for name, actor in actors.items():
        if actor.collidepoint(pos):
            value = coins[name][0]
            score += value
            print(f"You clicked on the {name}! Your score is {round(score, 2)} USD.")
            margin = coins[name][1]
            actor.pos = (randint(margin, WIDTH - margin), randint(margin, HEIGHT - margin))
            return
    print(f"You missed! Game over! Your final score is {round(score, 2)} USD.")
    clock.schedule_unique(close_game, 3.0)

place_all()
clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

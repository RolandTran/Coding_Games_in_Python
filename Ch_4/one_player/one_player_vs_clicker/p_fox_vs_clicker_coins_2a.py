import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 800

score_fox = 0.0
score_clicker = 0.0
paused = False
space_pressed = False
game_over = False
time_left = 90
flash_time = 0

# --- Actors ---
fox = Actor("fox", (100, 100))

# Define coins and their values 💰
coins = [
    {"actor": Actor("coin"), "value": 1.00},
    {"actor": Actor("penny"), "value": 0.01},
    {"actor": Actor("nickel"), "value": 0.05},
    {"actor": Actor("dime"), "value": 0.10},
    {"actor": Actor("quarter"), "value": 0.25},
    {"actor": Actor("halfdollar"), "value": 0.50},
    {"actor": Actor("dollar"), "value": 1.00}
]

def place_actor(actor):
    actor.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

def flash():
    global flash_time
    flash_time = 1.5

# Place everything initially
place_actor(fox)
for c in coins:
    place_actor(c["actor"])

rules_text = """
PAUSED - GAME RULES:

- Fox uses arrow keys to move.
- Mouse or touch collects coins.
- Game lasts 90 seconds.
- Higher score wins!
- SPACE = Pause / Resume
"""

def draw():
    screen.fill("white")

    fox.draw()
    for c in coins:
        c["actor"].draw()

    screen.draw.text(f"Fox Score: {score_fox:.2f}", (10, 10), color="black")
    screen.draw.text(f"Clicker Score: {score_clicker:.2f}", (10, 30), color="black")
    screen.draw.text(f"Time Left: {time_left}", topright=(WIDTH-10, 10), color="red")

    if flash_time > 0:
        screen.draw.filled_rect(Rect(0,0,WIDTH,HEIGHT),(255,255,0,80))

    if paused and not game_over:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150,150,WIDTH-300,HEIGHT-300), color="white")

    if game_over:
        screen.fill("lightblue")

        if score_fox > score_clicker:
            winner = "Fox Wins! 🦊"
        elif score_clicker > score_fox:
            winner = "Clicker Wins! 🖱️"
        else:
            winner = "It's a Tie! 🤝"

        screen.draw.text(winner, center=(WIDTH/2, HEIGHT/2-40), fontsize=60, color="black")
        screen.draw.text(f"Fox: {score_fox:.2f} | Clicker: {score_clicker:.2f}",
                         center=(WIDTH/2, HEIGHT/2+20), fontsize=40, color="black")
        screen.draw.text("CLICK TO RESTART",
                         center=(WIDTH/2, HEIGHT/2+120), fontsize=45, color="darkred")

def update_timer():
    global time_left, game_over
    if not paused and not game_over:
        time_left -= 1
        if time_left <= 0:
            game_over = True
        else:
            clock.schedule_unique(update_timer, 1.0)
    else:
        clock.schedule_unique(update_timer, 1.0)

def update():
    global paused, space_pressed, flash_time, score_fox

    if flash_time > 0:
        flash_time -= 1

    # Pause toggle
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
    elif not keyboard.space:
        space_pressed = False

    if paused or game_over:
        return

    # Fox movement & boundaries
    if keyboard.left: fox.x -= 6
    if keyboard.right: fox.x += 6
    if keyboard.up: fox.y -= 6
    if keyboard.down: fox.y += 6
    fox.x = max(20, min(WIDTH-20, fox.x))
    fox.y = max(20, min(HEIGHT-20, fox.y))

    # Fox coin collection
    for c in coins:
        if fox.colliderect(c["actor"]):
            score_fox += c["value"]
            flash()
            place_actor(c["actor"])

def on_mouse_down(pos):
    global score_clicker, score_fox, game_over
    if game_over:
        restart_game()
        return

    if fox.collidepoint(pos):
        score_fox -= 0.10
        flash()
        place_actor(fox)
        return

    for c in coins:
        if c["actor"].collidepoint(pos):
            score_clicker += c["value"]
            flash()
            place_actor(c["actor"])
            break

def restart_game():
    global score_fox, score_clicker, time_left, paused, game_over, flash_time
    score_fox = score_clicker = 0.0
    time_left = 90
    paused = game_over = False
    flash_time = 0
    place_actor(fox)
    for c in coins:
        place_actor(c["actor"])

clock.schedule_interval(update_timer, 1.0)
pgzrun.go()

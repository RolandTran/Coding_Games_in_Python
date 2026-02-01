import pygame
import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 800

# Scores and states
score_fox = 0.0
score_clicker = 0.0
paused = False
space_pressed = False
game_over = False
time_left = 90
flash_time = 0

# ─── Music setup ───────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/jamesbondtheme.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# --- Actors ---
fox = Actor("fox")
coin = Actor("coin")
penny = Actor("penny")
nickel = Actor("nickel")
dime = Actor("dime")
quarter = Actor("quarter")
halfdollar = Actor("halfdollar")
dollar = Actor("dollar")

# --- Place function for all coins/fox ---
def place_actor(actor):
    actor.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

# --- Spawn everything ---
for a in [fox, coin, penny, nickel, dime, quarter, halfdollar, dollar]:
    place_actor(a)

# --- Pause rules text ---
rules_text = """
PAUSED - GAME RULES:

- Fox moves with arrow keys
- Mouse/touch clicks collect coins
- Game lasts 90 seconds
- Higher score wins
- SPACE = Pause / Resume
"""

# --- Flash effect ---
def flash():
    global flash_time
    flash_time = 2.0  # ~0.5 seconds

# --- Coins dictionary with value and sounds ---
coins = [
    {"actor": coin, "value": 1, "sound": sounds.hitcoin},
    {"actor": penny, "value": 0.01, "sound": sounds.hitpenny},
    {"actor": nickel, "value": 0.05, "sound": sounds.hitnickel},
    {"actor": dime, "value": 0.10, "sound": sounds.hitdime},
    {"actor": quarter, "value": 0.25, "sound": sounds.hitquarter},
    {"actor": halfdollar, "value": 0.50, "sound": sounds.hithalfdollar},
    {"actor": dollar, "value": 1, "sound": sounds.hitdollar}
]

# --- Draw function ---
def draw():
    screen.fill("white")

    for a in [fox, coin, penny, nickel, dime, quarter, halfdollar, dollar]:
        a.draw()

    screen.draw.text(f"Fox Score: {score_fox:.2f}", (10,10), color="black")
    screen.draw.text(f"Clicker Score: {score_clicker:.2f}", (10,30), color="black")
    screen.draw.text(f"Time Left: {time_left}", topright=(WIDTH-10,10), color="red")

    if flash_time > 0:
        screen.draw.filled_rect(Rect(0,0,WIDTH,HEIGHT),(255,255,0,80))

    if paused and not game_over:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150,150,WIDTH-300,HEIGHT-300), color="white")

    if game_over:
        screen.fill("lightblue")
        if score_fox > score_clicker: winner = "Fox Wins! 🦊"
        elif score_clicker > score_fox: winner = "Clicker Wins! 🖱️"
        else: winner = "It's a Tie! 🤝"
        screen.draw.text(winner, center=(WIDTH/2, HEIGHT/2-40), fontsize=60, color="black")
        screen.draw.text(f"Fox: {score_fox:.2f} | Clicker: {score_clicker:.2f}", 
                         center=(WIDTH/2, HEIGHT/2+20), fontsize=40, color="black")
        screen.draw.text("CLICK TO RESTART", center=(WIDTH/2, HEIGHT/2+120), fontsize=45, color="darkred")

def print_winner():
    if score_fox > score_clicker: print("Fox Wins! 🦊")
    elif score_clicker > score_fox: print("Clicker Wins! 🖱️")
    else: print("Tie Game! 🤝")
    print(f"Final Scores — Fox: {score_fox:.2f}, Clicker: {score_clicker:.2f}")

def end_game():
    global game_over
    game_over = True
    print_winner()

# --- Timer ---
def update_timer():
    global time_left
    if not paused and not game_over:
        time_left -= 1
        if time_left <= 0:
            end_game()
        else:
            clock.schedule_unique(update_timer,1.0)
    else:
        clock.schedule_unique(update_timer,1.0)



# --- Update ---
def update():
    global paused, space_pressed, score_fox, flash_time, game_over

    # Reduce flash timer
    if flash_time > 0:
        flash_time -= 1
        flash_time = max(flash_time, 0)

    # Pause toggle
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
    elif not keyboard.space:
        space_pressed = False

    # Block movement/collision if paused or game_over
    if paused or game_over:
        return

    # Fox movement
    dx = (keyboard.right - keyboard.left) * 6
    dy = (keyboard.down - keyboard.up) * 6
    fox.x = max(20, min(WIDTH-20, fox.x + dx))
    fox.y = max(20, min(HEIGHT-20, fox.y + dy))

    # Fox collisions
    for c in coins:
        if fox.colliderect(c["actor"]):
            c["sound"].play()
            score_fox += c["value"]
            flash()
            place_actor(c["actor"])

# --- Mouse clicks ---
def on_mouse_down(pos):
    global score_clicker, score_fox, game_over
    if game_over:
        restart_game()
        return

    # Click fox
    if fox.collidepoint(pos):
        sounds.hitfox.play()
        score_fox = max(0, score_fox - 0.10)
        flash()
        place_actor(fox)

    # Click coins
    for c in coins:
        if c["actor"].collidepoint(pos):
            c["sound"].play()
            score_clicker += c["value"]
            flash()
            place_actor(c["actor"])
            break  # Only one coin per click

# --- Restart ---
def restart_game():
    global score_fox, score_clicker, time_left, paused, game_over, flash_time
    score_fox = 0.0
    score_clicker = 0.0
    time_left = 90
    flash_time = 0
    paused = False
    game_over = False
    for a in [fox, coin, penny, nickel, dime, quarter, halfdollar, dollar]:
        place_actor(a)

# --- Schedule timer ---
clock.schedule_unique(update_timer, 1.0)

# --- Run game ---
pgzrun.go()

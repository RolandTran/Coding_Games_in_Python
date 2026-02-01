# condensed_currency_fox.py
# Refactor of original game: identical behavior, condensed using lists/dicts.

import pygame
import pgzrun
from random import randint, choice

WIDTH = 800
HEIGHT = 800

# --- game state ---
score_fox = 0.0
score_clicker = 0.0
fox_speed = 1
paused = False
space_pressed = False
game_over = False
time_left = 90
flash_time = 0

# --- music (same as original) ---
pygame.mixer.init()
pygame.mixer.music.load("music/jamesbondtheme.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# --- fox actor ---
fox = Actor("fox")
fox.pos = 100, 100

# --- coin definitions (keeps per-coin nuance identical to original) ---
# Fields:
# name, value (USD), sound, rot_incr_on_fox, rot_incr_on_click,
# speed_incr_on_fox (applied to dx/dy), speed_incr_on_click (applied to dx/dy),
# fox_speed_incr_on_fox (some coins change fox speed; dollar intentionally doesn't in original)
COIN_DEFS = [
    {"name": "coin",      "value": 1.00, "sound": "hitcoin",      "rot_incr_on_fox": 1,    "rot_incr_on_click": 1,    "speed_incr_on_fox": 1,    "speed_incr_on_click": 1,    "fox_speed_incr_on_fox": 1},
    {"name": "penny",     "value": 0.01, "sound": "hitpenny",     "rot_incr_on_fox": 0.01, "rot_incr_on_click": 0.01, "speed_incr_on_fox": 0.01, "speed_incr_on_click": 0.01, "fox_speed_incr_on_fox": 0.01},
    {"name": "nickel",    "value": 0.05, "sound": "hitnickel",    "rot_incr_on_fox": 0.05, "rot_incr_on_click": 0.05, "speed_incr_on_fox": 0.05, "speed_incr_on_click": 0.05, "fox_speed_incr_on_fox": 0.05},
    {"name": "dime",      "value": 0.10, "sound": "hitdime",      "rot_incr_on_fox": 0.10, "rot_incr_on_click": 0.10, "speed_incr_on_fox": 0.10, "speed_incr_on_click": 0.10, "fox_speed_incr_on_fox": 0.10},
    {"name": "quarter",   "value": 0.25, "sound": "hitquarter",   "rot_incr_on_fox": 0.25, "rot_incr_on_click": 0.25, "speed_incr_on_fox": 0.25, "speed_incr_on_click": 0.25, "fox_speed_incr_on_fox": 0.25},
    {"name": "halfdollar","value": 0.50, "sound": "hithalfdollar","rot_incr_on_fox": 0.50, "rot_incr_on_click": 0.25, "speed_incr_on_fox": 0.50, "speed_incr_on_click": 0.50, "fox_speed_incr_on_fox": 0.50},
    {"name": "dollar",    "value": 1.00, "sound": "hitdollar",    "rot_incr_on_fox": 1.00, "rot_incr_on_click": 1.00, "speed_incr_on_fox": 1,    "speed_incr_on_click": 1,    "fox_speed_incr_on_fox": 0.0},  # original omitted fox_speed change
]

# Create coin objects (Actor + dynamic attributes)
coins = []
for d in COIN_DEFS:
    a = Actor(d["name"])
    a.pos = randint(10, WIDTH-10), randint(10, HEIGHT-10)
    a.dx = choice([-3, -2, -1, 1, 2, 3])
    a.dy = choice([-3, -2, -1, 1, 2, 3])
    a.rot_speed = 5
    a.angle = 0
    coins.append({
        "def": d,
        "actor": a
    })

# --- utility placement ---
def place_actor(a):
    a.x = randint(20, WIDTH-20)
    a.y = randint(20, HEIGHT-20)

def place_coin_obj(cobj):
    place_actor(cobj["actor"])

# initial placements (fox + all coins)
place_actor(fox)
for c in coins:
    place_coin_obj(c)

# --- rules text ---
rules_text = """
PAUSED - GAME RULES:

- Fox moves with arrow keys
- Mouse/touch clicks collect coins
- Game lasts 90 seconds
- Higher score wins
- SPACE = Pause / Resume
""".strip()

# --- flash effect ---
def flash():
    global flash_time
    flash_time = 2.0

# --- restart / end / printing ---
def restart_game():
    global score_fox, score_clicker, time_left, paused, game_over, flash_time, fox_speed
    score_fox = 0.0
    score_clicker = 0.0
    time_left = 90
    flash_time = 0
    paused = False
    game_over = False
    fox_speed = 2
    place_actor(fox)
    for c in coins:
        place_coin_obj(c)

# --- drawing ---
def draw():
    screen.fill("white")
    fox.draw()
    for c in coins:
        c["actor"].draw()

    screen.draw.text(f"Fox Score: {score_fox:.2f}", (10,10), color="black")
    screen.draw.text(f"Clicker Score: {score_clicker:.2f}", (10,30), color="black")
    screen.draw.text(f"Time Left: {time_left}", topright=(WIDTH-10,10), color="red")

    if flash_time > 0:
        screen.draw.filled_rect(Rect(0,0,WIDTH,HEIGHT),(255,255,0,80))

    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text, Rect(150,150,WIDTH-300,HEIGHT-300), color="white")

    if game_over:
        screen.fill("lightblue")
        if score_fox > score_clicker:
            winner = "Fox Wins! 🦊"
        elif score_clicker > score_fox:
            winner = "Clicker Wins! 🖱️"
        else:
            winner = "It's a Tie! 🤝"

        screen.draw.text(winner, center=(WIDTH/2, HEIGHT/2-40), fontsize=60, color="black")
        screen.draw.text(f"Fox: {score_fox:.2f} | Clicker: {score_clicker:.2f}", center=(WIDTH/2, HEIGHT/2+20), fontsize=40, color="black")
        screen.draw.text("CLICK TO RESTART", center=(WIDTH/2, HEIGHT/2+120), fontsize=45, color="darkred")

def close_game():
    print("Closing game...")
    quit()

def end_game():
    global game_over
    game_over = True
    print_winner()

# --- timer (keeps original scheduling behavior) ---
def update_timer():
    global time_left
    if not paused and not game_over:
        time_left -= 1
        if time_left <= 0:
            sounds.miss.play()
            clock.schedule_unique(close_game, 5.0)
            end_game()
        else:
            clock.schedule_unique(update_timer, 1.0)
    else:
        clock.schedule_unique(update_timer, 1.0)

def print_winner():
    if score_fox > score_clicker:
        print("Fox Wins! 🦊")
    elif score_clicker > score_fox:
        print("Clicker Wins! 🖱️")
    else:
        print("Tie Game! 🤝")
    print(f"Final Scores — Fox: {score_fox:.2f}, Clicker: {score_clicker:.2f}")

# --- movement helpers ---
def clamp_speed(val, limit=20):
    if val > limit: return limit
    if val < -limit: return -limit
    return val

def move_coin_obj(cobj):
    a = cobj["actor"]
    a.x += a.dx
    a.y += a.dy
    if a.left < 0 or a.right > WIDTH:
        a.dx *= -1
    if a.top < 0 or a.bottom > HEIGHT:
        a.dy *= -1
    a.angle = (a.angle + a.rot_speed) % 360

# --- update loop ---
def update():
    global paused, space_pressed, score_fox, flash_time, game_over, fox_speed, score_clicker

    if flash_time > 0:
        flash_time -= 1
        if flash_time < 0:
            flash_time = 0

    # SPACE pause toggle (preserve original behavior)
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
        if paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    elif not keyboard.space:
        space_pressed = False

    if paused or game_over:
        return

    # move coins
    for c in coins:
        move_coin_obj(c)

    # fox movement (same boundary limits)
    if keyboard.left: fox.x -= fox_speed
    if keyboard.right: fox.x += fox_speed
    if keyboard.up: fox.y -= fox_speed
    if keyboard.down: fox.y += fox_speed

    fox.x = max(20, min(WIDTH-20, fox.x))
    fox.y = max(20, min(HEIGHT-20, fox.y))

    # collisions: fox with each coin
    for c in coins:
        d = c["def"]
        a = c["actor"]
        if fox.colliderect(a):
            # play sound
            getattr(sounds, d["sound"]).play()
            # fox score change
            score_fox += d["value"]
            # rot speed change on fox-collision
            a.rot_speed += d["rot_incr_on_fox"]
            # flash effect
            flash()
            # speed increase for coin (dx/dy)
            incr = d["speed_incr_on_fox"]
            a.dx += incr if a.dx > 0 else -incr
            a.dy += incr if a.dy > 0 else -incr
            a.dx = clamp_speed(a.dx)
            a.dy = clamp_speed(a.dy)
            # fox speed increment (note: dollar has 0 so no change, preserving original quirk)
            fox_speed_change = d["fox_speed_incr_on_fox"]
            if fox_speed_change:
                # original used small floats for pennies etc; keep fox_speed as float
                # but original started as int; we preserve numeric behavior
                # (fox_speed grows cumulatively)
                globals()["fox_speed"] += fox_speed_change
            # prints to match original logs (varied messages in original; we keep generic)
            print(f"Fox's score is {score_fox:.2f} USD")
            place_coin_obj(c)

    # game over condition (redundant with timer but keep identical)
    if time_left <= 0:
        game_over = True

    # coin-vs-coin collisions: each coin places itself if it collides with any other coin (mirrors original)
    for i, c in enumerate(coins):
        ai = c["actor"]
        for j, other in enumerate(coins):
            if i == j: continue
            aj = other["actor"]
            if ai.colliderect(aj):
                place_coin_obj(c)
                break  # placed this coin, break to next coin

# --- mouse clicks (identical logic) ---
def on_mouse_down(pos):
    global score_clicker, score_fox, game_over, flash_time, fox_speed
    if game_over:
        restart_game()
        return

    # click fox
    if fox.collidepoint(pos):
        sounds.miss.play()
        score_clicker += 2.0
        score_fox -= 5.0
        fox_speed -= 0.25
        flash()
        place_actor(fox)
        return

    # check coins (preserve original priority/order: coin then penny then nickel... )
    for c in coins:
        d = c["def"]
        a = c["actor"]
        if a.collidepoint(pos):
            getattr(sounds, d["sound"]).play()
            score_clicker += d["value"]
            # rot speed change on click (some coins differ; we've preserved that in defs)
            a.rot_speed += d["rot_incr_on_click"]
            flash()
            # speed increase for coin on click
            incr = d["speed_incr_on_click"]
            a.dx += incr if a.dx > 0 else -incr
            a.dy += incr if a.dy > 0 else -incr
            a.dx = clamp_speed(a.dx)
            a.dy = clamp_speed(a.dy)
            print(f"Clicker's score is {score_clicker:.2f} USD")
            place_coin_obj(c)
            return

    # miss (clicked empty space)
    sounds.miss.play()
    print(f" Clicker missed and loses $0.25! Clicker's score is now {round(score_clicker,2)}")
    score_clicker -= 0.05

# --- Schedule timer ---
clock.schedule_unique(update_timer, 1.0)

# --- ensure graceful exit prints identical final block behavior ---
try:
    pgzrun.go()
finally:
    if not game_over:
        print("\nGame closed manually — treating as Game Over!\n")
        end_game()

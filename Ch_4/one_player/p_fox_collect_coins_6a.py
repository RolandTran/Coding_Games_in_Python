import pygame
import pgzrun
from random import randint, choice

WIDTH, HEIGHT = 800, 800
score = 0
game_over = False
remaining_time = 90
paused = False
space_pressed = False

# ─── Music ───────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/jamesbondtheme.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ─── Player ──────────────────────
fox = Actor("fox", (100, 100))

# ─── Coins setup (image, value, sound) ──────────────────────
coin_data = [
    ("coin",      1.00, "hitcoin"),
    ("penny",     0.01, "hitpenny"),
    ("nickel",    0.05, "hitnickel"),
    ("dime",      0.10, "hitdime"),
    ("quarter",   0.25, "hitquarter"),
    ("halfdollar",0.50, "hithalfdollar"),
    ("dollar",    1.00, "hitdollar"),
]

coins = []
for name, value, sound in coin_data:
    c = Actor(name)
    c.actor_name = name
    c.value = value
    c.sound = sound
    c.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)
    c.dx, c.dy = choice([-3, -2, -1, 1, 2, 3]), choice([-3, -2, -1, 1, 2, 3])
    c.angle = 0
    coins.append(c)

# ─── Rules text ──────────────────────
rules_text = """
PAUSED - GAME RULES:

- Move the fox with arrow keys.
- Collect coins to increase your USD.
- The game ends when you reach $100 or the timer runs out.
- Press SPACE to pause or resume the game.
"""

# ─── Draw ──────────────────────
def draw():
    screen.fill("white")
    fox.draw()
    for c in coins: c.draw()

    screen.draw.text(f"Score: {round(score,2)} USD", topright=(WIDTH-15, 10), fontsize=30, color="black")
    screen.draw.text(f"Time: {remaining_time}s", topleft=(10, 10), fontsize=30, color="black")

    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150, 150, WIDTH - 300, HEIGHT - 300), color="white", align="left")
    if game_over:
        screen.fill("pink")
        msg = "You won!" if score >= 100 else "Time's up!"
        screen.draw.text(f"{msg} Final score: {round(score,2)} USD", center=(WIDTH//2, HEIGHT//2), fontsize=50, color="red")

# ─── Timer ──────────────────────
def close_game():
    quit()

def update_timer():
    global remaining_time, game_over
    if not paused and not game_over:
        remaining_time -= 1
        if remaining_time <= 0:
            sounds.miss.play()
            game_over = True
            clock.schedule_unique(close_game, 3.0)
    clock.schedule_unique(update_timer, 1.0)

# ─── Update ──────────────────────
def update():
    global paused, space_pressed, score, game_over

    # Pause toggle
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
    elif not keyboard.space:
        space_pressed = False

    if paused or game_over: return

    # Move coins
    for c in coins:
        c.x += c.dx
        c.y += c.dy
        if c.left < 0 or c.right > WIDTH: c.dx *= -1
        if c.top < 0 or c.bottom > HEIGHT: c.dy *= -1
        c.angle = (c.angle + 5) % 360

    # Move player
    if keyboard.left:  fox.x -= 6
    if keyboard.right: fox.x += 6
    if keyboard.up:    fox.y -= 6
    if keyboard.down:  fox.y += 6

    # Collisions
    for c in coins:
        if fox.colliderect(c):
            getattr(sounds, c.sound).play()
            score += c.value
            # speed up coin
            c.dx = max(min(c.dx + (1 if c.dx>0 else -1), 10), -10)
            c.dy = max(min(c.dy + (1 if c.dy>0 else -1), 10), -10)
            c.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)
            print(f"Your score is {score:.2f} USD")

    # Win condition
    if score >= 100:
        game_over = True

# ─── Start timer ──────────────────────
clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

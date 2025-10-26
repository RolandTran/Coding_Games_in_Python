import pygame
import pgzrun
from random import randint

WIDTH, HEIGHT = 800, 800
score, time_left = 0, 60
paused = game_over = space_pressed = False

# ─── Music setup ───────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/jamesbondtheme.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Coin values and margin and sounds
coin_data = {
    coin: (1.00, 20, "hitcoin"),
    penny: (0.01, 25, "hitpenny"),
    nickel: (0.05, 15, "hitnickel"),
    dime: (0.10, 20, "hitdime"),
    quarter: (0.25, 25, "hitquarter"),
    halfdollar: (0.50, 15, "hithalfdollar"),
    dollar: (1.00, 15, "hitdollar"),
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
    print("Closing game...in 1.5s")
    quit()

def update_timer():
    global time_left, game_over
    if not paused and not game_over:
        time_left -= 1
        if time_left <= 0:
            game_over = True
            print(f"Time's up! Final score: {round(score,2)}")
            clock.schedule_unique(close_game, 1.5)
    clock.schedule_unique(update_timer, 1.0)

# ─── Update Loop ───────────────────────
def update():
    global paused, space_pressed
    # allow pause/suesm toggle always when not game_over
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
        # stop all other updateds if puased or game is over
        if paused or game_over: 
            pygame.mixer.music.pause()
            return # skip any game logic
        else:
            pygame.mixer.music.unpause()
            clock.schedule_unique(update_timer, 1.0)
    elif not keyboard.space:
        space_pressed = False

#------ Mouse function ---------
def on_mouse_down(pos):
    global score
    if paused or game_over:
        return
    hit = False
    for actor, (value, margin, sound) in coin_data.items():
        if actor.collidepoint(pos):
            sounds[sound].play()
            score += value
            print(f"You clicked on the {actor.image}! Your score is {round(score, 2)} USD.")
            actor.pos = (randint(margin, WIDTH - margin), randint(margin, HEIGHT - margin))
            hit = True
            break
    if not hit:
        sounds.miss.play()
        print(f"You missed! Game over! Your final score is {round(score, 2)}")
        clock.schedule_unique(close_game, 1.5)
        
place_all()
clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

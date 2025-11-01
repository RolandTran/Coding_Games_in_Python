import pgzrun
from random import randint
import pygame

WIDTH, HEIGHT = 800, 800
score, remaining_time = 0, 90
game_over, paused, space_pressed = False, False, False

# ─── Music setup ───────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/jamesbondtheme.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ─── Player ────────────────────────────
fox = Actor("fox", (100, 100))

# ─── Coins: actor, value, sound ────────
coins = {
    "coin":      (Actor("coin"),      1.00, sounds.hitcoin),
    "penny":     (Actor("penny"),     0.01, sounds.hitpenny),
    "nickel":    (Actor("nickel"),    0.05, sounds.hitnickel),
    "dime":      (Actor("dime"),      0.10, sounds.hitdime),
    "quarter":   (Actor("quarter"),   0.25, sounds.hitquarter),
    "halfdollar":(Actor("halfdollar"),0.50, sounds.hithalfdollar),
    "dollar":    (Actor("dollar"),    1.00, sounds.hitdollar),
}

# Random placement
def place(actor):
    actor.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

for name, (actor, _, _) in coins.items():
    place(actor)

# ─── Rules text ────────────────────────
rules_text = """
PAUSED - GAME RULES:

- Move the fox with arrow keys.
- Collect coins to increase your USD.
- The game ends when you reach $100 or the timer runs out.
- Press SPACE to pause or resume the game.
"""

# ─── Draw Loop ─────────────────────────
def draw():
    screen.fill("white")
    fox.draw()
    for actor, _, _ in coins.values():
        actor.draw()

    screen.draw.text(f"Score: {score:.2f} USD", topright=(WIDTH-15, 10), fontsize=30, color="black")
    screen.draw.text(f"Time: {remaining_time}s", topleft=(10, 10), fontsize=30, color="black")

    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150,150,WIDTH-300,HEIGHT-300), color="white", align="left")

    if game_over:
        screen.fill("pink")
        screen.draw.text(f"Final score: {score:.2f} USD", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")

# ─── Timer ─────────────────────────────
def close_game():
    print("Closing game..."); quit()

def update_timer():
    global remaining_time, game_over
    if not paused and not game_over:
        remaining_time -= 1
        if remaining_time <= 0:
            sounds.miss.play()
            game_over = True
            print(f"Time's up! Final score {score:.2f} USD")
            clock.schedule_unique(close_game, 3.0)
        else:
            clock.schedule_unique(update_timer, 1.0)
    else:
        clock.schedule_unique(update_timer, 1.0)

# ─── Update Loop ───────────────────────
def update():
    global paused, space_pressed, score, game_over
    if keyboard.space and not space_pressed and not game_over:
        paused, space_pressed = not paused, True
    elif not keyboard.space:
        space_pressed = False
    if paused or game_over: return

    # Movement
    if keyboard.left:  fox.x -= 6
    if keyboard.right: fox.x += 6
    if keyboard.up:    fox.y -= 6
    if keyboard.down:  fox.y += 6

    # Coin collisions
    for actor, value, sound in coins.values():
        if fox.colliderect(actor):
            sound.play()
            score += value
            print(f"Your score is {score:.2f} USD")
            place(actor)

    if score >= 100:
        game_over = True

# ─── Start Game ────────────────────────
clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

import pgzrun
import pygame
from random import randint, choice

WIDTH, HEIGHT = 800, 800
score, remaining_time = 0, 90
game_over, paused, space_pressed = False, False, False

# ─── Music setup ───────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/jamesbondtheme.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ─── Player ───────────────────────────
fox = Actor("fox")
fox.pos = 100, 100

# ─── Coins setup ──────────────────────
coin_data = [
    ("coin", 1.00), ("penny", 0.01), ("nickel", 0.05),
    ("dime", 0.10), ("quarter", 0.25), ("halfdollar", 0.50), ("dollar", 1.00)
]

coins = []
for name, value in coin_data:
    actor = Actor(name)
    actor.actor_name = name            # store the coin's name
    actor.pos = randint(20, WIDTH - 20), randint(20, HEIGHT - 20)
    actor.dx, actor.dy = choice([-3, -2, -1, 1, 2, 3]), choice([-3, -2, -1, 1, 2, 3])
    actor.angle = 0
    actor.value = value
    coins.append(actor)

# ─── Rules text ───────────────────────
rules_text = """
PAUSED - GAME RULES:

- Move the fox with arrow keys.
- Collect coins to increase your USD.
- The game ends when you reach $100 or the timer runs out.
- Press SPACE to pause or resume the game.
"""

# ─── Draw ─────────────────────────────
def draw():
    screen.fill("white")
    fox.draw()
    for c in coins:
        c.draw()
    screen.draw.text(f"Score: {score:.2f} USD", topright=(WIDTH-15,10), fontsize=30, color="black")
    screen.draw.text(f"Time: {remaining_time}s", topleft=(10,10), fontsize=30, color="black")
    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150,150,WIDTH-300,HEIGHT-300), color="white", align="left")
    if game_over:
        screen.fill("pink")
        screen.draw.text(f"Time's up! Final score is {score:.2f} USD",
                         center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")

# ─── Timer ────────────────────────────
def update_timer():
    global remaining_time, game_over
    if not paused and not game_over:
        remaining_time -= 1
        if remaining_time <= 0:
            sounds.miss.play()
            game_over = True
            clock.schedule_unique(quit_game, 3.0)
        else:
            clock.schedule_unique(update_timer, 1.0)
    else:
        clock.schedule_unique(update_timer, 1.0)

def quit_game():
    print(f"Time's up! Final score was {score:.2f} USD.")
    quit()

# ─── Coin movement ────────────────────
def move_actor(a):
    a.x += a.dx
    a.y += a.dy
    if a.left < 0 or a.right > WIDTH: a.dx *= -1
    if a.top < 0 or a.bottom > HEIGHT: a.dy *= -1
    a.angle = (a.angle + 5) % 360

# ─── Update ──────────────────────────
def update():
    global paused, space_pressed, score, game_over
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
    elif not keyboard.space:
        space_pressed = False

    if paused or game_over: 
        return

    # Move coins
    for c in coins:
        move_actor(c)

    # Move player
    if keyboard.left: fox.x -= 6
    if keyboard.right: fox.x += 6
    if keyboard.up: fox.y -= 6
    if keyboard.down: fox.y += 6

    # Collisions
    for c in coins:
        if fox.colliderect(c):
            sound_name = f"hit{c.actor_name}"  # play coin's sound
            if hasattr(sounds, sound_name):
                getattr(sounds, sound_name).play()
            score += c.value
            c.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

    if score >= 100:
        game_over = True

clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

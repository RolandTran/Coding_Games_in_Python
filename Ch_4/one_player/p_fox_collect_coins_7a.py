import pygame, pgzrun
from random import randint, choice

WIDTH, HEIGHT = 800, 800
score, game_over, paused, space_pressed = 0, False, False, False
remaining_time = 90

# ─── Music ─────────────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/jamesbondtheme.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ─── Player ────────────────────────────
fox = Actor("fox", (100, 100))

# ─── Coins setup ───────────────────────
coin_data = {
    "coin": 1.00, "penny": 0.01, "nickel": 0.05,
    "dime": 0.10, "quarter": 0.25, "halfdollar": 0.50,
    "dollar": 1.00
}
coins = []
for name, value in coin_data.items():
    c = Actor(name, (randint(20, WIDTH-20), randint(20, HEIGHT-20)))
    c.dx, c.dy = choice([-3, -2, -1, 1, 2, 3]), choice([-3, -2, -1, 1, 2, 3])
    c.angle, c.value, c.actor_name = 0, value, name
    coins.append(c)

# ─── Rules text ────────────────────────
rules_text = """
PAUSED - GAME RULES:

- Move the fox with arrow keys.
- Collect coins to increase your USD.
- The game ends when you reach $100 or the timer runs out.
- Press SPACE to pause or resume the game.
"""

def draw():
    screen.fill("white")
    fox.draw()
    for c in coins: c.draw()
    screen.draw.text(f"Score: {round(score,2)} USD", topright=(WIDTH-15, 10), fontsize=30, color="black")
    screen.draw.text(f"Time: {remaining_time}s", topleft=(10, 10), fontsize=30, color="black")
    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150, 150, WIDTH-300, HEIGHT-300), color="white", align="left")
    if game_over:
        screen.fill("pink")
        msg = "You won!" if score >= 100 else f"Time's up! Final score is {round(score,2)} USD"
        screen.draw.text(msg, center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")

def close_game(): quit()

def update_timer():
    global remaining_time, game_over
    if not paused and not game_over:
        remaining_time -= 1
        if remaining_time <= 0:
            sounds.miss.play()
            game_over = True
            clock.schedule_unique(close_game, 3.0)
        else:
            clock.schedule_unique(update_timer, 1.0)
    else:
        clock.schedule_unique(update_timer, 1.0)

def move_coin(c):
    c.x += c.dx; c.y += c.dy
    if c.left < 0 or c.right > WIDTH: c.dx *= -1
    if c.top < 0 or c.bottom > HEIGHT: c.dy *= -1
    c.angle = (c.angle + 5) % 360

def update():
    global paused, space_pressed, score, game_over
    if keyboard.space and not space_pressed and not game_over:
        paused, space_pressed = not paused, True
    elif not keyboard.space: space_pressed = False
    if paused or game_over: return

    # Fox movement
    if keyboard.left: fox.x -= 6
    if keyboard.right: fox.x += 6
    if keyboard.up: fox.y -= 6
    if keyboard.down: fox.y += 6

    # Coins update
    for c in coins:
        move_coin(c)
        if fox.colliderect(c):
            getattr(sounds, f"hit{c.actor_name}").play()
            score += c.value
            c.dx += 1 if c.dx > 0 else -1
            c.dy += 1 if c.dy > 0 else -1
            c.dx, c.dy = max(min(c.dx, 10), -10), max(min(c.dy, 10), -10)
            c.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)
            print(f"Your score is {score:.2f} USD")

    if score >= 100: game_over = True

clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

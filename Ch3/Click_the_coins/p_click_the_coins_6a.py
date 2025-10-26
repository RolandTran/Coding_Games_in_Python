import pygame
import pgzrun
from random import randint, choice

score, time_left, paused, game_over, space_pressed = 0, 60, False, False, False
WIDTH, HEIGHT = 800, 800

pygame.mixer.init()
pygame.mixer.music.load("music/jamesbondtheme.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ─── Coin Setup ───
coin_data = [
    ("coin", 1.00), ("penny", 0.01), ("nickel", 0.05), ("dime", 0.10),
    ("quarter", 0.25), ("halfdollar", 0.50), ("dollar", 1.00)
]
coins = {}

for name, value in coin_data:
    actor = Actor(name)
    actor.pos = (randint(10, WIDTH), randint(10, HEIGHT))
    actor.dx = choice([-3, -2, -1, 1, 2, 3])
    actor.dy = choice([-3, -2, -1, 1, 2, 3])
    coins[name] = {"actor": actor, "value": value}
    actor.angle = 0
    coins[name] = {"actor": actor, "value": value}

# -------- Rules text ---------------------
rules_text = """
PAUSED - GAME RULES:

- Click the coins by moving the mouse cursor over it and clicking.
- The game will end if you click outside the coins.
- Acquire the most USD
- Press SPACE to pause or resume the game.
"""

def draw():
    screen.fill("white")
    for data in coins.values():
        data["actor"].draw()
    screen.draw.text(f"Score: {round(score,2)} USD", topright=(WIDTH-15, 10), fontsize=30, color="black")
    screen.draw.text(f"Time: {time_left}s", topleft=(10, 10), fontsize=30, color="black")
    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150, 150, WIDTH - 300, HEIGHT - 300), color="white", align="left")
    if game_over:
        screen.draw.text(f"Time's up! Final score is {round(score,2)}", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")

def close_game():
    print("Closing game...in 1.5s")
    quit()

def update_timer():
    global time_left, game_over
    if not paused and not game_over:
        time_left -= 1
        if time_left <= 0:
            game_over = True
            print(f"Time's up! Your final score was {score}.")
            clock.schedule_unique(close_game, 1.5)
        else:
            clock.schedule_unique(update_timer, 1.0)

def move_coins():
    for data in coins.values():
        actor = data["actor"]
        actor.x += actor.dx
        actor.y += actor.dy
        if actor.left < 0 or actor.right > WIDTH: actor.dx *= -1
        if actor.top < 0 or actor.bottom > HEIGHT: actor.dy *= -1
        actor.angle = (actor.angle + 5) % 360  # Rotate

def update():
    global paused, space_pressed
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
        pygame.mixer.music.pause() if paused else pygame.mixer.music.unpause()
        if not paused: clock.schedule_unique(update_timer, 1.0)
    elif not keyboard.space:
        space_pressed = False
    if not paused and not game_over: move_coins()

def on_mouse_down(pos):
    global score
    if paused or game_over:
        return

    for name, data in coins.items():
        actor = data["actor"]
        if actor.collidepoint(pos):
            # Play sound dynamically
            getattr(sounds, f"hit{name}").play()

            # Update score
            score += data["value"]

            # Increase and clamp speed
            actor.dx += 1 if actor.dx > 0 else -1
            actor.dy += 1 if actor.dy > 0 else -1
            actor.dx = max(min(actor.dx, 10), -10)
            actor.dy = max(min(actor.dy, 10), -10)

            # Reposition coin
            actor.pos = (randint(20, WIDTH - 20), randint(20, HEIGHT - 20))

            print(f"You clicked on the {name}! Your score is {round(score, 2)} USD.")
            return

    # If no coin was clicked
    sounds.miss.play()
    print(f"You missed! Game over! Your final score is {round(score, 2)}")
    clock.schedule_unique(close_game, 1.0)


clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

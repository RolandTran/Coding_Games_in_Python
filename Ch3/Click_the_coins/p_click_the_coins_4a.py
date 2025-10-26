import pygame
import pgzrun
from random import randint, choice

WIDTH, HEIGHT, score, time_left = 800, 800, 0, 60
paused = game_over = space_pressed = False

# ─── Music Setup ───
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

rules_text = """
PAUSED - GAME RULES:
- Click the coins by moving the mouse cursor over it and clicking.
- The game will end if you click outside the coins.
- Acquire the most USD
- Press SPACE to pause or resume the game.
"""

def draw():
    screen.fill("white")
    for coin in coins.values():
        coin["actor"].draw()
    screen.draw.text(f"Score: {round(score, 2)} USD", topright=(WIDTH - 15, 10), fontsize=30, color="black")
    screen.draw.text(f"Time: {time_left}s", topleft=(10, 10), fontsize=30, color="black")
    if paused:
        screen.draw.filled_rect(Rect(100, 100, WIDTH - 200, HEIGHT - 200), (0, 0, 0, 180))
        screen.draw.textbox(rules_text.strip(), Rect(150, 150, WIDTH - 300, HEIGHT - 300), color="white", align="left")
    if game_over:
        screen.draw.text(f"Time's up! Final score is {round(score, 2)}", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")

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
            clock.schedule_unique(close_game, 3.0)
        else:
            clock.schedule_unique(update_timer, 1.0)
    else:
        clock.schedule_unique(update_timer, 1.0)

def update():
    global paused, space_pressed
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
        if paused or game_over:
            pygame.mixer.music.pause()
            return
        else:
            pygame.mixer.music.unpause()
            clock.schedule_unique(update_timer, 1.0)
    elif not keyboard.space:
        space_pressed = False

    if not paused and not game_over:
        for coin in coins.values():
            actor = coin["actor"]
            actor.x += actor.dx
            actor.y += actor.dy
            if actor.left < 0 or actor.right > WIDTH:
                actor.dx *= -1
            if actor.top < 0 or actor.bottom > HEIGHT:
                actor.dy *= -1

def on_mouse_down(pos):
    global score
    if paused or game_over:
        return

    for name, data in coins.items():
        actor = data["actor"]
        if actor.collidepoint(pos):
            getattr(sounds, f"hit{name}").play()
            score += data["value"]
            actor.pos = (randint(20, WIDTH - 20), randint(20, HEIGHT - 20))
            print(f"You clicked on the {name}! Score: {round(score, 2)} USD.")
            return

    sounds.miss.play()
    print(f"You missed! Game over! Your final score is {round(score, 2)}")
    clock.schedule_unique(close_game, 1.5)

clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

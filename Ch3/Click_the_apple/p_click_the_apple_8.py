import pygame
import pgzrun
from random import randint, choice
from datetime import datetime
import string

# ─── Window setup ─────────────────────
WIDTH = 800
HEIGHT = 800

# ─── Music setup ───────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/chicagobullstheme.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ─── Game state ────────────────────────
score = 0
remaining_time = 60
paused = False
game_over = False
space_pressed = False
speed_level = 1

# ─── Actor setup ───────────────────────
apple = Actor("apple")
apple.pos = (randint(10, WIDTH - 10), randint(10, HEIGHT - 10))
apple.dx = choice([-3, -2, -1, 1, 2, 3])
apple.dy = choice([-3, -2, -1, 1, 2, 3])
apple.angle = 0

# ─── Rules text ────────────────────────
rules_text = """
PAUSED - GAME RULES:

- Click the apple by moving the mouse cursor over it and clicking.
- The game will end if you click outside the apple.
- Press SPACE to pause or resume the game.
"""

# ─── Initials input ─────────────────────
initials = ""
input_active = False
MAX_INITIALS = 3
score_saved = False

TOP3_FILE = "top3scores_click_the_apple.txt"

# ─── High Score Helpers ─────────────────
def load_top3():
    top3 = []
    try:
        with open(TOP3_FILE, "r") as f:
            for line in f:
                name, val, date_str = line.strip().split(",")
                top3.append((name, int(val), date_str))
    except FileNotFoundError:
        pass
    return top3

def save_top3(top3):
    with open(TOP3_FILE, "w") as f:
        for name, val, date_str in top3:
            f.write(f"{name},{val},{date_str}\n")

def add_to_top3(name, val):
    now = datetime.now().strftime("%Y-%m-%d")
    top3 = load_top3()
    top3.append((name, val, now))
    top3 = sorted(top3, key=lambda x: x[1], reverse=True)[:3]
    save_top3(top3)
    return top3

def place_apple():
    apple.pos = (randint(10, WIDTH - apple.width), randint(10, HEIGHT - apple.height))

# ─── Draw Function ─────────────────────
def draw():
    screen.clear()
    if game_over:
        screen.fill("black")
        screen.draw.text("Game Over", center=(WIDTH // 2, 100), fontsize=60, color="white")
        screen.draw.text("Enter Your Initials:", topleft=(100, 200), fontsize=40, color="white")
        screen.draw.text(initials, topleft=(100, 260), fontsize=60, color="yellow")

        if score_saved:
            screen.draw.text("Score Saved!", topleft=(100, 340), fontsize=40, color="green")

        top3 = load_top3()
        screen.draw.text("Top 3 High Scores:", topleft=(450, 150), fontsize=30, color="white")
        for i, (name, val, date_str) in enumerate(top3, start=1):
            screen.draw.text(f"{i}. {name} — {val} ({date_str})", topleft=(450, 150 + i * 40), fontsize=28, color="white")

    else:
        apple.draw()
        screen.draw.text(f"Score: {score}", topright=(WIDTH - 15, 10), fontsize=30, color="white")
        screen.draw.text(f"Time: {remaining_time}s", topleft=(10, 10), fontsize=30, color="white")
        screen.draw.text(f"Difficulty: {speed_level}", midtop=(WIDTH // 2, 10), fontsize=30, color="yellow")

        if paused:
            screen.draw.filled_rect(Rect(50, 50, WIDTH - 100, HEIGHT - 100), (20, 20, 20, 200))
            screen.draw.textbox(rules_text.strip(), Rect(100, 100, WIDTH - 200, HEIGHT - 200), color="white", align="left")

# ─── Close Game ────────────────────────
def close_game():
    print("Closing game...")
    quit()

# ─── Timer Logic ───────────────────────
def update_timer():
    global remaining_time, game_over, input_active
    if not paused and not game_over:
        remaining_time -= 1
        if remaining_time <= 0:
            game_over = True
            input_active = True
            pygame.mixer.music.fadeout(1000)
        else:
            clock.schedule_unique(update_timer, 1.0)
    else:
        clock.schedule_unique(update_timer, 1.0)

# ─── Apple Movement ────────────────────
def move_apple():
    apple.x += apple.dx
    apple.y += apple.dy

    if apple.left < 0 or apple.right > WIDTH:
        apple.dx *= -1
    if apple.top < 0 or apple.bottom > HEIGHT:
        apple.dy *= -1

    apple.angle = (apple.angle + 5) % 360

# ─── Update Loop ───────────────────────
def update():
    global paused, space_pressed, input_active
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
        if paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
            clock.schedule_unique(update_timer, 1.0)
    elif not keyboard.space:
        space_pressed = False

    if not paused and not game_over:
        move_apple()

# ─── Mouse Logic ───────────────────────
def on_mouse_down(pos):
    global score, speed_level, game_over, input_active
    if not game_over and not paused:
        if apple.collidepoint(pos):
            sounds.hitapple.play()
            score += 1
            apple.dx += 1 if apple.dx > 0 else -1
            apple.dy += 1 if apple.dy > 0 else -1
            speed_level = max(abs(apple.dx), abs(apple.dy))
            place_apple()
        else:
            sounds.miss.play()
            print("Missed! Game over.")
            game_over = True
            input_active = True
            pygame.mixer.music.fadeout(1000)

# ─── Keyboard Logic ────────────────────
def on_key_down(key):
    global initials, input_active, score_saved
    if input_active and not score_saved:
        if key.name in string.ascii_uppercase and len(initials) < MAX_INITIALS:
            initials += key.name
        elif key == keys.BACKSPACE and initials:
            initials = initials[:-1]
        elif key == keys.RETURN and len(initials) == MAX_INITIALS:
            add_to_top3(initials, score)
            score_saved = True
            print("Score saved:", initials, score)
            clock.schedule_unique(close_game, 5.0)

# ─── Start Game ────────────────────────
place_apple()
clock.schedule_unique(update_timer, 1.0)

pgzrun.go()


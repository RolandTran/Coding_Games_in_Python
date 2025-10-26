import pygame
import pgzrun
from random import randint, choice

# ─── Window setup ─────────────────────
WIDTH = 800
HEIGHT = 800

# ─── Music setup ───────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/chicagobullstheme.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop indefinitely

# ─── Game state ────────────────────────
score = 0
remaining_time = 60
paused = False
game_over = False
space_pressed = False

# ─── Actor setup ───────────────────────
apple = Actor("apple")
apple.pos = (randint(10, WIDTH - 10), randint(10, HEIGHT - 10))
apple.dx = choice([-3, -2, -1, 1, 2, 3])
apple.dy = choice([-3, -2, -1, 1, 2, 3])
apple.angle = 0  # start rotation

# ─── Rules text ────────────────────────
rules_text = """
PAUSED - GAME RULES:

- Click the apple by moving the mouse cursor over it and clicking.
- The game will end if you click outside the apple.
- Press SPACE to pause or resume the game.
"""

def place_apple():
    apple.pos = (randint(10, WIDTH - apple.width), randint(10, HEIGHT - apple.height))
    apple.dx = choice([-3, -2, -1, 1, 2, 3])
    apple.dy = choice([-3, -2, -1, 1, 2, 3])

# ─── Draw Function ─────────────────────
def draw():
    screen.clear()
    if game_over:
        screen.fill("black")
        screen.draw.text("Game Over!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="white")
    else:
        apple.draw()
        screen.draw.text(f"Score: {score}", topright=(WIDTH - 15, 10), fontsize=30, color="white")
        screen.draw.text(f"Time: {remaining_time}s", topleft=(10, 10), fontsize=30, color="white")

        if paused:
            screen.draw.filled_rect(Rect(50, 50, WIDTH - 100, HEIGHT - 100), (20, 20, 20, 200))  # Optional transparency
            screen.draw.textbox(rules_text.strip(), Rect(100, 100, WIDTH - 200, HEIGHT - 200), color="white", align="left")


# ─── Close Game ────────────────────────
def close_game():
    print("Closing game...")
    quit()

# ─── Timer Logic ───────────────────────
def update_timer():
    global remaining_time, game_over
    if not paused and not game_over:
        remaining_time -= 1
        if remaining_time <= 0:
            game_over = True
            print(f"Time's up! Your final score was {score}.")
            clock.schedule_unique(close_game, 3.0)
        else:
            clock.schedule_unique(update_timer, 1.0)
    else:
        # Keep checking every second while paused
        clock.schedule_unique(update_timer, 1.0)

# ─── Apple Movement ────────────────────
def move_apple():
    apple.x += apple.dx
    apple.y += apple.dy

    # Bounce off walls
    if apple.left < 0 or apple.right > WIDTH:
        apple.dx *= -1
    if apple.top < 0 or apple.bottom > HEIGHT:
        apple.dy *= -1
        
    # Rotate the apple
    apple.angle = (apple.angle + 5) % 360  # rotates clockwise 5 degrees per frame

# ─── Update Loop ───────────────────────
def update():
    global paused, space_pressed
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
    global score
    if not game_over and not paused:
        if apple.collidepoint(pos):
            sounds.hitapple.play()
            score += 1
            print(f"Good shot! Score: {score}")
            place_apple()
        else:
            sounds.miss.play()
            print("Missed! Game over in 3s")
            clock.schedule_unique(close_game, 3.0)

# ─── Start Timer ───────────────────────
place_apple()
clock.schedule_unique(update_timer, 1.0)

pgzrun.go()

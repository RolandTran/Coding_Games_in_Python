import pygame, pgzrun
from random import randint

# ─── State ─────────────────────────────
score, remaining_time = 0, 90
paused = game_over = space_pressed = False
WIDTH, HEIGHT = 800, 800

# ─── Music ─────────────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/chicagobullstheme.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ─── Actors ────────────────────────────
apple, pineapple, orange = Actor("apple"), Actor("pineapple"), Actor("orange")
for a in (apple, pineapple, orange): a.pos = (randint(10, WIDTH), randint(10, HEIGHT))

rules_text = """
PAUSED - GAME RULES:

- Click the apple to score.
- Orange & Pineapple = mistakes.
- Clicking outside apple ends game.
- Press SPACE to pause/resume.
"""

# ─── Helpers ───────────────────────────
def place(actor, margin=20): actor.pos = (randint(margin, WIDTH-margin), randint(margin, HEIGHT-margin))
def close_game(): print("Closing game..."); quit()

# ─── Timer ─────────────────────────────
def update_timer():
    global remaining_time, game_over
    if not paused and not game_over:
        remaining_time -= 1
        if remaining_time <= 0:
            game_over = True
            print(f"Time's up! Final score: {score}")
            clock.schedule_unique(close_game, 1.5)
        else: clock.schedule_unique(update_timer, 1.0)
    else: clock.schedule_unique(update_timer, 1.0)

# ─── Draw ──────────────────────────────
def draw():
    screen.clear()
    for a in (apple, pineapple, orange): a.draw()
    screen.draw.text(f"Score: {score}", topright=(WIDTH-15,10), fontsize=30, color="white")
    screen.draw.text(f"Time: {remaining_time}s", topleft=(10,10), fontsize=30, color="white")
    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150,150,WIDTH-300,HEIGHT-300), color="white", align="left")
    if game_over:
        screen.draw.text("Time's up!", center=(WIDTH//2, HEIGHT//2+60), fontsize=60, color="red")

# ─── Update ────────────────────────────
def update():
    global paused, space_pressed
    if keyboard.space and not space_pressed and not game_over:
        paused, space_pressed = not paused, True
        (pygame.mixer.music.pause() if paused else pygame.mixer.music.unpause())
        if not paused: clock.schedule_unique(update_timer, 1.0)
    elif not keyboard.space: space_pressed = False
    if paused or game_over: return

# ─── Mouse ─────────────────────────────
def on_mouse_down(pos):
    global score
    if paused or game_over: return
    if apple.collidepoint(pos):
        sounds.hitapple.play(); score += 1
        print(f"Apple! Score: {score}"); place(apple)
    elif pineapple.collidepoint(pos):
        sounds.hitpineapple.play(); print("Pineapple!"); place(pineapple)
    elif orange.collidepoint(pos):
        sounds.hitorange.play(); print("Orange!"); place(orange)
    else:
        sounds.miss.play(); print("Missed! Game over!")
        clock.schedule_unique(close_game, 2.0)

# ─── Init ──────────────────────────────
for a in (apple, pineapple, orange): place(a)
clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

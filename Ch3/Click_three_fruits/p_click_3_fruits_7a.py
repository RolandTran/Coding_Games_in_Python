import pygame, pgzrun
from random import randint, choice

# ─── Game state ────────────────────────
score, remaining_time = 0, 99
paused, game_over, space_pressed, speed_level = False, False, False, 1

# ─── Window setup ─────────────────────
WIDTH, HEIGHT = 800, 800

# ─── Music setup ───────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/chicagobullstheme.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ─── Fruit Factory ─────────────────────
def make_fruit(name, margin=20):
    f = Actor(name, (randint(margin, WIDTH-margin), randint(margin, HEIGHT-margin)))
    f.dx, f.dy, f.angle, f.margin = choice([-3,-2,-1,1,2,3]), choice([-3,-2,-1,1,2,3]), 0, margin
    return f

apple, pineapple, orange = make_fruit("apple",20), make_fruit("pineapple",25), make_fruit("orange",25)

# ─── Rules ─────────────────────────────
rules_text = """
PAUSED - GAME RULES:

- Click the apple to score.
- Other fruits are mistakes.
- Clicking outside the apple ends the game.
- Press SPACE to pause or resume.
"""

# ─── Draw ──────────────────────────────
def draw():
    screen.clear()
    for f in (apple, pineapple, orange): f.draw()
    screen.draw.text(f"Score: {score}", topright=(WIDTH-15,10), fontsize=30, color="white")
    screen.draw.text(f"Time: {remaining_time}s", topleft=(10,10), fontsize=30, color="white")
    screen.draw.text(f"Difficulty: {speed_level}", midtop=(WIDTH//2,10), fontsize=30, color="yellow")
    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150,150,WIDTH-300,HEIGHT-300), color="white", align="left")
    if game_over:
        screen.draw.text("Time's up! Game is over!", center=(WIDTH//2, HEIGHT//2+60), fontsize=60, color="red")

# ─── Helpers ───────────────────────────
def close_game(): quit()

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

def move_fruit(f):
    f.x, f.y = f.x + f.dx, f.y + f.dy
    if f.left < 0 or f.right > WIDTH: f.dx *= -1
    if f.top < 0 or f.bottom > HEIGHT: f.dy *= -1
    f.angle = (f.angle + 5) % 360

def place_fruit(f):
    f.pos = (randint(f.margin, WIDTH-f.margin), randint(f.margin, HEIGHT-f.margin))

def speed_up(f):
    f.dx += 1 if f.dx > 0 else -1
    f.dy += 1 if f.dy > 0 else -1
    f.dx, f.dy = max(min(f.dx,10),-10), max(min(f.dy,10),-10)

# ─── Update Loop ───────────────────────
def update():
    global paused, space_pressed
    if keyboard.space and not space_pressed and not game_over:
        paused, space_pressed = not paused, True
        if paused: pygame.mixer.music.pause()
        else: pygame.mixer.music.unpause(); clock.schedule_unique(update_timer,1.0)
        return
    elif not keyboard.space: space_pressed = False
    if not paused and not game_over:
        for f in (apple,pineapple,orange): move_fruit(f)

# ─── Mouse Logic ───────────────────────   
def on_mouse_down(pos):
    global score, speed_level
    if paused or game_over: return
    if apple.collidepoint(pos):
        sounds.hitapple.play(); score += 1; speed_up(apple); speed_level = max(abs(apple.dx),abs(apple.dy)); place_fruit(apple)
    elif pineapple.collidepoint(pos):
        sounds.hitpineapple.play(); speed_up(pineapple); place_fruit(pineapple)
    elif orange.collidepoint(pos):
        sounds.hitorange.play(); speed_up(orange); place_fruit(orange)
    else:
        sounds.miss.play(); print("Missed! Game over in 1.5s!"); clock.schedule_unique(close_game,1.5)

# ─── Start ─────────────────────────────
for f in (apple,pineapple,orange): place_fruit(f)
clock.schedule_unique(update_timer,1.0)
pgzrun.go()

import pygame, pgzrun
from random import randint, choice

# ─── Game state ────────────────────────
score, remaining_time = 0, 60
paused, game_over, space_pressed = False, False, False

# ─── Window setup ─────────────────────
WIDTH, HEIGHT = 800, 800

# ─── Music setup ───────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/chicagobullstheme.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ─── Fruit Factory ─────────────────────
def make_fruit(name, margin=20):
    f = Actor(name, (randint(margin, WIDTH - margin), randint(margin, HEIGHT - margin)))
    f.dx, f.dy, f.angle = choice([-3,-2,-1,1,2,3]), choice([-3,-2,-1,1,2,3]), 0
    return f

apple, pineapple, orange = make_fruit("apple"), make_fruit("pineapple"), make_fruit("orange")

# ─── Rules ─────────────────────────────
rules_text = """
PAUSED - GAME RULES:

- Click the apple to score.
- Clicking other fruits is a mistake.
- Clicking outside the apple ends the game.
- Press SPACE to pause or resume.
"""

# ─── Draw ──────────────────────────────
def draw():
    screen.clear()
    for f in (apple, pineapple, orange): f.draw()
    screen.draw.text(f"Score: {score}", topright=(WIDTH-15,10), fontsize=30, color="white")
    screen.draw.text(f"Time: {remaining_time}s", topleft=(10,10), fontsize=30, color="white")
    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150,150,WIDTH-300,HEIGHT-300), color="white", align="left")
    if game_over:
        screen.draw.text("Time's up!", center=(WIDTH//2, HEIGHT//2+60), fontsize=60, color="red")

# ─── Game Logic ────────────────────────
def close_game(): print("Closing game.."), quit()

def update_timer():
    global remaining_time, game_over
    if not paused and not game_over:
        remaining_time -= 1
        if remaining_time <= 0:
            game_over = True
            print(f"Time's up! Final score: {score}.")
            clock.schedule_unique(close_game, 1.5)
        else: clock.schedule_unique(update_timer, 1.0)
    else: clock.schedule_unique(update_timer, 1.0)

def move_fruit(f):
    f.x, f.y = f.x + f.dx, f.y + f.dy
    if f.left < 0 or f.right > WIDTH: f.dx *= -1
    if f.top < 0 or f.bottom > HEIGHT: f.dy *= -1
    f.angle = (f.angle + 5) % 360

def place_fruit(f, margin=20):
    f.pos = (randint(margin, WIDTH-margin), randint(margin, HEIGHT-margin))
    f.dx, f.dy = choice([-3,-2,-1,1,2,3]), choice([-3,-2,-1,1,2,3])

def update():
    global paused, space_pressed
    if keyboard.space and not space_pressed and not game_over:
        paused, space_pressed = not paused, True
        if paused: pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
            clock.schedule_unique(update_timer, 1.0)
        return
    elif not keyboard.space: space_pressed = False
    if not paused and not game_over:
        for f in (apple, pineapple, orange): move_fruit(f)

def on_mouse_down(pos):
    global score
    if paused or game_over: return
    if apple.collidepoint(pos):
        sounds.hitapple.play(); score += 1; place_fruit(apple)
    elif pineapple.collidepoint(pos):
        sounds.hitpineapple.play(); place_fruit(pineapple, 25)
    elif orange.collidepoint(pos):
        sounds.hitorange.play(); place_fruit(orange, 25)
    else:
        sounds.miss.play(); print("Missed! Game over in 1.5s!")
        clock.schedule_unique(close_game, 1.5)

# ─── Start ─────────────────────────────
clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

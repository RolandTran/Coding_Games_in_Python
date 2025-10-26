import pygame
import pgzrun
from random import randint, choice

# ─── Game state ────────────────────────
score, remaining_time, paused, game_over, space_pressed = 0, 90, False, False, False

# ─── Window setup ─────────────────────
WIDTH, HEIGHT = 800, 800

# ─── Music setup ───────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/chicagobullstheme.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ─── Actor setup ───────────────────────
fruits = {
    'apple': Actor("apple", (randint(10, WIDTH), randint(10, HEIGHT))),
    'pineapple': Actor("pineapple", (randint(10, WIDTH), randint(10, HEIGHT))),
    'orange': Actor("orange", (randint(10, WIDTH), randint(10, HEIGHT)))
}

for fruit in fruits.values():
    fruit.dx, fruit.dy = choice([-3, -2, -1, 1, 2, 3]), choice([-3, -2, -1, 1, 2, 3])

rules_text = """
PAUSED - GAME RULES:
- Click the apple to score. Avoid other fruits.
- Game ends if you click outside the apple.
- Press SPACE to pause/resume.
"""

# ─── Draw Function ─────────────────────
def draw():
    screen.clear()
    for fruit in fruits.values():
        fruit.draw()
    screen.draw.text(f"Score: {score}", topright=(WIDTH-15, 10), fontsize=30, color="white")
    screen.draw.text(f"Time: {remaining_time}s", topleft=(10, 10), fontsize=30, color="white")
    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150, 150, WIDTH - 300, HEIGHT - 300), color="white", align="left")
    if game_over:
        screen.draw.text("Time's up!", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=60, color="red")

# ─── Place Fruit ───────────────────────
def place_fruit(fruit):
    fruit.x, fruit.y = randint(20, WIDTH-20), randint(20, HEIGHT-20)
    fruit.dx, fruit.dy = choice([-3, -2, -1, 1, 2, 3]), choice([-3, -2, -1, 1, 2, 3])

# ─── Timer Logic ───────────────────────
def update_timer():
    global remaining_time, game_over
    if not paused and not game_over:
        remaining_time -= 1
        if remaining_time <= 0:
            game_over = True
            print(f"Time's up! Your final score was {score}.")
            clock.schedule_unique(close_game, 1.5)
        else:
            clock.schedule_unique(update_timer, 1.0)

# ─── Fruit Movement ────────────────────
def move_fruit(fruit):
    fruit.x += fruit.dx
    fruit.y += fruit.dy
    if fruit.left < 0 or fruit.right > WIDTH: fruit.dx *= -1
    if fruit.top < 0 or fruit.bottom > HEIGHT: fruit.dy *= -1

# ─── Update Loop ───────────────────────
def update():
    global paused, space_pressed
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
        if paused or game_over:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
            clock.schedule_unique(update_timer, 1.0)
    elif not keyboard.space:
        space_pressed = False

    if not paused and not game_over:
        for fruit in fruits.values():
            move_fruit(fruit)

# ─── Mouse Logic ───────────────────────   
def on_mouse_down(pos):
    global score
    if paused or game_over:
        return

    for name, fruit in fruits.items():
        if fruit.collidepoint(pos):
            if name == 'apple':
                sounds.hitapple.play()
                print(f"Good shot! Your score is {score}")
                score += 1
            else:
                sounds[f"hit{name}"].play()
                print(f"Oops! You clicked on the {name} by mistake!")
            place_fruit(fruit)
            return
    sounds.miss.play()
    print("You missed! Game over in 1.5s!")
    clock.schedule_unique(close_game, 1.5)

# ─── Close Game ────────────────────────
def close_game():
    print("Closing game...")
    quit()

# ─── Start Position ───────────────────────
for fruit in fruits.values():
    place_fruit(fruit)

# ─── Start Timer ───────────────────────
clock.schedule_unique(update_timer, 1.0)

pgzrun.go()

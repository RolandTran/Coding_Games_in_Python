import pgzrun
from random import randint

score, remaining_time = 0, 60
paused = game_over = space_pressed = False

WIDTH, HEIGHT = 800, 800

# Actors
apple, pineapple, orange = Actor("apple"), Actor("pineapple"), Actor("orange")

for actor in (apple, pineapple, orange):
    actor.pos = (randint(10, WIDTH), randint(10, HEIGHT))

rules_text = """
PAUSED - GAME RULES:

- Click the apple to score.
- Game ends if you click outside the apple.
- Press SPACE to pause/resume.
"""

def draw():
    screen.clear()
    for actor in (apple, pineapple, orange): actor.draw()
    screen.draw.text(f"Score: {score}", topright=(WIDTH-15, 10), fontsize=30, color="white")
    screen.draw.text(f"Time: {remaining_time}s", topleft=(10, 10), fontsize=30, color="white")
    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150,150,WIDTH-300,HEIGHT-300), color="white", align="left")
    if game_over:
        screen.draw.text("Time's up!", center=(WIDTH//2, HEIGHT//2+60), fontsize=60, color="red")

def place(actor, margin=20): actor.pos = (randint(margin, WIDTH-margin), randint(margin, HEIGHT-margin))

def close_game():
    print("Closing game..."); quit()

def update_timer():
    global remaining_time, game_over
    if not paused and not game_over:
        remaining_time -= 1
        if remaining_time <= 0:
            game_over = True
            print(f"Time's up! Final score: {score}.")
            clock.schedule_unique(close_game, 3.0)
        else: clock.schedule_unique(update_timer, 1.0)
    else: clock.schedule_unique(update_timer, 1.0)

def update():
    global paused, space_pressed
    if keyboard.space and not space_pressed and not game_over:
        paused, space_pressed = not paused, True
    elif not keyboard.space: space_pressed = False
    if paused or game_over: return

def on_mouse_down(pos):
    global score
    if paused or game_over: return
    if apple.collidepoint(pos):
        score += 1; print(f"Hit! Score: {score}"); place(apple)
    elif pineapple.collidepoint(pos):
        print("Oops! Pineapple!"); place(pineapple)
    elif orange.collidepoint(pos):
        print("Oops! Orange!"); place(orange)
    else:
        print("Missed! Game over!"); clock.schedule_unique(close_game, 2.0)

for actor in (apple, pineapple, orange): place(actor)
clock.schedule_unique(update_timer, 1.0)

pgzrun.go()

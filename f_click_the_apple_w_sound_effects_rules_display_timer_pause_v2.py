import pgzrun
from random import randint

WIDTH, HEIGHT = 800, 600
apple = Actor("apple", (randint(50, WIDTH - 50), randint(50, HEIGHT - 50)))
remaining_time, paused, game_over, space_pressed = 30, False, False, False

rules_text = """
PAUSED - GAME RULES:

- Click the apple by moving the mouse cursor over it and clicking.
- The game will end if you click outside the apple.
- Press SPACE to pause or resume the game.
"""

def place_apple():
    apple.pos = (randint(10, WIDTH - apple.width), randint(10, HEIGHT - apple.height))

def close_game():
    print("Closing game..."); quit()

def draw():
    screen.clear()
    if game_over:
        screen.fill("black")
        screen.draw.text("Game Over!", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="white")
        clock.schedule_unique(close_game, 5.0)
    else:
        apple.draw()
        screen.draw.text(f"Time Left: {remaining_time}s", topleft=(10, 10), color="white")
        if paused:
            screen.draw.filled_rect(Rect(50, 50, WIDTH - 100, HEIGHT - 100), (20, 20, 20))
            screen.draw.textbox(rules_text, Rect(100, 100, WIDTH - 200, HEIGHT - 200), color="white")

def update_timer():
    global remaining_time, game_over
    if not paused and not game_over:
        remaining_time -= 1
        if remaining_time <= 0:
            game_over = True
        else:
            clock.schedule_unique(update_timer, 1.0)

def update():
    global paused, space_pressed
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
        if not paused:
            clock.schedule_unique(update_timer, 1.0)
    elif not keyboard.space:
        space_pressed = False

def on_mouse_down(pos):
    global game_over
    if apple.collidepoint(pos):
        print("Good shot!"); sounds.hitapple.play(); place_apple()
    else:
        print("Game over!"); sounds.miss.play(); game_over = True; clock.schedule_unique(close_game, 5.0)

place_apple()
clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

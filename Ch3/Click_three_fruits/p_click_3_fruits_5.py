import pygame
import pgzrun
from random import randint, choice

# ─── Game state ────────────────────────
score = 0
remaining_time = 90
paused = False
game_over = False
space_pressed = False

# ─── Window setup ─────────────────────
WIDTH = 800
HEIGHT = 800

# ─── Music setup ───────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/chicagobullstheme.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ─── Actor setup ───────────────────────
apple = Actor("apple")
apple.pos = (randint(10, WIDTH), randint(10, HEIGHT))
apple.dx = choice([-3, -2, -1, 1, 2, 3])
apple.dy = choice([-3, -2, -1, 1, 2, 3])

pineapple = Actor("pineapple")
pineapple.pos = (randint(10, WIDTH), randint(10, HEIGHT))
pineapple.dx = choice([-3, -2, -1, 1, 2, 3])
pineapple.dy = choice([-3, -2, -1, 1, 2, 3])

orange = Actor("orange")
orange.pos = (randint(10, WIDTH), randint(10, HEIGHT))
orange.dx = choice([-3, -2, -1, 1, 2, 3])
orange.dy = choice([-3, -2, -1, 1, 2, 3])

# -------- Rules text ---------------------
rules_text = """
PAUSED - GAME RULES:

- Click the apple by moving the mouse cursor over it and clicking.
- Other fruits are by mistake
- The game will end if you click outside the apple.
- Press SPACE to pause or resume the game.
"""

# ─── Draw Function ─────────────────────
def draw():
    screen.clear()
    apple.draw()
    pineapple.draw()
    orange.draw()
    screen.draw.text(f"Score: {score}", topright=(WIDTH-15, 10), fontsize=30, color="white")
    screen.draw.text(f"Time: {remaining_time}s", topleft=(10, 10), fontsize=30, color="white")
    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150, 150, WIDTH - 300, HEIGHT - 300), color="white", align="left")
    if game_over:
        screen.draw.text("Time's up!", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=60, color="red")


def place_apple():
    apple.x = randint(20, WIDTH - 20)
    apple.y = randint(20, HEIGHT - 20)
    apple.dx = choice([-3, -2, -1, 1, 2, 3])
    apple.dy = choice([-3, -2, -1, 1, 2, 3])

def place_orange():
    orange.x = randint(25, WIDTH - 15)
    orange.y = randint(25, HEIGHT - 15)
    orange.dx = choice([-3, -2, -1, 1, 2, 3])
    orange.dy = choice([-3, -2, -1, 1, 2, 3])

def place_pineapple():
    pineapple.x = randint(15, WIDTH - 25)
    pineapple.y = randint(15, HEIGHT - 25)
    pineapple.dx = choice([-3, -2, -1, 1, 2, 3])
    pineapple.dy = choice([-3, -2, -1, 1, 2, 3])

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
            clock.schedule_unique(close_game, 1.5)
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

# ───Pineapple Movement ────────────────────
def move_pineapple():
    pineapple.x += pineapple.dx
    pineapple.y += pineapple.dy

    # Bounce off walls
    if pineapple.left < 0 or pineapple.right > WIDTH:
        pineapple.dx *= -1
    if pineapple.top < 0 or pineapple.bottom > HEIGHT:
        pineapple.dy *= -1

# ─── Orange Movement ────────────────────
def move_orange():
    orange.x += orange.dx
    orange.y += orange.dy

    # Bounce off walls
    if orange.left < 0 or orange.right > WIDTH:
        orange.dx *= -1
    if orange.top < 0 or orange.bottom > HEIGHT:
        orange.dy *= -1

# ─── Update Loop ───────────────────────
def update():
    global paused, space_pressed
    # allow pause/suesm toggle always when not game_over
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
        # stop all other updateds if puased or game is over
        if paused or game_over: 
            pygame.mixer.music.pause()
            return # skip any game logic
        else:
            pygame.mixer.music.unpause()
            clock.schedule_unique(update_timer, 1.0)
    elif not keyboard.space:
        space_pressed = False
    
    if not paused and not game_over:
        move_apple()
        move_pineapple()
        move_orange()
    
# ─── Mouse Logic ───────────────────────   
def on_mouse_down(pos):
    global score # score is global level and must be declared
    if paused or game_over:
        return # ignore all clicks if the game is paused or over
    
    if apple.collidepoint(pos):
        sounds.hitapple.play()
        print(f"Good shot! You hit the apple! Your score is {score}")
        score += 1
        place_apple()
    elif pineapple.collidepoint(pos):
        sounds.hitpineapple.play()
        print("Oops! You clicked on the pineapple by mistake!")
        place_pineapple()
    elif orange.collidepoint(pos):
        sounds.hitorange.play()
        print("Oops! You clicked on the orange by mistake!")
        place_orange()
    else:
        sounds.miss.play()
        print("You missed! Game over in 1.5s!")
        clock.schedule_unique(close_game, 1.5)


# ─── Start Position ───────────────────────
place_apple()
place_pineapple()
place_orange()

# ─── Start Timer ───────────────────────
clock.schedule_unique(update_timer, 1.0)

pgzrun.go()
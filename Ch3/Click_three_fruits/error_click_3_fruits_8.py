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
speed_level = 1  # Track difficulty based on speed

# ─── Actor setup ───────────────────────
apple = Actor("apple")
apple.pos = (randint(10, WIDTH), randint(10, HEIGHT))
apple.dx = choice([-3, -2, -1, 1, 2, 3])
apple.dy = choice([-3, -2, -1, 1, 2, 3])
apple.angle = 0  # start apple rotation

pineapple = Actor("pineapple")
pineapple.pos = (randint(10, WIDTH), randint(10, HEIGHT))
pineapple.dx = choice([-3, -2, -1, 1, 2, 3])
pineapple.dy = choice([-3, -2, -1, 1, 2, 3])
pineapple.angle = 0  # start pine rotation

orange = Actor("orange")
orange.pos = (randint(10, WIDTH), randint(10, HEIGHT))
orange.dx = choice([-3, -2, -1, 1, 2, 3])
orange.dy = choice([-3, -2, -1, 1, 2, 3])
orange.angle = 0  # start orange rotation

# -------- Rules text ---------------------
rules_text = """
PAUSED - GAME RULES:

- Click the apple by moving the mouse cursor over it and clicking.
- Other fruits are by mistake
- The game will end if you click outside the apple.
- Press SPACE to pause or resume the game.
"""

# ─── Initials input ─────────────────────
initials = ""
input_active = False
MAX_INITIALS = 3
score_saved = False

Top3_File = "top3scores_click_three_fruits.txt"

# ─── High Score Helpers ─────────────────
def load_top3():
    top3 = []
    try:
        with open(Top3_File, "r") as f:
            for line in f:
                name, val, date_str = line.strip().split(",")
                top3.append((name, int(val), date_str))
    except FileNotFoundError:
        pass
    return top3

def save_top3(top3):
    with open(Top3_File, "w") as f:
        for name, val, date_str in top3:
            f.write(f"{name},{val},{date_str}\n")

def add_to_top3(name, val):
    now = datetime.now().strftime("%Y-%m-%d")
    top3 = load_top3()
    top3.append((name, val, now))
    top3 = sorted(top3, key=lambda x: x[1], reverse=True)[:3]
    save_top3(top3)
    return top3

# ─── Draw Function ─────────────────────
def draw():
    screen.clear()
    apple.draw()
    pineapple.draw()
    orange.draw()
    screen.draw.text(f"Score: {score}", topright=(WIDTH-15, 10), fontsize=30, color="white")
    screen.draw.text(f"Time: {remaining_time}s", topleft=(10, 10), fontsize=30, color="white")
    screen.draw.text(f"Difficulty: {speed_level}", midtop=(WIDTH // 2, 10), fontsize=30, color="yellow")
    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150, 150, WIDTH - 300, HEIGHT - 300), color="white", align="left")
    if game_over:
        screen.fill("black")
        screen.draw.text("Time's up! Game is over!", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=60, color="red")
        screen.draw.text("Enter Your Initials:", topleft=(100, 200), fontsize=40, color="white")
        screen.draw.text(initials, topleft=(100, 260), fontsize=60, color="yellow")
        
        if score_saved:
            screen.draw.text("Score Saved!", topleft=(100, 340), fontsize=40, color="green")

        top3 = load_top3()
        screen.draw.text("Top 3 High Scores:", topleft=(450, 150), fontsize=30, color="white")
        for i, (name, val, date_str) in enumerate(top3, start=1):
            screen.draw.text(f"{i}. {name} — {val} ({date_str})", topleft=(450, 150 + i * 40), fontsize=28, color="white")


def place_apple():
    apple.x = randint(20, WIDTH - 20)
    apple.y = randint(20, HEIGHT - 20)

def place_orange():
    orange.x = randint(25, WIDTH - 15)
    orange.y = randint(25, HEIGHT - 15)

def place_pineapple():
    pineapple.x = randint(15, WIDTH - 25)
    pineapple.y = randint(15, HEIGHT - 25)

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
            print(f"Time's up! Your final score was {score}.")
            clock.schedule_unique(close_game, 1.5)
        else:
            clock.schedule_unique(update_timer, 1.0)
    else:
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

# ───Pineapple Movement ────────────────────
def move_pineapple():
    pineapple.x += pineapple.dx
    pineapple.y += pineapple.dy

    # Bounce off walls
    if pineapple.left < 0 or pineapple.right > WIDTH:
        pineapple.dx *= -1
    if pineapple.top < 0 or pineapple.bottom > HEIGHT:
        pineapple.dy *= -1
    
    # Rotate the pineapple
    pineapple.angle = (pineapple.angle + 5) % 360  # rotates clockwise 5 degrees per frame

# ─── Orange Movement ────────────────────
def move_orange():
    orange.x += orange.dx
    orange.y += orange.dy

    # Bounce off walls
    if orange.left < 0 or orange.right > WIDTH:
        orange.dx *= -1
    if orange.top < 0 or orange.bottom > HEIGHT:
        orange.dy *= -1
    
    # Rotate the orange
    orange.angle = (orange.angle + 5) % 360  # rotates clockwise 5 degrees per frame

# ─── Update Loop ───────────────────────
def update():
    global paused, space_pressed, input_active
    # allow pause/suesm toggle always when not game_over
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
        # stop all other updateds if puased or game is over
        if paused: 
            pygame.mixer.music.pause()
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
    global score, speed_level, game_over, input_active # score is global level and must be declared
    if paused or game_over:
        return # ignore all clicks if the game is paused or over
    # collision with actors
    if apple.collidepoint(pos):
        sounds.hitapple.play()
        print(f"Good shot! You hit the apple! Your score is {score}")
        score += 1
        # Increase speed
        apple.dx += 1 if apple.dx > 0 else -1
        apple.dy += 1 if apple.dy > 0 else -1
        # Cap max speed (optional)
        apple.dx = max(min(apple.dx, 10), -10)
        apple.dy = max(min(apple.dy, 10), -10)
        # update difficult level
        speed_level = max(abs(apple.dx), abs(apple.dy))
        place_apple()
    elif pineapple.collidepoint(pos):
        sounds.hitpineapple.play()
        print("Oops! You clicked on the pineapple by mistake!")
        # Increase pineapple speed
        pineapple.dx += 1 if pineapple.dx > 0 else -1
        pineapple.dy += 1 if pineapple.dy > 0 else -1
        pineapple.dx = max(min(pineapple.dx, 10), -10)
        pineapple.dy = max(min(pineapple.dy, 10), -10)
        place_pineapple()
    elif orange.collidepoint(pos):
        sounds.hitorange.play()
        print("Oops! You clicked on the orange by mistake!")
        # Increase orange speed
        orange.dx += 1 if orange.dx > 0 else -1
        orange.dy += 1 if orange.dy > 0 else -1
        orange.dx = max(min(orange.dx, 10), -10)
        orange.dy = max(min(orange.dy, 10), -10)
        place_orange()
    else:
        sounds.miss.play()
        print("You missed! Game over in 5.0s!")
        clock.schedule_unique(close_game, 5.0)

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


# ─── Start Position ───────────────────────
place_apple()
place_pineapple()
place_orange()

# ─── Start Timer ───────────────────────
clock.schedule_unique(update_timer, 1.0)

pgzrun.go()
import pygame, pgzrun, string
from random import randint, choice
from datetime import datetime

WIDTH, HEIGHT = 800, 800

pygame.mixer.init()
pygame.mixer.music.load("music/chicagobullstheme.mp3")  # or .wav
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

score = 0
remaining_time = 60
paused = False
game_over = False
space_pressed = False
speed_level = 1

# Setup fruits with common properties
def make_fruit(name):
    a = Actor(name)
    a.pos = (randint(10, WIDTH), randint(10, HEIGHT))
    a.dx = choice([-3, -2, -1, 1, 2, 3])
    a.dy = choice([-3, -2, -1, 1, 2, 3])
    a.angle = 0
    return a

apple = make_fruit("apple")
pineapple = make_fruit("pineapple")
orange = make_fruit("orange")

rules_text = """
PAUSED - GAME RULES:

- Click the apple by moving the mouse cursor over it and clicking.
- Other fruits are by mistake
- The game will end if you click outside the apple.
- Press SPACE to pause or resume the game.
"""

initials = ""
input_active = False
MAX_INITIALS = 3
score_saved = False
Top3_File = "top3scores_click_three_fruits.txt"

def load_top3():
    try:
        with open(Top3_File) as f:
            return [ (n,int(v),d) for n,v,d in (line.strip().split(",") for line in f) ]
    except FileNotFoundError:
        return []

def save_top3(top3):
    with open(Top3_File, "w") as f:
        f.writelines(f"{n},{v},{d}\n" for n,v,d in top3)

def add_to_top3(name, val):
    now = datetime.now().strftime("%Y-%m-%d")
    top3 = load_top3()
    top3.append((name,val,now))
    top3 = sorted(top3, key=lambda x: x[1], reverse=True)[:3]
    save_top3(top3)
    return top3

def place(f):
    margin = 20
    f.x = randint(margin, WIDTH - margin)
    f.y = randint(margin, HEIGHT - margin)

def draw():
    screen.clear()
    if game_over:
        screen.fill("black")
        screen.draw.text("Time's up! Game is over!", center=(WIDTH//2, HEIGHT//2 + 60), fontsize=60, color="red")
        screen.draw.text("Enter Your Initials:", topleft=(100, 200), fontsize=40, color="white")
        screen.draw.text(initials, topleft=(100, 260), fontsize=60, color="yellow")
        screen.draw.text("Press Enter to Save", topleft=(100, 320), fontsize=30, color="white")
        if score_saved:
            screen.draw.text("Score Saved!", topleft=(100, 340), fontsize=40, color="green")
        top3 = load_top3()
        screen.draw.text("Top 3 High Scores:", topleft=(450, 150), fontsize=30, color="white")
        for i, (n,v,d) in enumerate(top3, 1):
            screen.draw.text(f"{i}. {n} — {v} ({d})", topleft=(450, 150 + i*40), fontsize=28, color="white")
    else:
        for f in (apple, pineapple, orange):
            f.draw()
        screen.draw.text(f"Score: {score}", topright=(WIDTH-15, 10), fontsize=30, color="white")
        screen.draw.text(f"Time: {remaining_time}s", topleft=(10,10), fontsize=30, color="white")
        screen.draw.text(f"Difficulty: {speed_level}", midtop=(WIDTH//2, 10), fontsize=30, color="yellow")
        if paused:
            screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200), (0,0,0,180))
            screen.draw.textbox(rules_text.strip(), Rect(150,150,WIDTH-300,HEIGHT-300), color="white", align="left")

def close_game():
    print("Closing game...")
    quit()

def update_timer():
    global remaining_time, game_over, input_active
    if not paused and not game_over:
        remaining_time -= 1
        if remaining_time <= 0:
            game_over = True
            input_active = True
            print(f"Time's up! Your final score was {score}.")
            pygame.mixer.music.fadeout(1000)
            clock.schedule_unique(close_game, 5)
        else:
            clock.schedule_unique(update_timer, 1)
    else:
        clock.schedule_unique(update_timer, 1)

def move(f):
    f.x += f.dx
    f.y += f.dy
    if f.left < 0 or f.right > WIDTH: f.dx *= -1
    if f.top < 0 or f.bottom > HEIGHT: f.dy *= -1
    f.angle = (f.angle + 5) % 360

def update():
    global paused, space_pressed
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
        if paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
            clock.schedule_unique(update_timer, 1)
    elif not keyboard.space:
        space_pressed = False
    if not paused and not game_over:
        for f in (apple, pineapple, orange):
            move(f)

def on_mouse_down(pos):
    global score, speed_level, game_over, input_active
    if paused or game_over: return
    def speed_up(f):
        f.dx = max(min(f.dx + (1 if f.dx > 0 else -1), 10), -10)
        f.dy = max(min(f.dy + (1 if f.dy > 0 else -1), 10), -10)
    for fruit, sound, msg, inc_score in [
        (apple, sounds.hitapple, f"Good shot! Your score is {score+1}", True),
        (pineapple, sounds.hitpineapple, "Oops! You clicked on the pineapple by mistake!", False),
        (orange, sounds.hitorange, "Oops! You clicked on the orange by mistake!", False),
    ]:
        if fruit.collidepoint(pos):
            sound.play()
            speed_up(fruit)
            place(fruit)
            if inc_score:
                score += 1
                speed_level = max(abs(fruit.dx), abs(fruit.dy))
            print(msg)
            return
    sounds.miss.play()
    game_over = input_active = True
    pygame.mixer.music.fadeout(1000)
    clock.schedule_unique(close_game, 5)
    print("You missed! Game over in 5.0s!")

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
            clock.schedule_unique(close_game, 5)

for f in (apple, pineapple, orange): place(f)
clock.schedule_unique(update_timer, 1)

pgzrun.go()

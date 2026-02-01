import pygame, pgzrun
from random import randint, choice
from datetime import datetime

WIDTH = 800
HEIGHT = 800

# ─── Game State ─────────────────────────
score_fox = 0.0
score_clicker = 0.0
fox_speed = 2
paused = False
space_pressed = False
game_over = False
time_left = 90
flash_time = 0

entering_initials = False
winner_label = ""
winner_score = 0.0
initials = ""
score_saved = False
MAX_INITIALS = 3

Top3_File = "top3scores_collect_the_coins_fox_vs_clicker.txt"

# ─── Music ──────────────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/jamesbondtheme.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ─── Actors ─────────────────────────────
fox = Actor("fox")

coin_defs = [
    ("coin", 1.00),
    ("penny", 0.01),
    ("nickel", 0.05),
    ("dime", 0.10),
    ("quarter", 0.25),
    ("halfdollar", 0.50),
    ("dollar", 1.00),
]

coins = []

def place(a):
    a.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

for name, value in coin_defs:
    a = Actor(name)
    a.dx = choice([-3, -2, -1, 1, 2, 3])
    a.dy = choice([-3, -2, -1, 1, 2, 3])
    a.rot_speed = 5
    a.value = value
    place(a)
    coins.append(a)

place(fox)

# ─── Leaderboard ────────────────────────
def load_top3():
    try:
        with open(Top3_File) as f:
            data = []
            for line in f:
                p = line.strip().split(",")
                if len(p) == 3:
                    n, v, d = p
                    w = "Unknown"
                else:
                    n, v, d, w = p
                data.append((n, float(v), d, w))
            return data
    except FileNotFoundError:
        return []

def save_top3(top3):
    with open(Top3_File, "w") as f:
        for entry in top3:
            if len(entry) == 4:
                n, v, d, w = entry
                f.write(f"{n},{v},{d},{w}\n")

def add_to_top3(name, val, winner):
    now = datetime.now().strftime("%Y-%m-%d")
    top3 = load_top3()
    top3.append((name, val, now, winner))
    top3 = sorted(top3, key=lambda x: x[1], reverse=True)[:3]
    save_top3(top3)
    return top3

# ─── Effects ────────────────────────────
def flash():
    global flash_time

# --- Restart ---
def restart_game():
    global score_fox, score_clicker, time_left, paused, game_over, flash_time

    score_fox = score_clicker = 0.0
    time_left = 90
    flash_time = 2.0
    paused = False
    game_over = False

    # Re-place everything
    place(fox)
    for c in coins:
        place(c)
        c.dx = choice([-3, -2, -1, 1, 2, 3])
        c.dy = choice([-3, -2, -1, 1, 2, 3])


# ─── Movement ───────────────────────────
def move_actor(a):
    a.x += a.dx
    a.y += a.dy

    if a.left < 0 or a.right > WIDTH:
        a.dx *= -1
    if a.top < 0 or a.bottom > HEIGHT:
        a.dy *= -1

    a.angle = (a.angle + a.rot_speed) % 360

def close_game():
    print("Closing game...in 10s")
    quit()

def print_winner():
    if score_fox > score_clicker: print("Fox Wins! 🦊")
    elif score_clicker > score_fox: print("Clicker Wins! 🖱️")
    else: print("Tie Game! 🤝")
    print(f"Final Scores — Fox: {score_fox:.2f}, Clicker: {score_clicker:.2f}")
    
# ─── Timer ──────────────────────────────
def end_game():
    global game_over, entering_initials, winner_label, winner_score
    game_over = True
    if score_fox >= score_clicker:
        winner_label = "Fox"
        winner_score = score_fox
    else:
        winner_label = "Clicker"
        winner_score = score_clicker
    entering_initials = True
    print_winner()

# --- Timer ---
def update_timer():
    global time_left
    if not paused and not game_over:
        time_left -= 1
        if time_left <= 0:
            clock.schedule_unique(close_game, 10.0)
            end_game()
        else:
            clock.schedule_unique(update_timer, 1.0)
    else:
        clock.schedule_unique(update_timer, 1.0)


# ─── Draw ───────────────────────────────
def draw():
    screen.fill("white")
    top3 = load_top3()

    if not game_over:
        fox.draw()
        for c in coins:
            c.draw()

        screen.draw.text(f"Fox Score: {score_fox:.2f}", (10, 10), color="black")
        screen.draw.text(f"Clicker Score: {score_clicker:.2f}", (10, 30), color="black")
        screen.draw.text(f"Time Left: {time_left}", topright=(WIDTH-10, 10), color="red")

        if flash_time > 0:
            screen.draw.filled_rect(Rect(0,0,WIDTH,HEIGHT),(255,255,0,80))
    else:
        screen.fill("lightblue")
        screen.draw.text(
            f"{winner_label} Wins!",
            center=(WIDTH/2, 120),
            fontsize=60
        )

        screen.draw.text(
            f"Your Score: {winner_score:.2f} USD",
            center=(WIDTH/2, 200),
            fontsize=40
        )

        if entering_initials:
            screen.draw.text(
                f"ENTER INITIALS: {initials}",
                center=(WIDTH/2, 300),
                fontsize=50,
                color="darkred"
            )

        y = 420
        screen.draw.text("TOP 3 SCORES", center=(WIDTH/2, y-40), fontsize=45)
        for n, v, d, w in top3:
            screen.draw.text(
                f"{n} - {v:.2f} USD ({d}) [{w}]",
                center=(WIDTH/2, y),
                fontsize=32
            )
            y += 40

# ─── Update ─────────────────────────────
def update():
    global paused, space_pressed, score_fox, flash_time, fox_speed

    if flash_time > 0:
        flash_time -= 1

    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
        pygame.mixer.music.pause() if paused else pygame.mixer.music.unpause()
    elif not keyboard.space:
        space_pressed = False

    if paused or game_over:
        return

    for c in coins:
        move_actor(c)

    if keyboard.left: fox.x -= fox_speed
    if keyboard.right: fox.x += fox_speed
    if keyboard.up: fox.y -= fox_speed
    if keyboard.down: fox.y += fox_speed

    fox.x = max(20, min(WIDTH-20, fox.x))
    fox.y = max(20, min(HEIGHT-20, fox.y))

    for c in coins:
        if fox.colliderect(c):
            score_fox += c.value
            fox_speed += c.value
            c.rot_speed += c.value
            flash()
            place(c)

# ─── Input ──────────────────────────────
def on_key_down(key):
    global initials, entering_initials, score_saved

    if not entering_initials or score_saved:
        return

    if key.name == "BACKSPACE":
        initials = initials[:-1]
    elif key.name == "RETURN" and initials:
        add_to_top3(initials, winner_score, winner_label)
        score_saved = True
        entering_initials = False
        print("Score saved!")
    elif len(initials) < MAX_INITIALS and key.name.isalpha():
        initials += key.name.upper()

# --- Mouse clicks ---
def on_mouse_down(pos):
    global score_clicker
    if game_over:
        restart_game()
        return

    for c in coins:
        if c.collidepoint(pos):
            score_clicker += c.value
            c.rot_speed += c.value
            flash()
            place(c)
            return

# ─── Start ──────────────────────────────
clock.schedule_unique(update_timer, 1.0)

# --- Run game safely ---
try:
    pgzrun.go()
finally:
    if not game_over:
        print("\nGame closed manually — treating as Game Over!\n")
        end_game()




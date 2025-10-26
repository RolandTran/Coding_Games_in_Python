import pygame, pgzrun, string
from random import randint, choice
from datetime import datetime

score, time_left, paused, game_over, space_pressed = 0, 60, False, False, False
WIDTH, HEIGHT = 800, 800

pygame.mixer.init()
pygame.mixer.music.load("music/jamesbondtheme.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ─── Coin Setup ───
coin_data = [
    ("coin", 1.00, 20),
    ("penny", 0.01, 25),
    ("nickel", 0.05, 15),
    ("dime", 0.10, 20),
    ("quarter", 0.25, 25),
    ("halfdollar", 0.50, 15),
    ("dollar", 1.00, 15)
]

coins = {}

for name, value, margin in coin_data:
    actor = Actor(name)
    actor.pos = (randint(10, WIDTH), randint(10, HEIGHT))
    actor.dx = choice([-3, -2, -1, 1, 2, 3])
    actor.dy = choice([-3, -2, -1, 1, 2, 3])
    actor.angle = 0
    coins[name] = {"actor": actor, "value": value, "margin": margin}

# -------- Rules text ---------------------
rules_text = """
PAUSED - GAME RULES:

- Click the coins by moving the mouse cursor over it and clicking.
- The game will end if you click outside the coins.
- Acquire the most USD
- Press SPACE to pause or resume the game.
"""

initials = ""
input_active = False
MAX_INITIALS = 3
score_saved = False
Top3_File = "top3scores_click_the_coins.txt"

def load_top3():
    try:
        with open(Top3_File) as f:
            return [ (n, float(v), d) for n, v, d in (line.strip().split(",") for line in f) ]
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

def place(actor, margin=20):
    actor.pos = (randint(margin, WIDTH - margin), randint(margin, HEIGHT - margin))

def speed_up(actor, max_speed=10):
    actor.dx = max(min(actor.dx + (1 if actor.dx > 0 else -1), max_speed), -max_speed)
    actor.dy = max(min(actor.dy + (1 if actor.dy > 0 else -1), max_speed), -max_speed)

def draw():
    screen.fill("white")
    for data in coins.values():
        data["actor"].draw()
    screen.draw.text(f"Score: {round(score,2)} USD", topright=(WIDTH-15, 10), fontsize=30, color="black")
    screen.draw.text(f"Time: {time_left}s", topleft=(10, 10), fontsize=30, color="black")
    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150, 150, WIDTH - 300, HEIGHT - 300), color="white", align="left")
    if game_over:
        screen.fill("black")
        screen.draw.text(f"Time's up! Game is over! Score: {round(score,2)}.", center=(WIDTH//2, HEIGHT//2 + 60), fontsize=60, color="red")
        screen.draw.text("Enter Your Initials:", topleft=(100, 200), fontsize=40, color="white")
        screen.draw.text(initials, topleft=(100, 260), fontsize=60, color="yellow")
        screen.draw.text("Press Enter to Save", topleft=(100, 320), fontsize=30, color="white")
        if score_saved:
            screen.draw.text("Score Saved!", topleft=(100, 340), fontsize=40, color="green")
        top3 = load_top3()
        screen.draw.text("Top 3 High Scores:", topleft=(450, 150), fontsize=30, color="white")
        for i, (n,v,d) in enumerate(top3, 1):
            screen.draw.text(f"{i}. {n} — {v} ({d})", topleft=(450, 150 + i*40), fontsize=28, color="white")

def close_game():
    print("Closing game...in 5s")
    quit()

def update_timer():
    global time_left, game_over, input_active
    if not paused and not game_over:
        time_left -= 1
        if time_left <= 0:
            game_over = True
            input_active = True
            print(f"Time's up! Your final score was {score}.")
            pygame.mixer.music.fadeout(1000)
            clock.schedule_unique(close_game, 5)
        else:
            clock.schedule_unique(update_timer, 1.0)
    else:
        clock.schedule_unique(update_timer, 1.0)

def move_coins():
    for data in coins.values():
        actor = data["actor"]
        actor.x += actor.dx
        actor.y += actor.dy
        if actor.left < 0 or actor.right > WIDTH: actor.dx *= -1
        if actor.top < 0 or actor.bottom > HEIGHT: actor.dy *= -1
        actor.angle = (actor.angle + 5) % 360  # Rotate

def update():
    global paused, space_pressed
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
        pygame.mixer.music.pause() if paused else pygame.mixer.music.unpause()
        if not paused: clock.schedule_unique(update_timer, 1.0)
    elif not keyboard.space:
        space_pressed = False
    if not paused and not game_over: 
        move_coins() # move coins
        
        # Handle collisions between coins
        coin_actors = [data["actor"] for data in coins.values()]
        for i in range(len(coin_actors)):
            for j in range(i + 1, len(coin_actors)):
                if coin_actors[i].colliderect(coin_actors[j]):
                    # Reposition both coins on collision
                    coin_actors[i].pos = (randint(20, WIDTH - 20), randint(20, HEIGHT - 20))
                    coin_actors[j].pos = (randint(20, WIDTH - 20), randint(20, HEIGHT - 20))

def on_mouse_down(pos):
    global score, game_over, input_active
    if paused or game_over:
        return

    for name, data in coins.items():
        actor = data["actor"]
        if actor.collidepoint(pos):
            getattr(sounds, f"hit{name}").play()
            score += data["value"]
            speed_up(actor)  # Use helper if defined
            place(actor, data.get("margin", 20))  # Reuse placement function
            print(f"You clicked on the {name}! Your score is {round(score, 2)} USD.")
            return

    sounds.miss.play()
    print(f"You missed! Game over! Your final score is {round(score, 2)} USD.")
    game_over = input_active = True
    pygame.mixer.music.fadeout(1000)
    clock.schedule_unique(close_game, 5.0)


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

for coin in coins.values():
    place(coin["actor"], coin.get("margin", 20))

clock.schedule_unique(update_timer, 1.0)

pgzrun.go()


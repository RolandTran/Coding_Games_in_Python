import pygame, pgzrun
from random import randint, choice

WIDTH = HEIGHT = 800

# ─── Game State ─────────────────────────────
score_fox = 0.0
score_clicker = 0.0
paused = False
space_pressed = False
game_over = False
time_left = 90
flash_time = 0

# ─── Music ───────────────────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/jamesbondtheme.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ─── Coins + Values ─────────────────────────
coin_values = {
    "coin": 1.0,
    "penny": 0.01,
    "nickel": 0.05,
    "dime": 0.10,
    "quarter": 0.25,
    "halfdollar": 0.50,
    "dollar": 1.0
}

# Create all coin actors
coins = {}
for name in coin_values:
    a = Actor(name)
    a.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)
    a.dx = choice([-3, -2, -1, 1, 2, 3])
    a.dy = choice([-3, -2, -1, 1, 2, 3])
    a.angle = 0
    coins[name] = a

# Fox
fox = Actor("fox")
fox.pos = 100, 100

# ─── Helpers ────────────────────────────────
def place(a):
    a.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

def flash():
    global flash_time
    flash_time = 2.0



# ─── Draw ───────────────────────────────────
rules_text = """
PAUSED - GAME RULES:

- Fox moves with arrow keys
- Mouse/touch clicks collect coins
- Game lasts 90 seconds
- Higher score wins
- SPACE = Pause / Resume
"""

def draw():
    screen.fill("white")
    fox.draw()
    for a in coins.values(): a.draw()

    screen.draw.text(f"Fox Score: {score_fox:.2f}", (10,10), color="black")
    screen.draw.text(f"Clicker Score: {score_clicker:.2f}", (10,30), color="black")
    screen.draw.text(f"Time Left: {time_left}", topright=(WIDTH-10,10), color="red")

    if flash_time > 0:
        screen.draw.filled_rect(Rect(0,0,WIDTH,HEIGHT),(255,255,0,80))

    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150,150,WIDTH-300,HEIGHT-300), color="white")

    if game_over:
        screen.fill("lightblue")
        if score_fox > score_clicker: msg = "Fox Wins! 🦊"
        elif score_clicker > score_fox: msg = "Clicker Wins! 🖱️"
        else: msg = "It's a Tie! 🤝"
        screen.draw.text(msg, center=(400,350), fontsize=60)
        screen.draw.text(f"Fox: {score_fox:.2f} | Clicker: {score_clicker:.2f}",
                         center=(400,420), fontsize=40)
        screen.draw.text("CLICK TO RESTART", center=(400,520), fontsize=45)

def close_game():
    print("Closing game...")
    quit()

def end_game():
    global game_over
    game_over = True
    print_winner()
    
# ─── Timer ───────────────────────────────────
def update_timer():
    global time_left, game_over
    if not paused and not game_over:
        time_left -= 1
        if time_left <= 0:
            sounds.miss.play()
            game_over = True
            end_game()
            clock.schedule_unique(close_game,10)
    clock.schedule_unique(update_timer,1)

# ─── Movement ───────────────────────────────
def move_actor(a):
    a.x += a.dx
    a.y += a.dy

    if a.left < 0 or a.right > WIDTH: a.dx *= -1
    if a.top < 0 or a.bottom > HEIGHT: a.dy *= -1

    a.angle = (a.angle + 5) % 360

def print_winner():
    print("\nFINAL SCORES:")
    print(f"Fox: {score_fox:.2f} | Clicker: {score_clicker:.2f}")
    if score_fox > score_clicker: print("Fox Wins! 🦊")
    elif score_clicker > score_fox: print("Clicker Wins! 🖱️")
    else: print("Tie Game! 🤝")
    
# ─── Update ─────────────────────────────────
def update():
    global paused, space_pressed, flash_time, score_fox, game_over
    
    if flash_time > 0: 
        flash_time -= 1

    # Pause
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
        (pygame.mixer.music.pause() if paused else pygame.mixer.music.unpause())
    elif not keyboard.space:
        space_pressed = False

    if paused or game_over: return

    # Move coins
    for a in coins.values():
        move_actor(a)

    # Move fox
    if keyboard.left: fox.x -= 6
    if keyboard.right: fox.x += 6
    if keyboard.up: fox.y -= 6
    if keyboard.down: fox.y += 6
    fox.x = max(20, min(WIDTH-20, fox.x))
    fox.y = max(20, min(HEIGHT-20, fox.y))

    # Fox → coin collisions
    for name, a in coins.items():
        if fox.colliderect(a):
            getattr(sounds, "hit" + name).play()
            score_fox += coin_values[name]
            flash()
            place(a)

    # Coin-coin collisions
    all_list = list(coins.values())
    for i in range(len(all_list)):
        for j in range(i+1, len(all_list)):
            if all_list[i].colliderect(all_list[j]):
                place(all_list[i])

# ─── Mouse ───────────────────────────────────
def on_mouse_down(pos):
    global score_clicker, score_fox, game_over

    if game_over:
        restart_game()
        return

    # Clicking fox = penalty
    if fox.collidepoint(pos):
        sounds.miss.play()
        score_fox -= 0.10
        flash()
        place(fox)
        return

    # Clicking coins
    for name, a in coins.items():
        if a.collidepoint(pos):
            getattr(sounds, "hit" + name).play()
            score_clicker += coin_values[name]
            flash()
            place(a)
            return

    # Miss
    sounds.miss.play()
    score_clicker -= 0.25

def restart_game():
    global score_fox, score_clicker, time_left, paused, game_over, flash_time
    score_fox = score_clicker = 0.0
    time_left = 90
    game_over = paused = False
    flash_time = 0
    
    place(fox)
    for a in coins.values():
        place(a)
        
clock.schedule_unique(update_timer,1.0)

# Safe run
try:
    pgzrun.go()
finally:
    if not game_over:
        print("\nGame closed manually — treating as Game Over.")
        end_game()

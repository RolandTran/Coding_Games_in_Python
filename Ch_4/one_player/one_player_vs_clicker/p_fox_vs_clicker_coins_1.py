import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 800

score_fox = 0.0
score_clicker = 0.0
game_over = False
paused = False
space_pressed = False
time_left = 90  # seconds

# Player
fox = Actor("fox")
fox.pos = 100, 100

# Coins
coin = Actor("coin")
penny = Actor("penny")
nickel = Actor("nickel")
dime = Actor("dime")
quarter = Actor("quarter")
halfdollar = Actor("halfdollar")
dollar = Actor("dollar")

# Place functions
def place_fox():
    fox.x = randint(20, WIDTH-20)
    fox.y = randint(20, HEIGHT-20)

def place_coin():
    coin.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

def place_penny():
    penny.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

def place_nickel():
    nickel.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

def place_dime():
    dime.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

def place_quarter():
    quarter.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

def place_halfdollar():
    halfdollar.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

def place_dollar():
    dollar.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

# Spawn items
place_coin()
place_penny()
place_nickel()
place_dime()
place_quarter()
place_halfdollar()
place_dollar()
place_fox()

# Pause rules text
rules_text = """
PAUSED - GAME RULES:

- Fox uses arrow keys to move.
- Mouse/touch clicks collect coins.
- 90 second match; higher money wins.
- Press SPACE to pause/resume.
"""

def draw():
    screen.fill("white")

    fox.draw()
    coin.draw()
    penny.draw()
    nickel.draw()
    dime.draw()
    quarter.draw()
    halfdollar.draw()
    dollar.draw()

    screen.draw.text(f"Fox Score: {score_fox:.2f}", (10, 10), color="black")
    screen.draw.text(f"Clicker Score: {score_clicker:.2f}", (10, 30), color="black")
    screen.draw.text(f"Time Left: {time_left}", topright=(WIDTH-10, 10), color="red")

    if paused and not game_over:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(),
                            Rect(150,150,WIDTH-300,HEIGHT-300),
                            color="white")

    if game_over:
        screen.fill("lightblue")

        if score_fox > score_clicker:
            winner = "Fox Wins! 🦊"
        elif score_clicker > score_fox:
            winner = "Clicker Wins! 🖱️"
        else:
            winner = "It's a Tie! 🤝"

        screen.draw.text(winner,
                         center=(WIDTH/2, HEIGHT/2),
                         fontsize=60,
                         color="black")

        screen.draw.text(f"Fox: {score_fox:.2f} | Clicker: {score_clicker:.2f}",
                         center=(WIDTH/2, HEIGHT/2 + 60),
                         fontsize=40,
                         color="black")

def close_game():
    print("Closing game...")
    quit()

def update_timer():
    global time_left, game_over
    if not paused and not game_over:
        time_left -= 1
        if time_left <= 0:
            game_over = True
            print("Time's up!")
            clock.schedule_unique(close_game, 3.0)
        else:
            clock.schedule_unique(update_timer, 1.0)
    else:
        # Keep checking every second while paused
        clock.schedule_unique(update_timer, 1.0)
        
def update():
    global paused, space_pressed, game_over, score_fox

    # Pause toggle
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
    elif not keyboard.space:
        space_pressed = False

    if paused or game_over:
        return

    # Fox movement
    if keyboard.left: fox.x -= 6
    if keyboard.right: fox.x += 6
    if keyboard.up: fox.y -= 6
    if keyboard.down: fox.y += 6

    # Coin collisions Fox
    if fox.colliderect(coin):
        score_fox += 1.00
        place_coin()

    if fox.colliderect(penny):
        score_fox += 0.01
        place_penny()

    if fox.colliderect(nickel):
        score_fox += 0.05
        place_nickel()

    if fox.colliderect(dime):
        score_fox += 0.10
        place_dime()

    if fox.colliderect(quarter):
        score_fox += 0.25
        place_quarter()

    if fox.colliderect(halfdollar):
        score_fox += 0.50
        place_halfdollar()

    if fox.colliderect(dollar):
        score_fox += 1.00
        place_dollar()

def on_mouse_down(pos):
    global score_clicker, score_fox, game_over
    if game_over:
        return

    if fox.collidepoint(pos):
        score_fox -= 0.10
        place_fox()

    if coin.collidepoint(pos):
        score_clicker += 1.00
        place_coin()

    elif penny.collidepoint(pos):
        score_clicker += 0.01
        place_penny()

    elif nickel.collidepoint(pos):
        score_clicker += 0.05
        place_nickel()

    elif dime.collidepoint(pos):
        score_clicker += 0.10
        place_dime()

    elif quarter.collidepoint(pos):
        score_clicker += 0.25
        place_quarter()

    elif halfdollar.collidepoint(pos):
        score_clicker += 0.50
        place_halfdollar()

    elif dollar.collidepoint(pos):
        score_clicker += 1.00
        place_dollar()

clock.schedule_interval(update_timer, 1.0)
pgzrun.go()


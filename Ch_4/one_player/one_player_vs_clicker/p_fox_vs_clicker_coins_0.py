import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 800

score_fox = 0.0
score_clicker = 0.0
game_over = False
time_left = 90  # 90 seconds timer

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

# Place functions for each coin
def place_coin():
    coin.x = randint(20, WIDTH-20)
    coin.y = randint(20, HEIGHT-20)

def place_penny():
    penny.x = randint(20, WIDTH-20)
    penny.y = randint(20, HEIGHT-20)

def place_nickel():
    nickel.x = randint(20, WIDTH-20)
    nickel.y = randint(20, HEIGHT-20)

def place_dime():
    dime.x = randint(20, WIDTH-20)
    dime.y = randint(20, HEIGHT-20)

def place_quarter():
    quarter.x = randint(20, WIDTH-20)
    quarter.y = randint(20, HEIGHT-20)

def place_halfdollar():
    halfdollar.x = randint(20, WIDTH-20)
    halfdollar.y = randint(20, HEIGHT-20)

def place_dollar():
    dollar.x = randint(20, WIDTH-20)
    dollar.y = randint(20, HEIGHT-20)

# Start all coins on board
place_coin()
place_penny()
place_nickel()
place_dime()
place_quarter()
place_halfdollar()
place_dollar()

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

    screen.draw.text(f"Fox Score: {score_fox:.2f}", color="black", topleft=(10, 10))
    screen.draw.text(f"Clicker Score: {score_clicker:.2f}", color="black", topleft=(10, 30))
    screen.draw.text(f"Time Left: {time_left}", color="red", topleft=(10, 50))

    if game_over:
        screen.fill("lightblue")

        # Winner check
        if score_fox > score_clicker:
            winner = "Fox Wins! 🦊"
        elif score_clicker > score_fox:
            winner = "Clicker Wins! 🖱️"
        else:
            winner = "It's a Tie! 🤝"

        screen.draw.text(winner, center=(WIDTH/2, HEIGHT/2),
                         fontsize=60, color="black")

        screen.draw.text(f"Fox: {score_fox:.2f} | Clicker: {score_clicker:.2f}",
                         center=(WIDTH/2, HEIGHT/2 + 60),
                         fontsize=40, color="black")

def update():
    global score_fox, game_over

    if game_over:
        return

    # Movement
    if keyboard.left: fox.x -= 6
    if keyboard.right: fox.x += 6
    if keyboard.up: fox.y -= 6
    if keyboard.down: fox.y += 6

    # Fox Collisions (long way)
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
    global score_clicker

    if game_over:
        return

    # Mouse clicks (long way)
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

# Timer counts down
def countdown():
    global time_left, game_over
    if time_left > 0:
        time_left -= 1
    else:
        game_over = True

clock.schedule_interval(countdown, 1.0)

pgzrun.go()

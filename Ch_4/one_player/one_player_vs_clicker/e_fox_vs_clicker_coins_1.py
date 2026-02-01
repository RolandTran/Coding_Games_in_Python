import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 800

score_fox = 0.0
score_clicker = 0.0
game_over = False
time_left = 90  # 90 seconds timer
paused = False
space_pressed = False

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
def place_fox():
    fox.x = randint(20, WIDTH-20)
    fox.y = randint(20, HEIGHT-20
    
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
palce_fox()

# -------- Rules text ---------------------
rules_text = """
PAUSED - GAME RULES:

- Move the fox with arrow keys and the clicker with mouse or touchscreen.
- Collect coins to increase your USD.
- The game ends after 90s with and the winner being the player
with the higher score.
- Press SPACE to pause or resume the game.
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

    screen.draw.text(f"Fox Score: {score_fox:.2f}", color="black", topleft=(10, 10))
    screen.draw.text(f"Clicker Score: {score_clicker:.2f}", color="black", topleft=(10, 30))
    screen.draw.text(f"Time Left: {time_left}", color="red", topright=(WIDTH-15, 10))

    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150, 150, WIDTH - 300, HEIGHT - 300), color="white", align="left")
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

def close_game():
    print("Closing game...")
    quit()

def update_timer():
    global remaining_time, game_over
    if not paused and not game_over:
        remaining_time -= 1
        if remaining_time <= 0:
            game_over = True
            print(f"Time's up! Your final score was {score}.")
            clock.schedule_unique(close_game, 3.0)
        else:
            clock.schedule_unique(update_timer, 1.0)
    else:
        # Keep checking every second while paused
        clock.schedule_unique(update_timer, 1.0)

def update():
    global paused, space_pressed, score_clicker, score_fox, game_over
     # allow pause/suesm toggle always when not game_over
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
    elif not keyboard.space:
        space_pressed = False
        
    if paused or game_over: # stop all other updateds if puased or game is over
        return # skip any game logic

    if not game_over: 
        # Movement (allow diagonal)
        if keyboard.left:
            fox.x -= 6
        if keyboard.right:
            fox.x += 6
        if keyboard.up:
            fox.y -= 6
        if keyboard.down:
            fox.y += 6

        # Collisions with coins
        if fox.colliderect(coin):
            score += 1.00
            print(f"Your score is {score_fox:.2f} USD")
            place_coin()

        if fox.colliderect(penny):
            score += 0.01
            print(f"Your score is {score_fox:.2f} USD")
            place_penny()

        if fox.colliderect(nickel):
            score += 0.05
            print(f"Your score is {score_fox:.2f} USD")
            place_nickel()

        if fox.colliderect(dime):
            score += 0.10
            print(f"Your score is {score_fox:.2f} USD")
            place_dime()

        if fox.colliderect(quarter):
            score += 0.25
            print(f"Your score is {score_fox:.2f} USD")
            place_quarter()

        if fox.colliderect(halfdollar):
            score += 0.50
            print(f"Your score is {score_fox:.2f} USD")
            place_halfdollar()

        if fox.colliderect(dollar):
            score += 1.00
            print(f"Your score is {score_fox:.2f} USD")
            place_dollar()

        print(f"Your score is {score_fox:.2f} USD")

def on_mouse_down(pos):
    global score_clicker

    if game_over:
        return

    # Mouse clicks (long way)
    if fox.collidepoint(pos):
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

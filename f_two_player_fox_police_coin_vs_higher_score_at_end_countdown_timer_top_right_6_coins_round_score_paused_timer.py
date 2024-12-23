import pgzrun
from random import randint
import time

WIDTH = 800
HEIGHT = 800

# Scores for both players
score_fox = 0
score_police = 0
game_over = False
winner = None  # Tracks the winner

# Pause state and timing variables
paused = False
pause_start_time = 0  # Time when the game was paused
total_pause_time = 0  # Total accumulated pause duration

# Define players
fox = Actor("fox")  # Player 1
fox.pos = 100, 100

police = Actor("police")  # Player 2
police.pos = 150, 150

# Define coin
coin = Actor("coin")
coin.pos = 200, 200

quarter = Actor("quarter")
quarter.pos = 100, 200

dime = Actor("dime")
dime.pos = 150, 150

nickel = Actor("nickel")
nickel.pos = 175, 175

halfdollar = Actor("halfdollar")
halfdollar.pos = 125, 125

one = Actor("one")
one.pos = 75, 125

# Timer setup
timer_duration = 60  # 60 seconds
remaining_time = timer_duration

def draw():
    screen.fill("green")
    fox.draw()
    police.draw()
    coin.draw()
    quarter.draw()
    dime.draw()
    nickel.draw()
    halfdollar.draw()
    one.draw()

    # Display scores for both players
    screen.draw.text(f"Fox Score: {round(score_fox, 2)} USD", color="black", topleft=(10, 10))
    screen.draw.text(f"Police Score: {round(score_police, 2)} USD", color="black", topleft=(10, 30))

    # Display remaining time
    if paused:
        screen.draw.text("Paused", color="red", center=(WIDTH // 2, HEIGHT // 2), fontsize=50)
    else:
        screen.draw.text(f"Time Left: {remaining_time} seconds", color="black", topright=(750, 10))

    if game_over:
        screen.fill("pink")
        if winner == "fox":
            screen.draw.text(f"Fox Wins! {round(score_fox, 2)} USD.", topleft=(100, 200), fontsize=60, color="black")
        elif winner == "police":
            screen.draw.text(f"Police Wins! {round(score_police, 2)} USD.", topleft=(100, 200), fontsize=60, color="black")
        else:
            screen.draw.text("Game Over", topleft=(100, 200), fontsize=60, color="black")

def place_coin():
    coin.x = randint(20, WIDTH - 20)
    coin.y = randint(20, HEIGHT - 20)

def place_quarter():
    quarter.x = randint(25, WIDTH - 15)
    quarter.y = randint(25, HEIGHT - 15)

def place_dime():
    dime.x = randint(15, WIDTH - 25)
    dime.y = randint(15, HEIGHT - 25)

def place_nickel():
    nickel.x = randint(35, WIDTH - 10)
    nickel.y = randint(35, HEIGHT - 10)

def place_halfdollar():
    halfdollar.x = randint(35, WIDTH - 15)
    halfdollar.y = randint(35, HEIGHT - 15)

def place_one():
    one.x = randint(65, WIDTH - 25)
    one.y = randint(65, HEIGHT - 25)

def time_up():
    global game_over
    global winner

    game_over = True
    # Determine winner based on scores
    if score_fox > score_police:
        winner = "fox"
    elif score_police > score_fox:
        winner = "police"
    else:
        winner = None  # Tie or no one wins

def update_timer():
    global remaining_time, game_over

    if game_over or paused:
        return

    remaining_time -= 1
    if remaining_time <= 0:
        time_up()
    else:
        clock.schedule_unique(update_timer, 1.0)  # Schedule the next timer update

def update():
    global score_fox, score_police, paused, pause_start_time, total_pause_time

    # Handle pause/resume logic
    if keyboard.space:
        if not paused:
            paused = True
            pause_start_time = time.time()  # Record the time when paused
        else:
            paused = False
            total_pause_time += time.time() - pause_start_time  # Accumulate pause duration
            clock.schedule_unique(update_timer, 1.0)  # Restart the timer

    if paused or game_over:
        return  # Stop all updates when paused or game over

    # Player 1 (Fox) controls:
    if keyboard.left:
        fox.x -= 6
    elif keyboard.right:
        fox.x += 6
    elif keyboard.up:
        fox.y -= 6
    elif keyboard.down:
        fox.y += 6

    # Player 2 (Police) controls:
    if keyboard.a:
        police.x -= 6
    elif keyboard.d:
        police.x += 6
    elif keyboard.w:
        police.y -= 6
    elif keyboard.s:
        police.y += 6

    # Keep fox within bounds
    fox.x = max(0, min(WIDTH, fox.x))
    fox.y = max(0, min(HEIGHT, fox.y))

    # Keep police within bounds
    police.x = max(0, min(WIDTH, police.x))
    police.y = max(0, min(HEIGHT, police.y))

    # Collision detection with the fox and coins
    if fox.colliderect(coin):
        score_fox += 0.01
        place_coin()

    if fox.colliderect(quarter):
        score_fox += 0.250
        place_quarter()

    if fox.colliderect(dime):
        score_fox += 0.100
        place_dime()

    if fox.colliderect(nickel):
        score_fox += 0.050
        place_nickel()

    if fox.colliderect(halfdollar):
        score_fox += 0.500
        place_halfdollar()

    if fox.colliderect(one):
        score_fox += 1.00
        place_one()

    # Collision detection with the police and coins
    if police.colliderect(coin):
        score_police += 0.01
        place_coin()

    if police.colliderect(quarter):
        score_police += 0.250
        place_quarter()

    if police.colliderect(dime):
        score_police += 0.100
        place_dime()

    if police.colliderect(nickel):
        score_police += 0.050
        place_nickel()

    if police.colliderect(halfdollar):
        score_police += 0.500
        place_halfdollar()

    if police.colliderect(one):
        score_police += 1.00
        place_one()

# Schedule the timer to start
clock.schedule_unique(update_timer, 1.0)
place_coin()
place_quarter()
place_dime()
place_nickel()
place_halfdollar()
place_one()

pgzrun.go()


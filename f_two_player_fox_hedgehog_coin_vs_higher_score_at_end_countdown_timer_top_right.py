import pgzrun
from random import randint
import time

WIDTH = 800
HEIGHT = 800

# Scores for both players
score_fox = 0
score_hedgehog = 0
game_over = False
winner = None  # Tracks the winner

# Define players
fox = Actor("fox")  # Player 1
fox.pos = 100, 100

hedgehog = Actor("hedgehog")  # Player 2
hedgehog.pos = 150, 150

# Define coin
coin = Actor("coin")
coin.pos = 200, 200

# Timer setup
timer_duration = 60  # 60 seconds
remaining_time = timer_duration

def draw():
    screen.fill("green")
    fox.draw()
    hedgehog.draw()
    coin.draw()

    # Display scores for both players
    screen.draw.text(f"Fox Score: {score_fox}", color="black", topleft=(10, 10))
    screen.draw.text(f"Hedgehog Score: {score_hedgehog}", color="black", topleft=(10, 30))

    # Display remaining time
    screen.draw.text(f"Time Left: {remaining_time} seconds", color="black", topright=(700, 10))

    if game_over:
        screen.fill("pink")
        if winner == "fox":
            screen.draw.text("Fox Wins!", topleft=(100, 200), fontsize=60, color="black")
        elif winner == "hedgehog":
            screen.draw.text("Hedgehog Wins!", topleft=(100, 200), fontsize=60, color="black")
        else:
            screen.draw.text("Game Over", topleft=(100, 200), fontsize=60, color="black")

def place_coin():
    coin.x = randint(20, WIDTH - 20)
    coin.y = randint(20, HEIGHT - 20)

def time_up():
    global game_over
    global winner

    game_over = True
    # Determine winner based on scores
    if score_fox > score_hedgehog:
        winner = "fox"
    elif score_hedgehog > score_fox:
        winner = "hedgehog"
    else:
        winner = None  # Tie or no one wins

def update_timer():
    global remaining_time, game_over

    if game_over:
        return

    remaining_time -= 1
    if remaining_time <= 0:
        time_up()
    else:
        clock.schedule_unique(update_timer, 1.0)  # Schedule the next timer update

def update():
    global score_fox, score_hedgehog

    if not game_over:
        # Player 1 (Fox) controls:
        if keyboard.left:
            fox.x -= 6
        elif keyboard.right:
            fox.x += 6
        elif keyboard.up:
            fox.y -= 6
        elif keyboard.down:
            fox.y += 6

        # Player 2 (Hedgehog) controls:
        if keyboard.a:
            hedgehog.x -= 6
        elif keyboard.d:
            hedgehog.x += 6
        elif keyboard.w:
            hedgehog.y -= 6
        elif keyboard.s:
            hedgehog.y += 6

        # Keep fox within bounds
        fox.x = max(0, min(WIDTH, fox.x))
        fox.y = max(0, min(HEIGHT, fox.y))

        # Keep hedgehog within bounds
        hedgehog.x = max(0, min(WIDTH, hedgehog.x))
        hedgehog.y = max(0, min(HEIGHT, hedgehog.y))

        # Collision detection with the coin
        if fox.colliderect(coin):
            score_fox += 5
            place_coin()
        if hedgehog.colliderect(coin):
            score_hedgehog += 5
            place_coin()

# Schedule the timer to start
clock.schedule_unique(update_timer, 1.0)  # Use schedule_unique instead of schedule_once
clock.schedule_unique(time_up, timer_duration)  # Schedule the end of the game after timer_duration
place_coin()

pgzrun.go()

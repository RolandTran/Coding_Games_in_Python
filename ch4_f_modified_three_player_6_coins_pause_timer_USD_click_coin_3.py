import pgzrun
from random import randint
import time

WIDTH = 800
HEIGHT = 800

# Scores for players
score_fox = 0
score_police = 0
score_hedgehog = 0
game_over = False
winner = None  # Tracks the winner

# Pause state and timing variables
paused = False
pause_start_time = 0  # Time when the game was paused
total_pause_time = 0  # Total accumulated pause duration

#Define Players
fox = Actor("fox")  # Player 1
police = Actor("police")  # Player 2
hedgehog = Actor("hedgehog") # Player 3

players = [fox, police, hedgehog]

#Define Coins
coin = Actor("coin")
quarter = Actor("quarter")
dime = Actor("dime")
nickel = Actor("nickel")
halfdollar = Actor("halfdollar")
one = Actor("one")

coins = [coin, quarter, dime, nickel, halfdollar, one]

# Define remaining time for the game
remaining_time = 60  # Start with 60 seconds or any desired duration

def draw():
    screen.fill("green")
    for actor in players:
        actor.draw()
    for actor in coins:
        actor.draw()

    # Display scores for the players
    screen.draw.text(f"Fox Score: {round(score_fox, 2)} USD", color="black", topleft=(10, 10))
    screen.draw.text(f"Police Score: {round(score_police, 2)} USD", color="black", topleft=(10, 30))
    screen.draw.text(f"Hedgehog Score: {round(score_hedgehog, 2)} USD", color="black", topleft=(10, 50))

    # Display remaining time
    if paused:
        screen.draw.text("Paused", color="red", center=(WIDTH // 2, HEIGHT // 2), fontsize=50)
    else:
        screen.draw.text(f"Time Left: {remaining_time} seconds", color="black", topright=(750, 10))

    if game_over:
        screen.fill("pink")
        if winner == "fox":
            screen.draw.text(f"Fox Wins! {round(score_fox, 2)} USD.", topleft=(100, 100), fontsize=60, color="black")
        if winner == "hedgehog":
            screen.draw.text(f"Hedgehog Wins! {round(score_hedgehog, 2)} USD.", topleft=(100, 200), fontsize=60, color="black")
        elif winner == "police":
            screen.draw.text(f"Police Wins! {round(score_police, 2)} USD.", topleft=(100, 300), fontsize=60, color="black")
        else:
            screen.draw.text("Game Over", topleft=(100, 200), fontsize=60, color="black")

def place_coins():
    for actor in coins:
        actor.pos = (randint(10, WIDTH - 10), randint(10, HEIGHT - 10))

def place_players():
    for actor in players:
        actor.pos = (randint(10, WIDTH - 10), randint(10, HEIGHT - 10))

def time_up():
    global game_over
    global winner

    game_over = True
    # Determine winner based on scores
    if score_fox > score_police and score_fox > score_hedgehog:
        winner = "fox"
    elif score_hedgehog > score_police and score_hedgehog > score_fox:
        winner = "hedgehog"
    elif score_police > score_fox and score_police > score_hedgehog:
        winner = "police"
    else:
        winner = None  # It's a tie

def update_timer():
    global remaining_time, game_over

    if game_over or paused:
        return

    remaining_time -= 1
    if remaining_time <= 0:
        time_up()
    else:
        clock.schedule_unique(update_timer, 1.0)  # Schedule the next timer update


def on_mouse_down(pos):
    global score
    actor_clicked = False
    for actor in coins:
        if actor.collidepoint(pos):
            if actor == coin:
                print("Good shot! You click the coin!")
            if actor == quarter:
                print("Good shot! You click the quarter!")
            if actor == nickel:
                print("Good shot! You click the nickel!") 
            if actor == dime:
                print("Good shot! You click the dime!") 
            if actor == halfdollar:
                print("Good shot! You click the halfdollar!")
            elif actor == one:
                print("Good shot! YOu click the one dollar.") 
            else:
                print(f"Oops! You clicked on the {actor.image} by mistake!")
            place_coins()
            actor_clicked = True
            break

    if not actor_clicked:
        print("You missed! Continue playing through!")

def update():
    global score_fox, score_police, score_hedgehog, paused, pause_start_time, total_pause_time

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

    # Player 3 (Hedgehog) controls:
    if keyboard.j:
        hedgehog.x -= 6
    elif keyboard.l:
        hedgehog.x += 6
    elif keyboard.i:
        hedgehog.y -= 6
    elif keyboard.k:
        hedgehog.y += 6

    # Keep players within bounds
    fox.x = max(0, min(WIDTH, fox.x))
    fox.y = max(0, min(HEIGHT, fox.y))

    police.x = max(0, min(WIDTH, police.x))
    police.y = max(0, min(HEIGHT, police.y))

    hedgehog.x = max(0, min(WIDTH, hedgehog.x))
    hedgehog.y = max(0, min(HEIGHT, hedgehog.y))

    # Collision detection for all players and coins
    for player, score_var in [(fox, 'score_fox'), (police, 'score_police'), (hedgehog, 'score_hedgehog')]:
        for coin_type, value in [(coin, 0.01), (quarter, 0.25), (dime, 0.10), (nickel, 0.05), (halfdollar, 0.50), (one, 1.0)]:
            if player.colliderect(coin_type):
                globals()[score_var] += value
                place_coins()
                
# Schedule the timer to start
clock.schedule_unique(update_timer, 1.0)
place_players()  # Place the players at random positions initially
place_coins()   # Place the coins at random positions initially

pgzrun.go()  # Run the game loop


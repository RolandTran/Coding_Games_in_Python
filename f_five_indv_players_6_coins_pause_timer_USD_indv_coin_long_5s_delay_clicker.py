import pgzrun
from random import randint
import time

# size of game screen
WIDTH = 800
HEIGHT = 800

# Scores for players
score_fox = 0
score_police = 0
score_hedgehog = 0
score_blacksonic = 0
score_clicker = 0  # Mouse clicker player
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

hedgehog = Actor("hedgehog")  # Player 3
hedgehog.pos = 50, 75

blacksonic = Actor("blacksonic")  # Player 4
blacksonic.pos = 125, 175

# Define coin objects
coin = Actor("coin")
quarter = Actor("quarter")
dime = Actor("dime")
nickel = Actor("nickel")
halfdollar = Actor("halfdollar")
one = Actor("one")

# List of all coin actors
coins = [coin, quarter, dime, nickel, halfdollar, one]

# Random placement functions
def place_coin(actor):
    actor.x = randint(20, WIDTH - 20)
    actor.y = randint(20, HEIGHT - 20)

# Place all coins initially
for c in coins:
    place_coin(c)

# Timer setup
timer_duration = 60  # 60 seconds
remaining_time = timer_duration

def draw():
    screen.fill("green")
    fox.draw()
    police.draw()
    hedgehog.draw()
    blacksonic.draw()
    
    for c in coins:
        c.draw()

    # Display scores
    screen.draw.text(f"Fox score: {round(score_fox, 2)} USD", color="black", topleft=(10, 10))
    screen.draw.text(f"Police score: {round(score_police, 2)} USD", color="black", topleft=(10, 30))
    screen.draw.text(f"Hedgehog score: {round(score_hedgehog, 2)} USD", color="black", topleft=(10, 50))
    screen.draw.text(f"Blacksonic score: {round(score_blacksonic, 2)} USD", color="black", topleft=(10, 70))
    screen.draw.text(f"Clicker score: {round(score_clicker, 2)} USD", color="black", topleft=(10, 90))

    # Display remaining time
    if paused:
        screen.draw.text("Paused", color="red", center=(WIDTH // 2, HEIGHT // 2), fontsize=50)
    else:
        screen.draw.text(f"Time Left: {remaining_time} seconds", color="black", topright=(750, 10))

    if game_over:
        screen.fill("pink")
        screen.draw.text(f"{winner} wins! {round(max(score_fox, score_police, score_hedgehog, score_blacksonic, score_clicker), 2)} USD.", 
                         topleft=(100, 200), fontsize=60, color="black")

def exit_game():
    quit()

def time_up():
    global game_over, winner
    game_over = True
    
    # Determine the winner
    scores = {
        "fox": score_fox,
        "police": score_police,
        "hedgehog": score_hedgehog,
        "blacksonic": score_blacksonic,
        "clicker": score_clicker
    }
    winner = max(scores, key=scores.get)  # Get the player with the highest score
    
    # Schedule exit after 5 seconds
    clock.schedule_unique(exit_game, 5.0)

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
    global score_clicker
    for actor in coins:
        if actor.collidepoint(pos):
            if actor == coin:
                score_clicker += 0.01
            elif actor == quarter:
                score_clicker += 0.25
            elif actor == dime:
                score_clicker += 0.10
            elif actor == nickel:
                score_clicker += 0.05
            elif actor == halfdollar:
                score_clicker += 0.50
            elif actor == one:
                score_clicker += 1.00

            place_coin(actor)  # Reposition the clicked coin
            print(f"Good shot! You clicked {actor.image} and earned money!")
            return

    print("You missed! Keep playing!")

def update():
    global paused, pause_start_time, total_pause_time

    # Pause logic
    if keyboard.space:
        if not paused:
            paused = True
            pause_start_time = time.time()
        else:
            paused = False
            total_pause_time += time.time() - pause_start_time
            clock.schedule_unique(update_timer, 1.0)

    if paused or game_over:
        return  # Stop updates when paused or game over

    # Player movement
    if keyboard.left:
        fox.x -= 6
    if keyboard.right:
        fox.x += 6
    if keyboard.up:
        fox.y -= 6
    if keyboard.down:
        fox.y += 6

    if keyboard.a:
        police.x -= 6
    if keyboard.d:
        police.x += 6
    if keyboard.w:
        police.y -= 6
    if keyboard.s:
        police.y += 6

    if keyboard.f:
        hedgehog.x -= 6
    if keyboard.h:
        hedgehog.x += 6
    if keyboard.t:
        hedgehog.y -= 6
    if keyboard.g:
        hedgehog.y += 6

    if keyboard.j:
        blacksonic.x -= 6
    if keyboard.l:
        blacksonic.x += 6
    if keyboard.i:
        blacksonic.y -= 6
    if keyboard.k:
        blacksonic.y += 6

    # Keep players within bounds
    for player in [fox, police, hedgehog, blacksonic]:
        player.x = max(0, min(WIDTH, player.x))
        player.y = max(0, min(HEIGHT, player.y))

    # Collision detection for all players
    for player, score in [(fox, 'score_fox'), (police, 'score_police'), 
                          (hedgehog, 'score_hedgehog'), (blacksonic, 'score_blacksonic')]:
        for actor in coins:
            if player.colliderect(actor):
                globals()[score] += {
                    "coin": 0.01,
                    "quarter": 0.25,
                    "dime": 0.10,
                    "nickel": 0.05,
                    "halfdollar": 0.50,
                    "one": 1.00
                }[actor.image]
                place_coin(actor)

# Start the timer
clock.schedule_unique(update_timer, 1.0)

pgzrun.go()

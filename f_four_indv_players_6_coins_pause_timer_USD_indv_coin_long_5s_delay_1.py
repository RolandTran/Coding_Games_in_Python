import pgzrun
from random import randint
import time

# size of game screen
WIDTH = 800
HEIGHT = 800

# Scores for 4 individual players
score_fox = 0
score_police = 0
score_hedgehog = 0
score_blacksonic = 0
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
    hedgehog.draw()
    blacksonic.draw()
    coin.draw()
    quarter.draw()
    dime.draw()
    nickel.draw()
    halfdollar.draw()
    one.draw()

    # Display scores for 4 players
    screen.draw.text(f"Fox score: {round(score_fox, 2)} USD", color="black", topleft=(10, 10))
    screen.draw.text(f"Police score: {round(score_police, 2)} USD", color="black", topleft=(10, 30))
    screen.draw.text(f"Hedgehog score: {round(score_hedgehog, 2)} USD", color="black", topleft=(10, 50))
    screen.draw.text(f"Blacksonic score: {round(score_blacksonic, 2)} USD", color="black", topleft=(10, 70))

    # Display remaining time
    if paused:
        screen.draw.text("Paused", color="red", center=(WIDTH // 2, HEIGHT // 2), fontsize=50)
    else:
        screen.draw.text(f"Time Left: {remaining_time} seconds", color="black", topright=(750, 10))

    if game_over:
        screen.fill("pink")
        if winner:
            screen.draw.text(f"{winner.capitalize()} wins! {round(eval('score_' + winner), 2)} USD.", topleft=(100, 200), fontsize=60, color="black")
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

def exit_game():
    quit()  # Close the game after 5 seconds

def time_up():
    global game_over, winner

    game_over = True
    # Determine winner based on scores
    scores = {
        "fox": score_fox,
        "police": score_police,
        "hedgehog": score_hedgehog,
        "blacksonic": score_blacksonic
    }
    winner = max(scores, key=scores.get) if len(set(scores.values())) > 1 else None  # Handle ties

    # Schedule exit after 5 seconds
    clock.schedule_unique(exit_game, 5.0)

def update():
    global score_fox, score_police, score_hedgehog, score_blacksonic, paused, pause_start_time, total_pause_time

    if keyboard.space:
        if not paused:
            paused = True
            pause_start_time = time.time()  
        else:
            paused = False
            total_pause_time += time.time() - pause_start_time
            clock.schedule_unique(update_timer, 1.0) 

    if paused or game_over:
        return  

    # Player controls
    if keyboard.left:
        fox.x -= 6
    elif keyboard.right:
        fox.x += 6
    elif keyboard.up:
        fox.y -= 6
    elif keyboard.down:
        fox.y += 6

    if keyboard.a:
        police.x -= 6
    elif keyboard.d:
        police.x += 6
    elif keyboard.w:
        police.y -= 6
    elif keyboard.s:
        police.y += 6

    if keyboard.f:
        hedgehog.x -= 6
    elif keyboard.h:
        hedgehog.x += 6
    elif keyboard.t:
        hedgehog.y -= 6
    elif keyboard.g:
        hedgehog.y += 6

    if keyboard.j:
        blacksonic.x -= 6
    elif keyboard.l:
        blacksonic.x += 6
    elif keyboard.i:
        blacksonic.y -= 6
    elif keyboard.k:
        blacksonic.y += 6

    # Keep players within bounds
    fox.x = max(0, min(WIDTH, fox.x))
    fox.y = max(0, min(HEIGHT, fox.y))

    police.x = max(0, min(WIDTH, police.x))
    police.y = max(0, min(HEIGHT, police.y))

    hedgehog.x = max(0, min(WIDTH, hedgehog.x))
    hedgehog.y = max(0, min(HEIGHT, hedgehog.y))

    blacksonic.x = max(0, min(WIDTH, blacksonic.x))
    blacksonic.y = max(0, min(HEIGHT, blacksonic.y))

    # Collision detection
    for player, score in [("fox", score_fox), ("police", score_police), ("hedgehog", score_hedgehog), ("blacksonic", score_blacksonic)]:
        actor = eval(player)

        if actor.colliderect(coin):
            locals()[f"score_{player}"] += 0.01
            place_coin()

        if actor.colliderect(quarter):
            locals()[f"score

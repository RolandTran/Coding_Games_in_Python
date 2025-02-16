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
score_a = 0
score_clicker = 0
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

a = Actor("a")  # Player 4
a.pos = 125, 175

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
    screen.fill("white")
    fox.draw()
    police.draw()
    hedgehog.draw()
    a.draw()
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
    screen.draw.text(f"A score: {round(score_a, 2)} USD", color="black", topleft=(10, 70))
    screen.draw.text(f"Clicker score: {round(score_clicker, 2)} USD", color="black", topleft=(10, 90))


    # Display remaining time
    if paused:
        screen.draw.text("Paused", color="red", center=(WIDTH // 2, HEIGHT // 2), fontsize=50)
    else:
        screen.draw.text(f"Time Left: {remaining_time} seconds", color="black", topright=(750, 10))

    if game_over:
        screen.fill("pink")
        if winner == "fox":
            screen.draw.text(f"Fox wins! {round(score_fox, 2)} USD.", topleft=(100, 200), fontsize=60, color="black")
        elif winner == "police":
            screen.draw.text(f"Police wins! {round(score_police, 2)} USD.", topleft=(100, 200), fontsize=60, color="black")
        elif winner == "hedgehog":
            screen.draw.text(f"Hedgehog wins! {round(score_hedgehog, 2)} USD.", topleft=(100, 200), fontsize=60, color="black")
        elif winner == "a":
            screen.draw.text(f"A wins! {round(score_a, 2)} USD.", topleft=(100, 200), fontsize=60, color="black")
        elif winner == "clicker":
            screen.draw.text(f"Clicker wins! {round(score_clicker, 2)} USD.", topleft=(100, 200), fontsize=60, color="black")
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

def place_fox():
    fox.x = randint(20, WIDTH - 20)
    fox.y = randint(20, HEIGHT - 20)

def place_hedgehog():
    hedgehog.x = randint(25, WIDTH - 15)
    hedgehog.y = randint(25, HEIGHT - 15)

def place_a():
    a.x = randint(15, WIDTH - 25)
    a.y = randint(15, HEIGHT - 25)

def place_police():
    police.x = randint(35, WIDTH - 10)
    police.y = randint(35, HEIGHT - 10)

def exit_game():
    quit()

def time_up():
    global game_over, winner
    game_over = True

    game_over = True
    # Determine winner based on scores
    if score_fox > score_police and score_fox > score_hedgehog and score_fox > score_a and score_fox > score_clicker:
        winner = "fox"
    elif score_police > score_fox and score_police > score_hedgehog and score_police > score_a and score_police > score_clicker:
        winner = "police"
    elif score_hedgehog > score_fox and score_hedgehog > score_police and score_hedgehog > score_a and score_hedgehog > score_clicker:
        winner = "hedgehog"
    elif score_a > score_fox and score_a > score_hedgehog and score_a > score_police and score_a > score_clicker:
        winner = "a"
    elif score_clicker > score_fox and score_clicker > score_hedgehog and score_clicker > score_police and score_clicker > score_a:
        winner = "clicker"
    else:
        winner = None  # Tie or no one wins
        
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
    if coin.collidepoint(pos):
        print("Good click! You hit the coin and gain $0.01 USD.")
        score_clicker += 0.01
        place_coin()
    elif quarter.collidepoint(pos):
        print("Good click! You hit the quarter and gain $0.25 USD.")
        score_clicker += 0.25
        place_quarter()
    elif dime.collidepoint(pos):
        print("Good click! You hit the dime and gain $0.10 USD.")
        score_clicker += 0.10
        place_dime()
    elif nickel.collidepoint(pos):
        print("Good click! You hit the coin and gain $0.05 USD.")
        score_clicker += 0.05
        place_nickel()
    elif halfdollar.collidepoint(pos):
        print("Good click! You hit the nickel and gain $0.05 USD.")
        score_clicker += 0.50
        place_halfdollar()
    elif one.collidepoint(pos):
        print("Good click! You hit the one and gain $1.00 USD.")
        score_clicker += 1.00
        place_one()
    elif a.collidepoint(pos):
        print("Good click! You hit the a and lost $1.00 USD.")
        score_clicker -= 1.00
        place_a()
    elif fox.collidepoint(pos):
        print("Good click! You hit the fox and lost $1.00 USD.")
        score_clicker -= 1.00
        place_fox()
    elif hedgehog.collidepoint(pos):
        print("Good click! You hit the hedgehog and lost $1.00 USD.")
        score_clicker -= 1.00
        place_hedgehog()
    elif police.collidepoint(pos):
        print("Good click! You hit the police and lost $1.00 USD.")
        score_clicker -= 1.00
        place_police()
    else:
        print("You missed!")
        score_clicker -= 2.00

def update():
    global score_fox, score_police, score_hedgehog, score_a, score_clicker, paused, pause_start_time, total_pause_time

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

    # Player 3 (hedgehog) controls:
    if keyboard.f:
        hedgehog.x -= 6
    elif keyboard.h:
        hedgehog.x += 6
    elif keyboard.t:
        hedgehog.y -= 6
    elif keyboard.g:
        hedgehog.y += 6

    # Player 4 (a) controls:
    if keyboard.j:
        a.x -= 6
    elif keyboard.l:
        a.x += 6
    elif keyboard.i:
        a.y -= 6
    elif keyboard.k:
        a.y += 6

    # Keep fox within bounds
    fox.x = max(0, min(WIDTH, fox.x))
    fox.y = max(0, min(HEIGHT, fox.y))

    # Keep police within bounds
    police.x = max(0, min(WIDTH, police.x))
    police.y = max(0, min(HEIGHT, police.y))

    # Keep hedgehog within bounds
    hedgehog.x = max(0, min(WIDTH, hedgehog.x))
    hedgehog.y = max(0, min(HEIGHT, hedgehog.y))

    # Keep a within bounds
    a.x = max(0, min(WIDTH, a.x))
    a.y = max(0, min(HEIGHT, a.y))

    # Collision detection with the fox and coins and players
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

    if fox.colliderect(a):
        score_fox -= 0.250
        place_fox()

    if fox.colliderect(police):
        score_fox -= 0.250
        place_fox()

    if fox.colliderect(hedgehog):
        score_fox -= 0.250
        place_fox()

    # Collision detection with the police and coins and players
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

    if police.colliderect(a):
        score_police -= 0.250
        place_police()

    if police.colliderect(fox):
        score_police -= 0.250
        place_police()

    if police.colliderect(hedgehog):
        score_police -= 0.250
        place_police()

    # Collision detection with the hedgehog and coins and players
    if hedgehog.colliderect(coin):
        score_hedgehog += 0.01
        place_coin()

    if hedgehog.colliderect(quarter):
        score_hedgehog += 0.250
        place_quarter()

    if hedgehog.colliderect(dime):
        score_hedgehog += 0.100
        place_dime()

    if hedgehog.colliderect(nickel):
        score_hedgehog += 0.050
        place_nickel()

    if hedgehog.colliderect(halfdollar):
        score_hedgehog += 0.500
        place_halfdollar()

    if hedgehog.colliderect(one):
        score_hedgehog += 1.00
        place_one()

    if hedgehog.colliderect(a):
        score_hedgehog -= 0.250
        place_hedgehog()

    if hedgehog.colliderect(fox):
        score_hedgehog -= 0.250
        place_hedgehog()

    if hedgehog.colliderect(police):
        score_hedgehog -= 0.250
        place_hedgehog()

    # Collision detection with the a and coins and players
    if a.colliderect(coin):
        score_a += 0.01
        place_coin()

    if a.colliderect(quarter):
        score_a += 0.250
        place_quarter()

    if a.colliderect(dime):
        score_a += 0.100
        place_dime()

    if a.colliderect(nickel):
        score_a += 0.050
        place_nickel()

    if a.colliderect(halfdollar):
        score_a += 0.500
        place_halfdollar()

    if a.colliderect(one):
        score_a += 1.00
        place_one()

    if a.colliderect(hedgehog):
        score_a -= 0.250
        place_a()

    if a.colliderect(fox):
        score_a -= 0.250
        place_a()

    if a.colliderect(police):
        score_a -= 0.250
        place_a()


# Schedule the timer to start
clock.schedule_unique(update_timer, 1.0)
place_coin()
place_quarter()
place_dime()
place_nickel()
place_halfdollar()
place_one()
place_a()
place_hedgehog()
place_fox()
place_police()

pgzrun.go()

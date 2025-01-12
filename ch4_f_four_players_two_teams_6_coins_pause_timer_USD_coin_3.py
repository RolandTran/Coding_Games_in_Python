import pgzrun 
from random import randint
import time

WIDTH = 800
HEIGHT = 800

# Score for teams
Team_A_score = 0
Team_B_score = 0
timer = 60
remaining_time = timer
game_over = False

# Pause state and timing variables
paused = False
pause_start_time = 0  # Time when the game was paused
total_pause_time = 0  # Total accumulated pause duration

# Define Players
fox = Actor("fox")
hedgehog = Actor("hedgehog")
police = Actor("police")
blacksonic = Actor("blacksonic")

# Define Teams using list
Team_A = [fox, hedgehog]
Team_B = [police, blacksonic]

# Define coins
coin = Actor("coin")
nickel = Actor("nickel")
dime = Actor("dime")
quarter = Actor("quarter")
halfdollar = Actor("halfdollar")
one = Actor("one")

# Define coins using list
coins = [coin, nickel, dime, quarter, halfdollar, one]

# Define remaining time for the game
remaining_time = 60  # Start with 60 seconds or any desired duration


# Draw function displaying green screen, teams' scores and remaining time
def draw():
    screen.fill("green")
    for actor in Team_A + Team_B:
        actor.draw()
    for actor in coins:
        actor.draw()

    # Display scores for the team and remaining time
    screen.draw.text(f"Team A (fox / hedgehog): $ {round(Team_A_score, 2)} USD", color = "black", topleft = (10,10))
    screen.draw.text(f"Team B (police / blacksonic): $ {round(Team_B_score, 2)} USD", color = "black", topleft = (10, 30))
    
    # Display remaining time
    if paused:
        screen.draw.text("Paused", color="red", center=(WIDTH // 2, HEIGHT // 2), fontsize=50)
    else:
        screen.draw.text(f"Time Left: {remaining_time} seconds", color="black", topright=(750, 10))

    if game_over:
        screen.fill("pink")
        if Team_A_score > Team_B_score:
            screen.draw.text(f"Team A Won (fox / hedgehog)! ${round(Team_A_score, 2)} USD.", (100,100), color = "black", fontsize = 30)
        elif Team_B_score > Team_A_score:
            screen.draw.text(f"Team B Won (police / blacksonic)! $ {round(Team_B_score, 2)} USD", (100,200), color = "black", fontsize = 30)
        else:
            screen.draw.text("Tie!", (100,100), color = "black", fontsize = 75)

def place_coins():
    for actor in coins:
        actor.pos = (randint(10, WIDTH - 10), randint(10, HEIGHT - 10))

def place_actors():
    for actor in Team_A + Team_B:
        actor.pos = (randint(10, WIDTH - 10), randint(10, HEIGHT - 10))

def time_up():
    global game_over
    game_over = True

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
    global Team_A_score, Team_B_score, paused, pause_start_time, total_pause_time

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
        fox.x -= 5
    elif keyboard.right:
        fox.x += 5
    elif keyboard.up:
        fox.y -= 5
    elif keyboard.down:
        fox.y += 5

    # Player 2 (Hedgehog) controls:
    if keyboard.a:
        hedgehog.x -= 5
    elif keyboard.d:
        hedgehog.x += 5
    elif keyboard.w:
        hedgehog.y -= 5
    elif keyboard.s:
        hedgehog.y += 5

    # Player 3 (Police) controls:
    if keyboard.f:
        police.x -= 5
    elif keyboard.h:
        police.x += 5
    elif keyboard.t:
        police.y -= 5
    elif keyboard.g:
        police.y += 5

    # Player 4 (blacksonic) controls:
    if keyboard.j:
        blacksonic.x -= 5
    elif keyboard.l:
        blacksonic.x += 5
    elif keyboard.i:
        blacksonic.y -= 5
    elif keyboard.k:
        blacksonic.y += 5
    
    
    # Keep players within bounds
    fox.x = max(0, min(WIDTH, fox.x))
    fox.y = max(0, min(HEIGHT, fox.y))

    hedgehog.x = max(0, min(WIDTH, hedgehog.x))
    hedgehog.y = max(0, min(HEIGHT, hedgehog.y))

    police.x = max(0, min(WIDTH, police.x))
    police.y = max(0, min(HEIGHT, police.y))

    blacksonic.x = max(0, min(WIDTH, blacksonic.x))
    blacksonic.y = max(0, min(HEIGHT, blacksonic.y))

    # Collision detection for all teams and coins
    for coin_type, value in [(coin, 0.01), (nickel, 0.05), (dime, 0.10), (quarter, 0.25), (halfdollar, 0.50),(one, 1)]:
        if fox.colliderect(coin_type):
            Team_A_score += value
            place_coins()
        if hedgehog.colliderect(coin_type):
            Team_A_score += value
            place_coins()
        if police.colliderect(coin_type):
            Team_B_score += value
            place_coins()
        if blacksonic.colliderect(coin_type):
            Team_B_score += value
            place_coins()

# Schedule the timer to start
clock.schedule_unique(update_timer, 1.0)
place_actors() # Place the players at random positions initially
place_coins()  # Place the coins at random positions initially
pgzrun.go() # Run the game loop

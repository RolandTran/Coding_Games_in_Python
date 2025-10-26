import pgzrun
from random import randint

score = 0
remaining_time = 60
paused = False
game_over = False
space_pressed = False
WIDTH = 800
HEIGHT = 800

# Define actors
coin = Actor("coin")
penny = Actor("penny")
nickel = Actor("nickel")
dime = Actor("dime")
quarter = Actor("quarter")
halfdollar = Actor("halfdollar")
dollar = Actor("dollar")

# Initial random positions
coin.pos = (randint(10, WIDTH), randint(10, HEIGHT))
penny.pos = (randint(10, WIDTH), randint(10, HEIGHT))
nickel.pos = (randint(10, WIDTH), randint(10, HEIGHT))
dime.pos = (randint(10, WIDTH), randint(10, HEIGHT))
quarter.pos = (randint(10, WIDTH), randint(10, HEIGHT))
halfdollar.pos = (randint(10, WIDTH), randint(10, HEIGHT))
dollar.pos = (randint(10, WIDTH), randint(10, HEIGHT))

# -------- Rules text ---------------------
rules_text = """
PAUSED - GAME RULES:

- Click the coins by moving the mouse cursor over it and clicking.
- The game will end if you click outside the coins.
- Acquire the most USD
- Press SPACE to pause or resume the game.
"""

def draw():
    screen.fill("white")
    coin.draw()
    penny.draw()
    nickel.draw()
    dime.draw()
    quarter.draw()
    halfdollar.draw()
    dollar.draw()
    screen.draw.text(f"Score: {round(score,2)}", topright=(WIDTH-15, 10), fontsize=30, color="black")
    screen.draw.text(f"Time: {remaining_time}s", topleft=(10, 10), fontsize=30, color="black")
    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150, 150, WIDTH - 300, HEIGHT - 300), color="white", align="left")
    if game_over:
        screen.draw.text(f"Time's up! Final score is {round(score,2)}", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")

def place_coin():
    coin.x = randint(20, WIDTH - 20)
    coin.y = randint(20, HEIGHT - 20)

def place_penny():
    penny.x = randint(25, WIDTH - 15)
    penny.y = randint(25, HEIGHT - 15)

def place_nickel():
    nickel.x = randint(15, WIDTH - 25)
    nickel.y = randint(15, HEIGHT - 25)

def place_dime():
    dime.x = randint(20, WIDTH - 20)
    dime.y = randint(20, HEIGHT - 20)

def place_quarter():
    quarter.x = randint(25, WIDTH - 15)
    quarter.y = randint(25, HEIGHT - 15)

def place_halfdollar():
    halfdollar.x = randint(15, WIDTH - 25)
    halfdollar.y = randint(15, HEIGHT - 25)

def place_dollar():
    dollar.x = randint(15, WIDTH - 25)
    dollar.y = randint(15, HEIGHT - 25)

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
    global paused, space_pressed
    # allow pause/suesm toggle always when not game_over
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
    elif not keyboard.space:
        space_pressed = False
    if paused or game_over: # stop all other updateds if puased or game is over
        return # skip any game logic

def on_mouse_down(pos):
    global score # score is global level and must be declared
    if paused or game_over:
        return # ignore all clicks if the game is paused or over
    
    if coin.collidepoint(pos):
        score += 1.00
        print(f"You hit the coin! Your score is {score} USD. ")
        place_coin()
    elif penny.collidepoint(pos):
        score += 0.01
        print(f"You clicked on the penny! Your score is {score} USD.")
        place_penny()
    elif nickel.collidepoint(pos):
        score += 0.05
        print(f"You clicked on the nickel! Your score is {score} USD.")
        place_nickel()
    elif dime.collidepoint(pos):
        score += 0.10
        print(f"You clicked on the dime! Your score is {score} USD.")
        place_dime()
    elif quarter.collidepoint(pos):
        score += 0.25
        print(f"You clicked on the quarter! Your score is {score} USD.")
        place_quarter()
    elif halfdollar.collidepoint(pos):
        score += 0.50
        print(f"You clicked on the halfdollar! Your score is {score} USD.")
        place_halfdollar()
    elif dollar.collidepoint(pos):
        score += 1.00
        print(f"You clicked on the dollar. Your score is {score} USD.")
        place_dollar()
    else:
        print(f"You missed! Game over! Your final score is {round(score,2)}")
        clock.schedule_unique(close_game, 3.0)

place_coin()
place_penny()
place_nickel()
place_dime()
place_quarter()
place_halfdollar()
place_dollar()

clock.schedule_unique(update_timer, 1.0)

pgzrun.go()
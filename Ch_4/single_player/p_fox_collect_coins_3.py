import pygame
import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 800

score = 0
game_over = False
remaining_time = 90
paused = False
space_pressed = False

# ─── Music setup ───────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/jamesbondtheme.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Define player
fox = Actor("fox")
fox.pos = 100, 100

# Define coins
coin = Actor("coin")
penny = Actor("penny")
nickel = Actor("nickel")
dime = Actor("dime")
quarter = Actor("quarter")
halfdollar = Actor("halfdollar")
dollar = Actor("dollar")

# Place coins at random start positions
def place_coin():
    coin.x = randint(20, WIDTH - 20)
    coin.y = randint(20, HEIGHT - 20)

def place_penny():
    penny.x = randint(20, WIDTH - 20)
    penny.y = randint(20, HEIGHT - 20)

def place_nickel():
    nickel.x = randint(20, WIDTH - 20)
    nickel.y = randint(20, HEIGHT - 20)

def place_dime():
    dime.x = randint(20, WIDTH - 20)
    dime.y = randint(20, HEIGHT - 20)

def place_quarter():
    quarter.x = randint(20, WIDTH - 20)
    quarter.y = randint(20, HEIGHT - 20)

def place_halfdollar():
    halfdollar.x = randint(20, WIDTH - 20)
    halfdollar.y = randint(20, HEIGHT - 20)

def place_dollar():
    dollar.x = randint(20, WIDTH - 20)
    dollar.y = randint(20, HEIGHT - 20)

# -------- Rules text ---------------------
rules_text = """
PAUSED - GAME RULES:

- Move the fox with arrow keys.
- Collect coins to increase your USD.
- The game ends when you reach $100 or the timer runs out.
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

    screen.draw.text(f"Score: {round(score,2)} USD", topright=(WIDTH-15, 10), fontsize=30, color="black")
    screen.draw.text(f"Time: {remaining_time}s", topleft=(10, 10), fontsize=30, color="black")
    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150, 150, WIDTH - 300, HEIGHT - 300), color="white", align="left")
    if game_over:
        screen.fill("pink")
        screen.draw.text(f"Time's up! Final score is {round(score,2)} USD", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")

def close_game():
    print("Closing game...")
    quit()

def update_timer():
    global remaining_time, game_over
    if not paused and not game_over:
        remaining_time -= 1
        if remaining_time <= 0:
            sounds.miss.play()
            game_over = True
            print(f"Time's up! Your final score was {score}.")
            clock.schedule_unique(close_game, 3.0)
        else:
            clock.schedule_unique(update_timer, 1.0)
    else:
        # Keep checking every second while paused
        clock.schedule_unique(update_timer, 1.0)

# ─── Update Loop ───────────────────────
def update():
    global paused, space_pressed, score, game_over
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
            sounds.hitcoin.play()
            score += 1.00
            print(f"Your score is {score:.2f} USD")
            place_coin()

        if fox.colliderect(penny):
            sounds.hitpenny.play()
            score += 0.01
            print(f"Your score is {score:.2f} USD")
            place_penny()

        if fox.colliderect(nickel):
            sounds.hitnickel.play()
            score += 0.05
            print(f"Your score is {score:.2f} USD")
            place_nickel()

        if fox.colliderect(dime):
            sounds.hitdime.play()
            score += 0.10
            print(f"Your score is {score:.2f} USD")
            place_dime()

        if fox.colliderect(quarter):
            sounds.hitquarter.play()
            score += 0.25
            print(f"Your score is {score:.2f} USD")
            place_quarter()

        if fox.colliderect(halfdollar):
            sounds.hithalfdollar.play()
            score += 0.50
            print(f"Your score is {score:.2f} USD")
            place_halfdollar()

        if fox.colliderect(dollar):
            sounds.hitdollar.play()
            score += 1.00
            print(f"Your score is {score:.2f} USD")
            place_dollar()

        print(f"Your score is {score:.2f} USD")
        
        # Winning condition
        if score >= 100:
            game_over = True

place_coin()
place_penny()
place_nickel()
place_dime()
place_quarter()
place_halfdollar()
place_dollar()

clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

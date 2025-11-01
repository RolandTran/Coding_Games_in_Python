import pygame
import pgzrun
from random import randint, choice

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


# ─── Actor setup ───────────────────────
coin = Actor("coin")
coin.pos = (randint(10, WIDTH), randint(10, HEIGHT))
coin.dx = choice([-3, -2, -1, 1, 2, 3])
coin.dy = choice([-3, -2, -1, 1, 2, 3])
coin.angle = 0  # start coin rotation

penny = Actor("penny")
penny.pos = (randint(10, WIDTH), randint(10, HEIGHT))
penny.dx = choice([-3, -2, -1, 1, 2, 3])
penny.dy = choice([-3, -2, -1, 1, 2, 3])
penny.angle = 0  # start pennu rotation

nickel = Actor("nickel")
nickel.pos = (randint(10, WIDTH), randint(10, HEIGHT))
nickel.dx = choice([-3, -2, -1, 1, 2, 3])
nickel.dy = choice([-3, -2, -1, 1, 2, 3])
nickel.angle = 0  # start nickel rotation

dime = Actor("dime")
dime.pos = (randint(10, WIDTH), randint(10, HEIGHT))
dime.dx = choice([-3, -2, -1, 1, 2, 3])
dime.dy = choice([-3, -2, -1, 1, 2, 3])
dime.angle = 0  # start dime rotation

quarter = Actor("quarter")
quarter.pos = (randint(10, WIDTH), randint(10, HEIGHT))
quarter.dx = choice([-3, -2, -1, 1, 2, 3])
quarter.dy = choice([-3, -2, -1, 1, 2, 3])
quarter.angle = 0  # start quarter rotation

halfdollar = Actor("halfdollar")
halfdollar.pos = (randint(10, WIDTH), randint(10, HEIGHT))
halfdollar.dx = choice([-3, -2, -1, 1, 2, 3])
halfdollar.dy = choice([-3, -2, -1, 1, 2, 3])
halfdollar.angle = 0  # start halfdollar rotation

dollar = Actor("dollar")
dollar.pos = (randint(10, WIDTH), randint(10, HEIGHT))
dollar.dx = choice([-3, -2, -1, 1, 2, 3])
dollar.dy = choice([-3, -2, -1, 1, 2, 3])
dollar.angle = 0  # start dollar rotation

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


# ─── coin Movement ────────────────────
def move_coin():
    coin.x += coin.dx
    coin.y += coin.dy

    # Bounce off walls
    if coin.left < 0 or coin.right > WIDTH:
        coin.dx *= -1
    if coin.top < 0 or coin.bottom > HEIGHT:
        coin.dy *= -1
    
    # Rotate the coin
    coin.angle = (coin.angle + 5) % 360  # rotates clockwise 5 degrees per frame

# ─── penny Movement ────────────────────
def move_penny():
    penny.x += penny.dx
    penny.y += penny.dy

    # Bounce off walls
    if penny.left < 0 or penny.right > WIDTH:
        penny.dx *= -1
    if penny.top < 0 or penny.bottom > HEIGHT:
        penny.dy *= -1
    
    # Rotate the penny
    penny.angle = (penny.angle + 5) % 360  # rotates clockwise 5 degrees per frame

# ─── nickel Movement ────────────────────
def move_nickel():
    nickel.x += nickel.dx
    nickel.y += nickel.dy

    # Bounce off walls
    if nickel.left < 0 or nickel.right > WIDTH:
        nickel.dx *= -1
    if nickel.top < 0 or nickel.bottom > HEIGHT:
        nickel.dy *= -1
    
    # Rotate the nickel
    nickel.angle = (nickel.angle + 5) % 360  # rotates clockwise 5 degrees per frame

# ─── dime Movement ────────────────────
def move_dime():
    dime.x += dime.dx
    dime.y += dime.dy

    # Bounce off walls
    if dime.left < 0 or dime.right > WIDTH:
        dime.dx *= -1
    if dime.top < 0 or dime.bottom > HEIGHT:
        dime.dy *= -1
    
    # Rotate the dime
    dime.angle = (dime.angle + 5) % 360  # rotates clockwise 5 degrees per frame

# ─── quarter Movement ────────────────────
def move_quarter():
    quarter.x += quarter.dx
    quarter.y += quarter.dy

    # Bounce off walls
    if quarter.left < 0 or quarter.right > WIDTH:
        quarter.dx *= -1
    if quarter.top < 0 or quarter.bottom > HEIGHT:
        quarter.dy *= -1
    
    # Rotate the quarter
    quarter.angle = (quarter.angle + 5) % 360  # rotates clockwise 5 degrees per frame

# ─── halfdollar Movement ────────────────────
def move_halfdollar():
    halfdollar.x += halfdollar.dx
    halfdollar.y += halfdollar.dy

    # Bounce off walls
    if halfdollar.left < 0 or halfdollar.right > WIDTH:
        halfdollar.dx *= -1
    if halfdollar.top < 0 or halfdollar.bottom > HEIGHT:
        halfdollar.dy *= -1
    
    # Rotate the halfdollar
    halfdollar.angle = (halfdollar.angle + 5) % 360  # rotates clockwise 5 degrees per frame

# ─── dollar Movement ────────────────────
def move_dollar():
    dollar.x += dollar.dx
    dollar.y += dollar.dy

    # Bounce off walls
    if dollar.left < 0 or dollar.right > WIDTH:
        dollar.dx *= -1
    if dollar.top < 0 or dollar.bottom > HEIGHT:
        dollar.dy *= -1
    
    # Rotate the dollar
    dollar.angle = (dollar.angle + 5) % 360  # rotates clockwise 5 degrees per frame


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

    if not paused and not game_over: 
        move_coin()
        move_penny()
        move_nickel()
        move_dime()
        move_quarter()
        move_halfdollar()
        move_dollar()
        
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
             # Increase coin speed
            coin.dx += 1 if coin.dx > 0 else -1
            coin.dy += 1 if coin.dy > 0 else -1
            coin.dx = max(min(coin.dx, 10), -10)
            coin.dy = max(min(coin.dy, 10), -10)
            print(f"Your score is {score:.2f} USD")
            place_coin()

        if fox.colliderect(penny):
            sounds.hitpenny.play()
            score += 0.01
            # Increase penny speed
            penny.dx += 1 if penny.dx > 0 else -1
            penny.dy += 1 if penny.dy > 0 else -1
            penny.dx = max(min(penny.dx, 10), -10)
            penny.dy = max(min(penny.dy, 10), -10)
            print(f"Your score is {score:.2f} USD")
            place_penny()

        if fox.colliderect(nickel):
            sounds.hitnickel.play()
            score += 0.05
             # Increase nickel speed
            nickel.dx += 1 if nickel.dx > 0 else -1
            nickel.dy += 1 if nickel.dy > 0 else -1
            nickel.dx = max(min(nickel.dx, 10), -10)
            nickel.dy = max(min(nickel.dy, 10), -10)
            print(f"Your score is {score:.2f} USD")
            place_nickel()

        if fox.colliderect(dime):
            sounds.hitdime.play()
            score += 0.10
            # Increase dime speed
            dime.dx += 1 if dime.dx > 0 else -1
            dime.dy += 1 if dime.dy > 0 else -1
            dime.dx = max(min(dime.dx, 10), -10)
            dime.dy = max(min(dime.dy, 10), -10)
            print(f"Your score is {score:.2f} USD")
            place_dime()

        if fox.colliderect(quarter):
            sounds.hitquarter.play()
            score += 0.25
            # Increase quarter speed
            quarter.dx += 1 if quarter.dx > 0 else -1
            quarter.dy += 1 if quarter.dy > 0 else -1
            quarter.dx = max(min(quarter.dx, 10), -10)
            quarter.dy = max(min(quarter.dy, 10), -10)
            print(f"Your score is {score:.2f} USD")
            place_quarter()

        if fox.colliderect(halfdollar):
            sounds.hithalfdollar.play()
            score += 0.50
            # Increase halfdollar speed
            halfdollar.dx += 1 if halfdollar.dx > 0 else -1
            halfdollar.dy += 1 if halfdollar.dy > 0 else -1
            halfdollar.dx = max(min(halfdollar.dx, 10), -10)
            halfdollar.dy = max(min(halfdollar.dy, 10), -10)
            print(f"Your score is {score:.2f} USD")
            place_halfdollar()

        if fox.colliderect(dollar):
            sounds.hitdollar.play()
            score += 1.00
            # Increase dollar speed
            dollar.dx += 1 if dollar.dx > 0 else -1
            dollar.dy += 1 if dollar.dy > 0 else -1
            dollar.dx = max(min(dollar.dx, 10), -10)
            dollar.dy = max(min(dollar.dy, 10), -10)
            print(f"Your score is {score:.2f} USD")
            place_dollar()
        
        # Winning condition
        if score >= 100:
            game_over = True
            
     # Collision detection with the coin and penny, nickel, dime, quarter, halfdollar, dollar
    if coin.colliderect(penny):
        place_coin()
    if coin.colliderect(nickel):
        place_coin()
    if coin.colliderect(dime):
        place_coin()
    if coin.colliderect(quarter):
        place_coin()
    if coin.colliderect(halfdollar):
        place_coin()
    if coin.colliderect(dollar):
        place_coin()

     # Collision detection with the penny and coin, nickel, dime, quarter, halfdollar, dollar
    if penny.colliderect(coin):
        place_penny()
    if penny.colliderect(nickel):
        place_penny()
    if penny.colliderect(dime):
        place_penny()
    if penny.colliderect(quarter):
        place_penny()
    if penny.colliderect(halfdollar):
        place_penny()
    if penny.colliderect(dollar):
        place_penny()
        
    # Collision detection with the nickel and coin, penny, dime, quarter, halfdollar, dollar
    if nickel.colliderect(coin):
        place_nickel()
    if nickel.colliderect(penny):
        place_nickel()
    if nickel.colliderect(dime):
        place_nickel()
    if nickel.colliderect(quarter):
        place_nickel()
    if nickel.colliderect(halfdollar):
        place_nickel()
    if nickel.colliderect(dollar):
        place_nickel()

      # Collision detection with the dime and coin, penny, nickel, quarter, halfdollar, dollar
    if dime.colliderect(coin):
        place_dime()
    if dime.colliderect(penny):
        place_dime()
    if dime.colliderect(nickel):
        place_dime()
    if dime.colliderect(quarter):
        place_dime()
    if dime.colliderect(halfdollar):
        place_dime()
    if dime.colliderect(dollar):
        place_dime()

    # Collision detection with the quarter and coin, penny, nickel, dime, halfdollar, dollar
    if quarter.colliderect(coin):
        place_quarter()
    if quarter.colliderect(penny):
        place_quarter()
    if quarter.colliderect(nickel):
        place_quarter()
    if quarter.colliderect(dime):
        place_quarter()
    if quarter.colliderect(halfdollar):
        place_quarter()
    if quarter.colliderect(dollar):
        place_quarter()

    # Collision detection with the halfdollar and coin, penny, nickel, dime, quarter, dollar
    if halfdollar.colliderect(coin):
        place_halfdollar()
    if halfdollar.colliderect(penny):
        place_halfdollar()
    if halfdollar.colliderect(nickel):
        place_halfdollar()
    if halfdollar.colliderect(dime):
        place_halfdollar()
    if halfdollar.colliderect(quarter):
        place_halfdollar()
    if halfdollar.colliderect(dollar):
        place_halfdollar()

     # Collision detection with the dollar and coin, penny, nickel, dime, quarter, halfdollar
    if dollar.colliderect(coin):
        place_dollar()
    if dollar.colliderect(penny):
        place_dollar()
    if dollar.colliderect(nickel):
        place_dollar()
    if dollar.colliderect(dime):
        place_dollar()
    if dollar.colliderect(quarter):
        place_dollar()
    if dollar.colliderect(halfdollar):
        place_dollar()

place_coin()
place_penny()
place_nickel()
place_dime()
place_quarter()
place_halfdollar()
place_dollar()

clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

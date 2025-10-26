import pygame
import pgzrun
from random import randint, choice

score = 0
time_left = 60
paused = False
game_over = False
space_pressed = False
WIDTH = 800
HEIGHT = 800

# ─── Music setup ───────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/jamesbondtheme.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


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
    screen.draw.text(f"Score: {round(score,2)} USD", topright=(WIDTH-15, 10), fontsize=30, color="black")
    screen.draw.text(f"Time: {time_left}s", topleft=(10, 10), fontsize=30, color="black")
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
    print("Closing game...in 1.5s")
    quit()

def update_timer():
    global time_left, game_over
    if not paused and not game_over:
        time_left -= 1
        if time_left <= 0:
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
    global paused, space_pressed
    # allow pause/suesm toggle always when not game_over
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
        # stop all other updateds if puased or game is over
        if paused or game_over: 
            pygame.mixer.music.pause()
            return # skip any game logic
        else:
            pygame.mixer.music.unpause()
            clock.schedule_unique(update_timer, 1.0)
    elif not keyboard.space:
        space_pressed = False
    
    if not paused and not game_over:
        move_coin()
        move_penny()
        move_nickel()
        move_dime()
        move_quarter()
        move_halfdollar()
        move_dollar()
    

def on_mouse_down(pos):
    global score # score is global level and must be declared
    if paused or game_over:
        return # ignore all clicks if the game is paused or over
    
    if coin.collidepoint(pos):
        sounds.hitcoin.play()
        score += 1.00
        print(f"You hit the coin! Your score is {round(score,2)} USD. ")
        place_coin()
    elif penny.collidepoint(pos):
        sounds.hitpenny.play()
        score += 0.01
        print(f"You clicked on the penny! Your score is {round(score,2)} USD.")
        place_penny()
    elif nickel.collidepoint(pos):
        sounds.hitnickel.play()
        score += 0.05
        print(f"You clicked on the nickel! Your score is {round(score,2)} USD.")
        place_nickel()
    elif dime.collidepoint(pos):
        sounds.hitdime.play()
        score += 0.10
        print(f"You clicked on the dime! Your score is {round(score,2)} USD.")
        place_dime()
    elif quarter.collidepoint(pos):
        sounds.hitquarter.play()
        score += 0.25
        print(f"You clicked on the quarter! Your score is {round(score,2)} USD.")
        place_quarter()
    elif halfdollar.collidepoint(pos):
        sounds.hithalfdollar.play()
        score += 0.50
        print(f"You clicked on the halfdollar! Your score is {round(score,2)}USD.")
        place_halfdollar()
    elif dollar.collidepoint(pos):
        sounds.hitdollar.play()
        score += 1.00
        print(f"You clicked on the dollar. Your score is {round(score,2)} USD.")
        place_dollar()
    else:
        sounds.miss.play()
        print(f"You missed! Game over! Your final score is {round(score,2)}")
        clock.schedule_unique(close_game, 1.5)

place_coin()
place_penny()
place_nickel()
place_dime()
place_quarter()
place_halfdollar()
place_dollar()

clock.schedule_unique(update_timer, 1.0)

pgzrun.go()
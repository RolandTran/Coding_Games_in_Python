import pygame
import pgzrun
from random import randint, choice

WIDTH = 800
HEIGHT = 800

# Scores and states
score_fox = 0.0
score_clicker = 0.0
paused = False
space_pressed = False
game_over = False
time_left = 90
flash_time = 0

# ─── Music setup ───────────────────────
pygame.mixer.init()
pygame.mixer.music.load("music/jamesbondtheme.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# --- Actors ---
fox = Actor("fox")
fox.pos = 100, 100

# --- coins ---
coin = Actor("coin")
coin.pos = (randint(10, WIDTH), randint(10, HEIGHT))
coin.dx = choice([-3, -2, -1, 1, 2, 3])
coin.dy = choice([-3, -2, -1, 1, 2, 3])
coin.angle = 0  # start coin rotation

penny = Actor("penny")
penny.pos = (randint(10, WIDTH), randint(10, HEIGHT))
penny.dx = choice([-3, -2, -1, 1, 2, 3])
penny.dy = choice([-3, -2, -1, 1, 2, 3])
penny.angle = 0  # start penny rotation

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

# --- Place functions ---
def place_fox():
    fox.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

def place_coin():
    coin.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

def place_penny():
    penny.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

def place_nickel():
    nickel.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

def place_dime():
    dime.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

def place_quarter():
    quarter.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

def place_halfdollar():
    halfdollar.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

def place_dollar():
    dollar.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

# --- Spawn everything ---
place_fox()
place_coin()
place_penny()
place_nickel()
place_dime()
place_quarter()
place_halfdollar()
place_dollar()

# --- Pause rules text ---
rules_text = """
PAUSED - GAME RULES:

- Fox moves with arrow keys
- Mouse/touch clicks collect coins
- Game lasts 90 seconds
- Higher score wins
- SPACE = Pause / Resume
"""

# --- Flash effect ---
def flash():
    global flash_time
    flash_time = 2.0

# --- Restart ---
def restart_game():
    global score_fox, score_clicker, time_left, paused, game_over, flash_time
    score_fox = 0.0
    score_clicker = 0.0
    time_left = 90
    flash_time = 0
    paused = False
    game_over = False
    place_fox()
    place_coin()
    place_penny()
    place_nickel()
    place_dime()
    place_quarter()
    place_halfdollar()
    place_dollar()
    
# --- Draw function ---
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
    
    screen.draw.text(f"Fox Score: {score_fox:.2f}", (10,10), color="black")
    screen.draw.text(f"Clicker Score: {score_clicker:.2f}", (10,30), color="black")
    screen.draw.text(f"Time Left: {time_left}", topright=(WIDTH-10,10), color="red")
    
    if flash_time > 0:
        screen.draw.filled_rect(Rect(0,0,WIDTH,HEIGHT),(255,255,0,80))
    
    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150,150,WIDTH-300,HEIGHT-300), color="white")
    
    if game_over:
        screen.fill("lightblue")
        if score_fox > score_clicker:
            winner = "Fox Wins! 🦊"
        elif score_clicker > score_fox:
            winner = "Clicker Wins! 🖱️"
        else:
            winner = "It's a Tie! 🤝"
        
        screen.draw.text(winner, center=(WIDTH/2, HEIGHT/2-40), fontsize=60, color="black")
        screen.draw.text(f"Fox: {score_fox:.2f} | Clicker: {score_clicker:.2f}", center=(WIDTH/2, HEIGHT/2+20), fontsize=40, color="black")
        screen.draw.text("CLICK TO RESTART", center=(WIDTH/2, HEIGHT/2+120), fontsize=45, color="darkred")

def close_game():
    print("Closing game...")
    quit()

def end_game():
    global game_over
    game_over = True
    print_winner()
    
# --- Timer ---
def update_timer():
    global time_left
    if not paused and not game_over:
        time_left -= 1
        if time_left <= 0:
            sounds.miss.play()
            clock.schedule_unique(close_game, 5.0)
            end_game()
        else:
            clock.schedule_unique(update_timer,1.0)
    else:
        clock.schedule_unique(update_timer,1.0)

def print_winner():
    if score_fox > score_clicker: print("Fox Wins! 🦊")
    elif score_clicker > score_fox: print("Clicker Wins! 🖱️")
    else: print("Tie Game! 🤝")
    print(f"Final Scores — Fox: {score_fox:.2f}, Clicker: {score_clicker:.2f}")

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


# --- Update ---
def update():
    global paused, space_pressed, score_fox, flash_time, game_over
    
    if flash_time > 0:
        flash_time -= 1
        if flash_time < 0:
            flash_time = 0
    
    # Pause toggle
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True

        if paused:
            pygame.mixer.music.pause() # pause music
        else:
            pygame.mixer.music.unpause() # resmume music
        
    elif not keyboard.space:
        space_pressed = False
    
    if paused or game_over:
        return

    if not paused and not game_over: 
        move_coin()
        move_penny()
        move_nickel()
        move_dime()
        move_quarter()
        move_halfdollar()
        move_dollar()

        # Fox movement with screen boundaries
        if keyboard.left: fox.x -= 6
        if keyboard.right: fox.x += 6
        if keyboard.up: fox.y -= 6
        if keyboard.down: fox.y += 6
    
        fox.x = max(20, min(WIDTH-20, fox.x))
        fox.y = max(20, min(HEIGHT-20, fox.y))
    
        # Coin collisions for fox
        if fox.colliderect(coin): sounds.hitcoin.play(); score_fox += 1; flash(); place_coin()
        if fox.colliderect(penny): sounds.hitpenny.play(); score_fox += 0.01; flash(); place_penny()
        if fox.colliderect(nickel): sounds.hitnickel.play(); score_fox += 0.05; flash(); place_nickel()
        if fox.colliderect(dime): sounds.hitdime.play(); score_fox += 0.10; flash(); place_dime()
        if fox.colliderect(quarter): sounds.hitquarter.play(); score_fox += 0.25; flash(); place_quarter()
        if fox.colliderect(halfdollar): sounds.hithalfdollar.play(); score_fox += 0.50; flash(); place_halfdollar()
        if fox.colliderect(dollar): sounds.hitdollar.play(); score_fox += 1; flash(); place_dollar()

        #Game over conditon
        if time_left <= 0:
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

# --- Mouse clicks ---
def on_mouse_down(pos):
    global score_clicker, score_fox, game_over, flash_time
    if game_over:
        restart_game()
        return
    
    if fox.collidepoint(pos):
        sounds.miss.play()
        score_fox -= 0.10
        flash()
        place_fox()
    
    if coin.collidepoint(pos): sounds.hitcoin.play(); score_clicker += 1; flash(); place_coin()
    elif penny.collidepoint(pos): sounds.hitpenny.play();  score_clicker += 0.01; flash(); place_penny()
    elif nickel.collidepoint(pos): sounds.hitnickel.play(); score_clicker += 0.05; flash(); place_nickel()
    elif dime.collidepoint(pos): sounds.hitdime.play(); score_clicker += 0.10; flash(); place_dime()
    elif quarter.collidepoint(pos): sounds.hitquarter.play();  score_clicker += 0.25; flash(); place_quarter()
    elif halfdollar.collidepoint(pos): sounds.hithalfdollar.play(); score_clicker += 0.50; flash(); place_halfdollar()
    elif dollar.collidepoint(pos): sounds.hitdollar.play(); score_clicker += 1; flash(); place_dollar()
    else: sounds.miss.play(); print(f" Clicker missed and loses $0.25! Clicker's score is now {round(score_clicker,2)}");score_clicker -= 0.25

# --- Schedule timer ---
clock.schedule_unique(update_timer, 1.0)

# --- Run game safely ---
try:
    pgzrun.go()
finally:
    if not game_over:
        print("\nGame closed manually — treating as Game Over!\n")
        end_game()




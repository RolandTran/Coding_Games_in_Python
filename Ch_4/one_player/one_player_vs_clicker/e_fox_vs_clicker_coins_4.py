import pygame
import pgzrun
from random import randint

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
coin = Actor("coin")
penny = Actor("penny")
nickel = Actor("nickel")
dime = Actor("dime")
quarter = Actor("quarter")
halfdollar = Actor("halfdollar")
dollar = Actor("dollar")

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
    flash_time = 20

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
    
    if paused and not game_over:
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
            clock.schedule_unique(close_game, 3.0)
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
    elif not keyboard.space:
        space_pressed = False
    
    if paused or game_over:
        return

    if not game_over:
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

# --- Mouse clicks ---
def on_mouse_down(pos):
    global score_clicker, score_fox, game_over, flash_time
    if game_over:
        restart_game()
        return
    
    if fox.collidepoint(pos):
        sounds.hitfox.play()
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

# --- Schedule timer ---
clock.schedule_unique(update_timer, 1.0)

# --- Run game safely ---
try:
    pgzrun.go()
finally:
    if not game_over:
        print("\nGame closed manually — treating as Game Over!\n")
        end_game()




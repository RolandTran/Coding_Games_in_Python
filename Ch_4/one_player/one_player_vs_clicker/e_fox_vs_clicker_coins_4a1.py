import pygame
import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 800

# Game state
score_fox = 0.0
score_clicker = 0.0
paused = False
space_pressed = False
game_over = False
time_left = 90
flash_time = 0

# Music setup
pygame.mixer.init()
pygame.mixer.music.load("music/jamesbondtheme.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Fox
fox = Actor("fox")

# Coins with values
coins = {
    "coin": 1.0,
    "penny": 0.01,
    "nickel": 0.05,
    "dime": 0.10,
    "quarter": 0.25,
    "halfdollar": 0.50,
    "dollar": 1.0,
}

coin_actors = {name: Actor(name) for name in coins}

def place(actor):
    actor.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

# Spawn everything
place(fox)
for actor in coin_actors.values():
    place(actor)

rules_text = """
PAUSED - GAME RULES:

- Fox moves with arrow keys
- Mouse/touch clicks collect coins
- Game lasts 90 seconds
- Higher score wins
- SPACE = Pause / Resume
"""

def flash():
    global flash_time
    flash_time = 2.0

def draw():
    screen.fill("white")
    
    fox.draw()
    for actor in coin_actors.values():
        actor.draw()

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
        if score_fox > score_clicker: winner = "Fox Wins! 🦊"
        elif score_clicker > score_fox: winner = "Clicker Wins! 🖱️"
        else: winner = "It's a Tie! 🤝"
        screen.draw.text(winner, center=(WIDTH/2,HEIGHT/2-40), fontsize=60, color="black")
        screen.draw.text(f"Fox: {score_fox:.2f} | Clicker: {score_clicker:.2f}",
                         center=(WIDTH/2,HEIGHT/2+20), fontsize=40, color="black")
        screen.draw.text("CLICK TO RESTART",
                         center=(WIDTH/2,HEIGHT/2+120),
                         fontsize=45, color="darkred")

def close_game():
    print("Closing game...")
    quit()

def end_game():
    global game_over
    game_over = True
    print_winner()

def update_timer():
    global time_left
    if not paused and not game_over:
        time_left -= 1
        if time_left <= 0:
            sounds.miss.play()
            end_game()
            clock.schedule_unique(close_game, 5.0)
        else:
            clock.schedule_unique(update_timer,1.0)
    else:
        clock.schedule_unique(update_timer,1.0)

def print_winner():
    print("\nFINAL SCORES:")
    print(f"Fox: {score_fox:.2f} | Clicker: {score_clicker:.2f}")
    if score_fox > score_clicker: print("Fox Wins! 🦊")
    elif score_clicker > score_fox: print("Clicker Wins! 🖱️")
    else: print("Tie Game! 🤝")

def update():
    global paused, space_pressed, flash_time, score_fox, game_over

    if flash_time > 0:
        flash_time -= 1

    # Pause toggle (always active)
    if keyboard.space and not space_pressed:
        paused = not paused
        space_pressed = True
        if paused: pygame.mixer.music.pause()
        else: pygame.mixer.music.unpause()
    elif not keyboard.space:
        space_pressed = False

    if paused or game_over: return

    # Fox movement
    if keyboard.left: fox.x -= 6
    if keyboard.right: fox.x += 6
    if keyboard.up: fox.y -= 6
    if keyboard.down: fox.y += 6

    fox.x = max(20, min(WIDTH-20, fox.x))
    fox.y = max(20, min(HEIGHT-20, fox.y))

    # Coin collisions (fox)
    for name, actor in coin_actors.items():
        if fox.colliderect(actor):
            sounds["hit"+name].play()
            score_fox += coins[name]
            flash()
            place(actor)

    if time_left <= 0:
        game_over = True

def on_mouse_down(pos):
    global score_clicker, score_fox

    if game_over:
        restart_game()
        return
    
    # Clicking the fox = penalty
    if fox.collidepoint(pos):
        sounds.miss.play()
        score_fox -= 0.10
        flash()
        place(fox)

    # Clicking coins
    for name, actor in coin_actors.items():
        if actor.collidepoint(pos):
            sounds["hit"+name].play()
            score_clicker += coins[name]
            flash()
            place(actor)
            break

def restart_game():
    global score_fox, score_clicker, time_left, paused, game_over, flash_time
    score_fox = score_clicker = 0.0
    time_left = 90
    flash_time = 0
    paused = False
    game_over = False

    place(fox)
    for actor in coin_actors.values():
        place(actor)

clock.schedule_unique(update_timer, 1.0)

try:
    pgzrun.go()
finally:
    if not game_over:
        print("\nGame closed manually — treating as Game Over!\n")
        end_game()




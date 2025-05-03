import pgzrun
from random import randint
import time

WIDTH, HEIGHT = 800, 800

# Lists of dots and lines
red_dots = []     # Fox's dots
blue_dots = []    # Hedgehog's dots
green_dots = []   # Police's dots
yellow_dots = []  # Player's dots

red_lines = []
blue_lines = []
green_lines = []
yellow_lines = []

# Game State Variables
fox_progress = 0
hedgehog_progress = 0
police_progress = 0
player_progress = 0

remaining_time = 75
paused = False
game_over = False
winner = ""

# Rules text for pause screen
rules_text = """
PAUSED - GAME RULES:

- Fox (Arrow Keys) must collect RED dots.
- Hedgehog (WASD Keys) must collect BLUE dots.
- Police (TGFH Keys) must collect GREEN dots.
- Player (Mouse Clicks) must collect YELLOW dots.

- Connect all your dots to win!
- First character to finish wins!
- Press SPACE to resume the game.
"""

# Create 10 dots for each character
for _ in range(10):
    red = Actor("dot")
    red.pos = randint(20, WIDTH - 20), randint(20, HEIGHT - 20)
    red_dots.append(red)
    
    blue = Actor("dot")
    blue.pos = randint(20, WIDTH - 20), randint(20, HEIGHT - 20)
    blue_dots.append(blue)
    
    green = Actor("dot")
    green.pos = randint(20, WIDTH - 20), randint(20, HEIGHT - 20)
    green_dots.append(green)
    
    yellow = Actor("dot")
    yellow.pos = randint(20, WIDTH - 20), randint(20, HEIGHT - 20)
    yellow_dots.append(yellow)

# Initialize characters
fox = Actor("fox")
fox.pos = red_dots[0].pos

hedgehog = Actor("hedgehog")
hedgehog.pos = blue_dots[0].pos

police = Actor("police")
police.pos = green_dots[0].pos

# --- Drawing ---
def draw():
    screen.fill("black")
    
    # Draw dots
    for i, dot in enumerate(red_dots):
        dot.draw()
        screen.draw.text(str(i+1), (dot.x+10, dot.y+10), color="red")
    for i, dot in enumerate(blue_dots):
        dot.draw()
        screen.draw.text(str(i+1), (dot.x+10, dot.y+10), color="blue")
    for i, dot in enumerate(green_dots):
        dot.draw()
        screen.draw.text(str(i+1), (dot.x+10, dot.y+10), color="green")
    for i, dot in enumerate(yellow_dots):
        dot.draw()
        screen.draw.text(str(i+1), (dot.x+10, dot.y+10), color="yellow")

    # Draw lines
    for line in red_lines:
        screen.draw.line(line[0], line[1], "red")
    for line in blue_lines:
        screen.draw.line(line[0], line[1], "blue")
    for line in green_lines:
        screen.draw.line(line[0], line[1], "green")
    for line in yellow_lines:
        screen.draw.line(line[0], line[1], "yellow")
    
    # Draw characters
    fox.draw()
    hedgehog.draw()
    police.draw()
    
    # Draw timer
    screen.draw.text(f"Time Left: {remaining_time}s", topleft=(10,10), color="white")
    
    # If paused, show rules
    if paused:
        screen.draw.filled_rect(Rect(50, 50, WIDTH-100, HEIGHT-100), (20, 20, 20))  # Dark background
        screen.draw.textbox(rules_text, Rect(100, 100, WIDTH-200, HEIGHT-200), color="white")
    
    # If game over
    if game_over:
        screen.fill("black")
        screen.draw.text(winner, center=(WIDTH//2, HEIGHT//2), fontsize=60, color="white")

def close_game():
    """Closes the game after a delay."""
    print("Closing game...")
    quit()  # Proper way to exit Pygame Zero

# --- Timer ---
def update_timer():
    global remaining_time, game_over, winner
    if paused or game_over:
        return
    remaining_time -= 1
    if remaining_time <= 0:
        game_over = True
        winner = "Time's up! No winner!"
        clock.schedule_unique(close_game, 5.0)
    else:
        clock.schedule_unique(update_timer, 1.0)

# --- Mouse Input (for player only) ---
def on_mouse_down(pos):
    global player_progress, yellow_lines, game_over, winner
    if game_over:
        return
    
    if yellow_dots[player_progress].collidepoint(pos):
        if player_progress > 0:
            yellow_lines.append((yellow_dots[player_progress-1].pos, yellow_dots[player_progress].pos))
        player_progress += 1
        print(f"Player connects {player_progress} yellow dot")
        if player_progress == len(yellow_dots):
            game_over = True
            winner = "Clicker wins! All yellow dots connected!"
            clock.schedule_unique(close_game, 5.0)
    else:
        yellow_lines.clear()
        player_progress = 0

# --- Movement and Logic Update ---
def update():
    global paused, game_over
    global fox_progress, hedgehog_progress, police_progress, winner
    
    if keyboard.space and not game_over:
        paused = not paused
        if not paused:
            clock.schedule_unique(update_timer, 1.0)
    
    if game_over or paused:
        return
    
    # --- Fox movement (Arrow keys) ---
    if keyboard.left:
        fox.x -= 4
    if keyboard.right:
        fox.x += 4
    if keyboard.up:
        fox.y -= 4
    if keyboard.down:
        fox.y += 4

    # --- Hedgehog movement (WASD keys) ---
    if keyboard.a:
        hedgehog.x -= 4
    if keyboard.d:
        hedgehog.x += 4
    if keyboard.w:
        hedgehog.y -= 4
    if keyboard.s:
        hedgehog.y += 4

    # --- Police movement (TGFH keys) ---
    if keyboard.f:
        police.x -= 4
    if keyboard.h:
        police.x += 4
    if keyboard.t:
        police.y -= 4
    if keyboard.g:
        police.y += 4

    # Boundaries
    fox.x = max(0, min(WIDTH, fox.x))
    fox.y = max(0, min(HEIGHT, fox.y))
    hedgehog.x = max(0, min(WIDTH, hedgehog.x))
    hedgehog.y = max(0, min(HEIGHT, hedgehog.y))
    police.x = max(0, min(WIDTH, police.x))
    police.y = max(0, min(HEIGHT, police.y))

    # --- Fox touches red dots ---
    if fox_progress < len(red_dots) and fox.colliderect(red_dots[fox_progress]):
        if fox_progress > 0:
            red_lines.append((red_dots[fox_progress-1].pos, red_dots[fox_progress].pos))
        fox_progress += 1
        print(f"Fox connects {fox_progress} red dot")
        if fox_progress == len(red_dots):
            game_over = True
            winner = "Fox wins! All red dots connected"
            clock.schedule_unique(close_game, 5.0)

    # --- Hedgehog touches blue dots ---
    if hedgehog_progress < len(blue_dots) and hedgehog.colliderect(blue_dots[hedgehog_progress]):
        if hedgehog_progress > 0:
            blue_lines.append((blue_dots[hedgehog_progress-1].pos, blue_dots[hedgehog_progress].pos))
        hedgehog_progress += 1
        print(f"Hedgehog connects {hedgehog_progress} blue dot")
        if hedgehog_progress == len(blue_dots):
            game_over = True
            winner = "Hedgehog wins! All blue dots connected"
            clock.schedule_unique(close_game, 5.0)

    # --- Police touches green dots ---
    if police_progress < len(green_dots) and police.colliderect(green_dots[police_progress]):
        if police_progress > 0:
            green_lines.append((green_dots[police_progress-1].pos, green_dots[police_progress].pos))
        police_progress += 1
        print(f"Police connects {police_progress} green dot")
        if police_progress == len(green_dots):
            game_over = True
            winner = "Police wins! All green dots connected"
            clock.schedule_unique(close_game, 5.0)

# Start the timer
clock.schedule_unique(update_timer, 1.0)

pgzrun.go()

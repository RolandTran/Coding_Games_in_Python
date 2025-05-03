import pgzrun
from random import randint
import time

WIDTH, HEIGHT = 800, 800

# List of dots and lines
dots = []
lines = []

# Game State Variables
next_dot = 0  # Player's progress
fox_progress = 0  # Fox's progress
hedgehog_progress = 0 # hedehog_progress
police_progress = 0  # police_progress
remaining_time = 60
paused = False
game_over = False
winner = ""

# Rules text for pause screen
rules_text = """
PAUSED - GAME RULES:

- Fox (Arrow Keys) must collect dots.
- Hedgehog (WASD Keys) must collect dots.
- Police (TGFH Keys) must collect dots.
- Player (Mouse Clicks) must collect dots.

- Connect all your dots to win!
- First character to finish wins!
- Press SPACE to resume the game.
"""

# Create 10 dots at random positions
for _ in range(10):
    actor = Actor("dot")
    actor.pos = randint(20, WIDTH - 20), randint(20, HEIGHT - 20)
    dots.append(actor)

# Initialize Fox
fox = Actor("fox")
fox.pos = 100, 100  # Start at the first dot

police = Actor("police")
police.pos = 150, 150  # Start at the first dot

hedgehog = Actor("hedgehog")
hedgehog.pos = 200, 200  # Start at the first dot

def draw():
    screen.fill("black")

    # Draw dots with numbers
    for i, dot in enumerate(dots):
        screen.draw.text(str(i + 1), (dot.pos[0], dot.pos[1] + 12), color="white")
        dot.draw()
    
    # Draw lines
    for line in lines:
        screen.draw.line(line[0], line[1], (0, 250, 0))
    
    # Draw Fox, hedgehog, police
    fox.draw()
    hedgehog.draw()
    police.draw()
    
    # Display game status
    screen.draw.text(f"Time Left: {remaining_time} s", topleft=(10, 10), color="white")

    # If paused, show rules
    if paused:
        screen.draw.filled_rect(Rect(50, 50, WIDTH-100, HEIGHT-100), (20, 20, 20))  # Dark background
        screen.draw.textbox(rules_text, Rect(100, 100, WIDTH-200, HEIGHT-200), color="white")

    # if game over
    if game_over:
        screen.fill("black")
        screen.draw.text(winner, center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="white")

def close_game():
    print("Closing game...")
    quit()

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

def on_mouse_down(pos):
    global next_dot, lines, game_over, winner
    if game_over:
        return
    
    if dots[next_dot].collidepoint(pos):
        if next_dot > 0:
            lines.append((dots[next_dot - 1].pos, dots[next_dot].pos))
        next_dot += 1
        
        if next_dot == len(dots):
            game_over = True
            winner = "Clicker wins! All dots connected!"
            clock.schedule_unique(close_game, 5.0)
    else:
        lines.clear()
        next_dot = 0

def update():
    global paused, game_over, fox_progress, hedgehog_progress, police_progress, winner
    
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
    
    # Check if fox reaches the next dot
    if fox_progress < len(dots) and fox.colliderect(dots[fox_progress]):
        fox_progress += 1
        print(f"Fox connects {fox_progress} dot")
        if fox_progress == len(dots):
            game_over = True
            winner = "Fox wins! Collected all dots!"
            clock.schedule_unique(close_game, 5.0)

    # Check if hedgehog reaches the next dot
    if hedgehog_progress < len(dots) and hedgehog.colliderect(dots[hedgehog_progress]):
        hedgehog_progress += 1
        print(f"Hedgehog connects {hedgehog_progress} dot")
        if hedgehog_progress == len(dots):
            game_over = True
            winner = "Hedgehog wins! Collected all dots!"
            clock.schedule_unique(close_game, 5.0)

     # Check if police reaches the next dot
    if police_progress < len(dots) and police.colliderect(dots[police_progress]):
        police_progress += 1
        print(f"Police connects {police_progress} dot")
        if police_progress == len(dots):
            game_over = True
            winner = "Police wins! Collected all dots!"
            clock.schedule_unique(close_game, 5.0)

clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

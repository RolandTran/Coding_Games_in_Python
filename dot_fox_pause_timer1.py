import pgzrun
from random import randint
import time

WIDTH, HEIGHT = 700, 700

# List of dots and lines
dots = []
lines = []

# Game State Variables
next_dot = 0  # Player's progress
fox_progress = 0  # Fox's progress
remaining_time = 60
paused = False
game_over = False
winner = ""

# Create 10 dots at random positions
for _ in range(10):
    actor = Actor("dot")
    actor.pos = randint(20, WIDTH - 20), randint(20, HEIGHT - 20)
    dots.append(actor)

# Initialize Fox
fox = Actor("fox")
fox.pos = 100, 100  # Start at the first dot

def draw():
    screen.fill("black")

    # Draw dots with numbers
    for i, dot in enumerate(dots):
        screen.draw.text(str(i + 1), (dot.pos[0], dot.pos[1] + 12), color="white")
        dot.draw()
    
    # Draw lines
    for line in lines:
        screen.draw.line(line[0], line[1], (100, 0, 0))
    
    # Draw Fox
    fox.draw()
    
    # Display game status
    screen.draw.text(f"Time Left: {remaining_time} s", topleft=(10, 10), color="white")
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
    global paused, game_over, fox_progress, winner
    
    if keyboard.space and not game_over:
        paused = not paused
        if not paused:
            clock.schedule_unique(update_timer, 1.0)
    
    if game_over or paused:
        return
    
    # Move fox using keyboard controls
    if not game_over:
        if keyboard.left:
            fox.x -= 6
        elif keyboard.right:
            fox.x += 6
        elif keyboard.up:
            fox.y -= 6
        elif keyboard.down:
            fox.y += 6

    # Keep fox within game boundaries
    fox.x = max(0, min(WIDTH, fox.x))
    fox.y = max(0, min(HEIGHT, fox.y))
    
    # Check if fox reaches the next dot
    if fox_progress < len(dots) and fox.colliderect(dots[fox_progress]):
        fox_progress += 1
        if fox_progress == len(dots):
            game_over = True
            winner = "Fox wins! Collected all dots!"
            clock.schedule_unique(close_game, 5.0)

clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

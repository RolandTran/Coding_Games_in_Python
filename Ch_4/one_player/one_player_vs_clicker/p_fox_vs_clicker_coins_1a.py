import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 800

# Game variables
score_fox = 0.0
score_clicker = 0.0
paused = False
space_pressed = False
time_left = 90
game_over = False

# Fox
fox = Actor("fox", (100, 100))

# All coins in ONE structure ✅
coins = [
    {"actor": Actor("coin"), "value": 1.00},
    {"actor": Actor("penny"), "value": 0.01},
    {"actor": Actor("nickel"), "value": 0.05},
    {"actor": Actor("dime"), "value": 0.10},
    {"actor": Actor("quarter"), "value": 0.25},
    {"actor": Actor("halfdollar"), "value": 0.50},
    {"actor": Actor("dollar"), "value": 1.00}
]

# Random placement function for all coins
def place_actor(actor):
    actor.x = randint(20, WIDTH - 20)
    actor.y = randint(20, HEIGHT - 20)

# Place everything once
for c in coins:
    place_actor(c["actor"])
place_actor(fox)

rules_text = """
PAUSED - GAME RULES:

- Arrow keys move fox.
- Tap coins to score (clicker).
- Collect coins as fox to score.
- Highest score after 90s wins.
- SPACE pauses/resumes game.
"""

def draw():
    screen.fill("white")

    fox.draw()
    for c in coins:
        c["actor"].draw()

    screen.draw.text(f"Fox Score: {score_fox:.2f}", (10, 10))
    screen.draw.text(f"Clicker Score: {score_clicker:.2f}", (10, 30))
    screen.draw.text(f"Time: {time_left}", topright=(WIDTH-10, 10), color="red")

    if paused and not game_over:
        screen.draw.filled_rect(Rect(100,100,600,600),(0,0,0,180))
        screen.draw.textbox(rules_text, Rect(150,150,500,500), color="white")

    if game_over:
        screen.fill("lightblue")

        if score_fox > score_clicker:
            winner = "Fox Wins! 🦊"
        elif score_clicker > score_fox:
            winner = "Clicker Wins! 🖱️"
        else:
            winner = "Tie Game! 🤝"

        screen.draw.text(winner, center=(WIDTH/2, HEIGHT/2), fontsize=60)
        screen.draw.text(f"{score_fox:.2f} vs {score_clicker:.2f}",
                         center=(WIDTH/2, HEIGHT/2 + 50), fontsize=40)

def update_timer():
    global time_left, game_over
    if not paused and not game_over:
        time_left -= 1
        if time_left <= 0:
            game_over = True
    clock.schedule_unique(update_timer, 1.0)

def update():
    global paused, space_pressed, score_fox

    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
    elif not keyboard.space:
        space_pressed = False

    if paused or game_over:
        return

    # Movement + screen boundary
    if keyboard.left: fox.x = max(20, fox.x - 6)
    if keyboard.right: fox.x = min(WIDTH-20, fox.x + 6)
    if keyboard.up: fox.y = max(20, fox.y - 6)
    if keyboard.down: fox.y = min(HEIGHT-20, fox.y + 6)

    # Fox collision with ANY coin ✅
    for c in coins:
        if fox.colliderect(c["actor"]):
            score_fox += c["value"]
            place_actor(c["actor"])

def on_mouse_down(pos):
    global score_clicker, score_fox
    if game_over: return

    # Click on fox (penalty)
    if fox.collidepoint(pos):
        score_fox -= 0.10
        place_actor(fox)

    # Click any coin ✅
    for c in coins:
        if c["actor"].collidepoint(pos):
            score_clicker += c["value"]
            place_actor(c["actor"])
            break

clock.schedule_interval(update_timer, 1.0)
pgzrun.go()


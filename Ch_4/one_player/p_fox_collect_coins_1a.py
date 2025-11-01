import pgzrun
from random import randint

WIDTH, HEIGHT = 800, 800
score, game_over = 0, False

# Player
fox = Actor("fox", (100, 100))

# Define coins with (name, value)
coin_data = [
    ("coin", 1.00),
    ("penny", 0.01),
    ("nickel", 0.05),
    ("dime", 0.10),
    ("quarter", 0.25),
    ("halfdollar", 0.50),
    ("dollar", 1.00)
]

# Create coins dictionary
coins = {name: {"actor": Actor(name), "value": val} for name, val in coin_data}

# Place all coins randomly
def place(actor):
    actor.pos = (randint(20, WIDTH-20), randint(20, HEIGHT-20))

for c in coins.values():
    place(c["actor"])

def draw():
    screen.fill("white")
    fox.draw()
    for c in coins.values():
        c["actor"].draw()
    
    screen.draw.text(f"Score: ${score:.2f}", topright=(WIDTH-15, 10), fontsize=40, color="black")

    if game_over:
        screen.fill("pink")
        screen.draw.text("You Win!", center=(WIDTH/2, HEIGHT/2), fontsize=80, color="black")

def update():
    global score, game_over
    if game_over: return

    # Movement (diagonal allowed)
    if keyboard.left: fox.x -= 6
    if keyboard.right: fox.x += 6
    if keyboard.up: fox.y -= 6
    if keyboard.down: fox.y += 6

    # Check collisions with all coins
    for data in coins.values():
        actor, val = data["actor"], data["value"]
        if fox.colliderect(actor):
            score += val
            print(f"Your score is {score:.2f} USD")
            place(actor)

    if score >= 100:
        game_over = True

pgzrun.go()

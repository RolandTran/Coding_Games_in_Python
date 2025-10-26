import pgzrun
from random import randint

WIDTH, HEIGHT, score = 800, 800, 0

# Define coin values and margins
coins = {
    "coin": (1.00, 20),
    "penny": (0.01, 25),
    "nickel": (0.05, 15),
    "dime": (0.10, 20),
    "quarter": (0.25, 25),
    "halfdollar": (0.50, 15),
    "dollar": (1.00, 15),
}

# Create Actor objects and assign to dictionary
actors = {name: Actor(name) for name in coins}

# Place all coins randomly with margin
def place_all():
    for name, actor in actors.items():
        margin = coins[name][1]
        actor.pos = (randint(margin, WIDTH - margin), randint(margin, HEIGHT - margin))

def close_game():
    print("Closing game...")
    quit()

def draw():
    screen.fill("white")
    for actor in actors.values():
        actor.draw()
    screen.draw.text(f"Score: {round(score, 2)}", topright=(WIDTH - 15, 10), fontsize=30, color="black")

def on_mouse_down(pos):
    global score
    for name, actor in actors.items():
        if actor.collidepoint(pos):
            value = coins[name][0]
            score += value
            print(f"You clicked on the {name}! Your score is {round(score, 2)} USD.")
            margin = coins[name][1]
            actor.pos = (randint(margin, WIDTH - margin), randint(margin, HEIGHT - margin))
            return
    print(f"You missed! Game over! Your final score is {round(score, 2)} USD.")
    clock.schedule_unique(close_game, 3.0)

place_all()
pgzrun.go()

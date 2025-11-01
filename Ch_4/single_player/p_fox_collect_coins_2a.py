import pgzrun
from random import randint

WIDTH, HEIGHT = 800, 800
score, remaining_time = 0, 90
game_over, paused, space_pressed = False, False, False

# Player
fox = Actor("fox", (100, 100))

# Coins + values
coins = {
    Actor("coin"): 1.00,
    Actor("penny"): 0.01,
    Actor("nickel"): 0.05,
    Actor("dime"): 0.10,
    Actor("quarter"): 0.25,
    Actor("halfdollar"): 0.50,
    Actor("dollar"): 1.00
}

# Place coins randomly
def place(actor):
    actor.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

for c in coins: 
    place(c)

rules_text = """
PAUSED - GAME RULES:

- Move the fox with arrow keys.
- Collect coins to increase your USD.
- The game ends when you reach $100 or the timer runs out.
- Press SPACE to pause or resume the game.
"""

def draw():
    screen.fill("white")
    fox.draw()
    for c in coins: c.draw()
    screen.draw.text(f"Score: {score:.2f} USD", topright=(WIDTH-15, 10), fontsize=30, color="black")
    screen.draw.text(f"Time: {remaining_time}s", topleft=(10, 10), fontsize=30, color="black")

    if paused:
        screen.draw.filled_rect(Rect(100,100,WIDTH-200,HEIGHT-200),(0,0,0,180))
        screen.draw.textbox(rules_text.strip(), Rect(150,150,WIDTH-300,HEIGHT-300), color="white", align="left")

    if game_over:
        screen.fill("pink")
        screen.draw.text(f"Game Over! Final score: {score:.2f} USD", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")

def close_game():
    print("Closing game..."); quit()

def update_timer():
    global remaining_time, game_over
    if not paused and not game_over:
        remaining_time -= 1
        if remaining_time <= 0:
            game_over = True
            print(f"Time's up! Final score {score:.2f} USD")
            clock.schedule_unique(close_game, 3.0)
        else:
            clock.schedule_unique(update_timer, 1.0)
    else:
        clock.schedule_unique(update_timer, 1.0)

def update():
    global paused, space_pressed, score, game_over
    # Pause toggle
    if keyboard.space and not space_pressed and not game_over:
        paused, space_pressed = not paused, True
    elif not keyboard.space:
        space_pressed = False
    if paused or game_over: return

    # Movement
    if keyboard.left: fox.x -= 10
    if keyboard.right: fox.x += 10
    if keyboard.up: fox.y -= 10
    if keyboard.down: fox.y += 10

    # Coin collisions
    for c, value in coins.items():
        if fox.colliderect(c):
            score += value
            print(f"Your score is {score:.2f} USD")
            place(c)

    if score >= 100: game_over = True

clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

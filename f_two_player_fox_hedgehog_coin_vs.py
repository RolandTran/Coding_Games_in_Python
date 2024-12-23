import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 800

# Scores for both players
score_fox = 0
score_hedgehog = 0
game_over = False

# Define players
fox = Actor("fox")  # Player 1
fox.pos = 100, 100

hedgehog = Actor("hedgehog")  # Player 2
hedgehog.pos = 150, 150

# Define coin
coin = Actor("coin")
coin.pos = 200, 200

def draw():
    screen.fill("green")
    fox.draw()
    hedgehog.draw()
    coin.draw()
    # Display scores for both players
    screen.draw.text(f"Fox Score: {score_fox}", color="black", topleft=(10, 10))
    screen.draw.text(f"Hedgehog Score: {score_hedgehog}", color="black", topleft=(10, 30))

    if game_over:
        screen.fill("pink")
        if score_fox >= 100 or score_hedgehog >= 100:
            screen.draw.text("You Win!", topleft=(100, 200), fontsize=60, color="black")
        else:
            screen.draw.text("Game Over", topleft=(100, 200), fontsize=60, color="black")

def place_coin():
    coin.x = randint(20, WIDTH - 20)
    coin.y = randint(20, HEIGHT - 20)

def time_up():
    global game_over
    game_over = True

def update():
    global score_fox, score_hedgehog

    if not game_over:
        # Player 1 (Fox) controls:
        if keyboard.left:
            fox.x -= 6
        elif keyboard.right:
            fox.x += 6
        elif keyboard.up:
            fox.y -= 6
        elif keyboard.down:
            fox.y += 6

        # Player 2 (Hedgehog) controls:
        if keyboard.a:
            hedgehog.x -= 6
        elif keyboard.d:
            hedgehog.x += 6
        elif keyboard.w:
            hedgehog.y -= 6
        elif keyboard.s:
            hedgehog.y += 6

        # Keep fox within bounds
        fox.x = max(0, min(WIDTH, fox.x))
        fox.y = max(0, min(HEIGHT, fox.y))

        # Keep hedgehog within bounds
        hedgehog.x = max(0, min(WIDTH, hedgehog.x))
        hedgehog.y = max(0, min(HEIGHT, hedgehog.y))

        # Collision detection with the coin
        if fox.colliderect(coin):
            score_fox += 5
            place_coin()
        if hedgehog.colliderect(coin):
            score_hedgehog += 5
            place_coin()

clock.schedule(time_up, 60.0)
place_coin()

pgzrun.go()

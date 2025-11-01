import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 800

score = 0
game_over = False

# Define player
fox = Actor("fox")
fox.pos = 100, 100

# Define coins
coin = Actor("coin")
penny = Actor("penny")
nickel = Actor("nickel")
dime = Actor("dime")
quarter = Actor("quarter")
halfdollar = Actor("halfdollar")
dollar = Actor("dollar")

# Place coins at random start positions
def place_coin():
    coin.x = randint(20, WIDTH - 20)
    coin.y = randint(20, HEIGHT - 20)

def place_penny():
    penny.x = randint(20, WIDTH - 20)
    penny.y = randint(20, HEIGHT - 20)

def place_nickel():
    nickel.x = randint(20, WIDTH - 20)
    nickel.y = randint(20, HEIGHT - 20)

def place_dime():
    dime.x = randint(20, WIDTH - 20)
    dime.y = randint(20, HEIGHT - 20)

def place_quarter():
    quarter.x = randint(20, WIDTH - 20)
    quarter.y = randint(20, HEIGHT - 20)

def place_halfdollar():
    halfdollar.x = randint(20, WIDTH - 20)
    halfdollar.y = randint(20, HEIGHT - 20)

def place_dollar():
    dollar.x = randint(20, WIDTH - 20)
    dollar.y = randint(20, HEIGHT - 20)

# Put all coins on the board initially
place_coin()
place_penny()
place_nickel()
place_dime()
place_quarter()
place_halfdollar()
place_dollar()

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

    screen.draw.text(f"Score: ${score:.2f}", topright=(WIDTH-15, 10), fontsize=40, color="black")

    if game_over:
        screen.fill("pink")
        screen.draw.text("You Win!", center=(WIDTH/2, HEIGHT/2), fontsize=80, color="black")

def update():
    global score, game_over

    if not game_over: 
        # Movement (allow diagonal)
        if keyboard.left:
            fox.x -= 6
        if keyboard.right:
            fox.x += 6
        if keyboard.up:
            fox.y -= 6
        if keyboard.down:
            fox.y += 6

        # Collisions with coins
        if fox.colliderect(coin):
            score += 1.00
            print(f"Your score is {score:.2f} USD")
            place_coin()

        if fox.colliderect(penny):
            score += 0.01
            print(f"Your score is {score:.2f} USD")
            place_penny()

        if fox.colliderect(nickel):
            score += 0.05
            print(f"Your score is {score:.2f} USD")
            place_nickel()

        if fox.colliderect(dime):
            score += 0.10
            print(f"Your score is {score:.2f} USD")
            place_dime()

        if fox.colliderect(quarter):
            score += 0.25
            print(f"Your score is {score:.2f} USD")
            place_quarter()

        if fox.colliderect(halfdollar):
            score += 0.50
            print(f"Your score is {score:.2f} USD")
            place_halfdollar()

        if fox.colliderect(dollar):
            score += 1.00
            print(f"Your score is {score:.2f} USD")
            place_dollar()

        # Winning condition
        if score >= 100:
            game_over = True

pgzrun.go()

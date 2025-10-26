import pgzrun
from random import randint

score = 0
WIDTH = 800
HEIGHT = 800

# Define actors
coin = Actor("coin")
penny = Actor("penny")
nickel = Actor("nickel")
dime = Actor("dime")
quarter = Actor("quarter")
halfdollar = Actor("halfdollar")
dollar = Actor("dollar")

# Initial random positions
coin.pos = (randint(10, WIDTH), randint(10, HEIGHT))
penny.pos = (randint(10, WIDTH), randint(10, HEIGHT))
nickel.pos = (randint(10, WIDTH), randint(10, HEIGHT))
dime.pos = (randint(10, WIDTH), randint(10, HEIGHT))
quarter.pos = (randint(10, WIDTH), randint(10, HEIGHT))
halfdollar.pos = (randint(10, WIDTH), randint(10, HEIGHT))
dollar.pos = (randint(10, WIDTH), randint(10, HEIGHT))


def draw():
    screen.fill("white")
    coin.draw()
    penny.draw()
    nickel.draw()
    dime.draw()
    quarter.draw()
    halfdollar.draw()
    dollar.draw()
    screen.draw.text(f"Score: {round(score,2)}", topright=(WIDTH-15, 10), fontsize=30, color="black")

def place_coin():
    coin.x = randint(20, WIDTH - 20)
    coin.y = randint(20, HEIGHT - 20)

def place_penny():
    penny.x = randint(25, WIDTH - 15)
    penny.y = randint(25, HEIGHT - 15)

def place_nickel():
    nickel.x = randint(15, WIDTH - 25)
    nickel.y = randint(15, HEIGHT - 25)

def place_dime():
    dime.x = randint(20, WIDTH - 20)
    dime.y = randint(20, HEIGHT - 20)

def place_quarter():
    quarter.x = randint(25, WIDTH - 15)
    quarter.y = randint(25, HEIGHT - 15)

def place_halfdollar():
    halfdollar.x = randint(15, WIDTH - 25)
    halfdollar.y = randint(15, HEIGHT - 25)

def place_dollar():
    dollar.x = randint(15, WIDTH - 25)
    dollar.y = randint(15, HEIGHT - 25)


def close_game():
    print("Closing game...")
    quit()

def on_mouse_down(pos):
    global score # update score
    if coin.collidepoint(pos):
        score += 1.00
        print(f"You hit the coin! Your score is {score} USD. ")
        place_coin()
    elif penny.collidepoint(pos):
        score += 0.01
        print(f"You clicked on the penny! Your score is {score} USD.")
        place_penny()
    elif nickel.collidepoint(pos):
        score += 0.05
        print(f"You clicked on the nickel! Your score is {score} USD.")
        place_nickel()
    elif dime.collidepoint(pos):
        score += 0.10
        print(f"You clicked on the dime! Your score is {score} USD.")
        place_dime()
    elif quarter.collidepoint(pos):
        score += 0.25
        print(f"You clicked on the quarter! Your score is {score} USD.")
        place_quarter()
    elif halfdollar.collidepoint(pos):
        score += 0.50
        print(f"You clicked on the halfdollar! Your score is {score} USD.")
        place_halfdollar()
    elif dollar.collidepoint(pos):
        score += 1.00
        print(f"You clicked on the dollar. Your score is {score} USD.")
        place_dollar()
    else:
        print(f"You missed! Game over! Your final score is {round(score,2)}")
        clock.schedule_unique(close_game, 3.0)

place_coin()
place_penny()
place_nickel()
place_dime()
place_quarter()
place_halfdollar()
place_dollar()

pgzrun.go()

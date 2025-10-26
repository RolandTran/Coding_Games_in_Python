import pgzrun
from random import randint

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
    if coin.collidepoint(pos):
        print("Good shot! You hit the coin!")
        place_coin()
    elif penny.collidepoint(pos):
        print("You clicked on the penny!")
        place_penny()
    elif nickel.collidepoint(pos):
        print("You clicked on the nickel!")
        place_nickel()
    elif dime.collidepoint(pos):
        print("You clicked on the dime!")
        place_dime()
    elif quarter.collidepoint(pos):
        print("You clicked on the quarter!")
        place_quarter()
    elif halfdollar.collidepoint(pos):
        print("You clicked on the halfdollar!")
        place_halfdollar()
    elif dollar.collidepoint(pos):
        print("You clicked on the dollar")
        place_dollar()
    else:
        print("You missed! Game over!")
        clock.schedule_unique(close_game, 3.0)

place_coin()
place_penny()
place_nickel()
place_dime()
place_quarter()
place_halfdollar()
place_dollar()

pgzrun.go()

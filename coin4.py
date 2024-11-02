import pgzrun
from random import randint

WIDTH = 400
HEIGHT = 400

score = 0
game_over = False
initials = ""

fox = Actor("fox")
fox.pos = 100, 100

coin = Actor("coin")
coin.pos = 200, 200

input_box = Rect(100, 250, 200, 50)
input_active = True

def draw():
    screen.fill("green")
    fox.draw()
    coin.draw()
    screen.draw.text("Score: " + str(score), color="black", topleft=(10, 10))

    if game_over:
        screen.fill("pink")
        if score >= 100:
            screen.draw.text("You Win!", topleft=(100, 200), fontsize=60, color="black")
        else:
            screen.draw.text("Game Over", topleft=(100, 200), fontsize=60, color="black")
        
        screen.draw.text("Enter Initials:", topleft=(100, 300), fontsize=30, color="black")
        screen.draw.text(initials, topleft=(250, 300), fontsize=30, color="black")
        
def on_key_down(key):
    global initials, input_active, game_over
    
    if game_over and input_active:
        if key == keys.BACKSPACE:
            initials = initials[:-1]
        elif key == keys.RETURN:
            save_score()
            input_active = False
            game_over = False
        elif len(initials) < 3:
            # Convert the key to a string
            initials += chr(key)

def save_score():
    # You can implement saving the score with initials to a file or a database here.
    print("Score saved:", initials, score)
    pgzrun.quit()

def place_coin():
    coin.x = randint(20, WIDTH - 20)
    coin.y = randint(20, HEIGHT - 20)

def time_up():
    global game_over
    game_over = True

def update():
    global score

    if not game_over:
        if keyboard.left:
            fox.x -= 2
        elif keyboard.right:
            fox.x += 2
        elif keyboard.up:
            fox.y -= 2
        elif keyboard.down:
            fox.y += 2

        if fox.colliderect(coin):
            score += 10
            place_coin()

clock.schedule(time_up, 30.0)
place_coin()

pgzrun.go()



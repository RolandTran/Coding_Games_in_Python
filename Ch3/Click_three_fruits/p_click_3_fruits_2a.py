import pgzrun
from random import randint

score = 0
remaining_time = 60
paused = False
game_over = False
space_pressed = False

WIDTH = 800
HEIGHT = 800

# Define actors
apple = Actor("apple")
pineapple = Actor("pineapple")
orange = Actor("orange")

# Initial random positions
apple.pos = (randint(10, WIDTH), randint(10, HEIGHT))
pineapple.pos = (randint(10, WIDTH), randint(10, HEIGHT))
orange.pos = (randint(10, WIDTH), randint(10, HEIGHT))


def draw():
    screen.clear()
    apple.draw()
    pineapple.draw()
    orange.draw()
    screen.draw.text(f"Score: {score}", topright=(WIDTH-15, 10), fontsize=30, color="white")
    screen.draw.text(f"Time: {remaining_time}s", topleft=(10, 10), fontsize=30, color="white")
    if paused:
        screen.draw.text("Paused", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="yellow")
    if game_over:
        screen.draw.text("Time's up!", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=60, color="red")


def place_apple():
    apple.x = randint(20, WIDTH - 20)
    apple.y = randint(20, HEIGHT - 20)

def place_orange():
    orange.x = randint(25, WIDTH - 15)
    orange.y = randint(25, HEIGHT - 15)

def place_pineapple():
    pineapple.x = randint(15, WIDTH - 25)
    pineapple.y = randint(15, HEIGHT - 25)

def close_game():
    print("Closing game...")
    quit()

def update_timer():
    global remaining_time, game_over
    if not paused and not game_over:
        remaining_time -= 1
        if remaining_time <= 0:
            game_over = True
            print(f"Time's up! Your final score was {score}.")
            clock.schedule_unique(close_game, 3.0)
        else:
            clock.schedule_unique(update_timer, 1.0)
    else:
        # Keep checking every second while paused
        clock.schedule_unique(update_timer, 1.0)

def update():
    global paused, space_pressed
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
    elif not keyboard.space:
        space_pressed = False

def on_mouse_down(pos):
    global score # score is global level and must be declared
    if apple.collidepoint(pos):
        print(f"Good shot! You hit the apple! Your score is {score}")
        score += 1
        place_apple()
    elif pineapple.collidepoint(pos):
        print("Oops! You clicked on the pineapple by mistake!")
        place_pineapple()
    elif orange.collidepoint(pos):
        print("Oops! You clicked on the orange by mistake!")
        place_orange()
    else:
        print("You missed! Game over!")
        clock.schedule_unique(close_game, 2.0)

place_apple()
place_pineapple()
place_orange()

# Remove or define update_timer if needed
clock.schedule_unique(update_timer, 1.0)

pgzrun.go()

import pgzrun
from random import randint

score = 0
remaining_time = 60
game_over = False
WIDTH = 800
HEIGHT = 600

apple = Actor("apple")
apple.pos = (randint(10, 800), randint(10, 600))

def draw():
    screen.clear()
    apple.draw()
    screen.draw.text(f"Score: {score}", topright=(WIDTH - 15, 10), fontsize=30, color="white")
    screen.draw.text(f"Time: {remaining_time}s", topleft=(10, 10), fontsize=30, color="white")
    if game_over:
        screen.draw.text("Time's up!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")

def close_game():
    print("Closing game...")
    quit()

def update_timer():
    global remaining_time, game_over
    remaining_time -= 1
    if remaining_time <= 0:
        game_over = True
        print(f"Time's up! Your final score was {score}.")
        clock.schedule_unique(close_game, 3.0)
    else:
        clock.schedule_unique(update_timer, 1.0)
        

def on_mouse_down(pos):
    global score
    if not game_over:
        if apple.collidepoint(pos):
            score += 1
            print(f"Good shot! You hit the apple! Your score is {score}")
            apple.pos = (randint(10, 800), randint(10, 600))
        else:
            print("Missed!")
            clock.schedule_unique(close_game, 3.0)

# Start the timer when the game launches
clock.schedule_unique(update_timer, 1.0)

pgzrun.go()

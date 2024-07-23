import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 600

apple = Actor("apple")
pineapple = Actor("pineapple")
orange = Actor("orange")
kiwi = Actor("kiwi")
roland = Actor("roland")
actors = [apple, pineapple, orange, kiwi, roland]  # List of all actors

score = 0  # Initialize the score variable
timer = 30  # Game duration in seconds
game_over = False
top_scores = [("AAA", 0), ("BBB", 0), ("CCC", 0)]  # Initialize top 3 scores with initials
initials = ""
input_active = True

def draw():
    screen.clear()
    for actor in actors:
        actor.draw()
    screen.draw.text("Score: " + str(score), topleft=(10, 10), color="white", fontsize=30)
    screen.draw.text("Time: " + str(int(timer)), topleft=(WIDTH - 100, 10), color="white", fontsize=30)

    if game_over:
        screen.fill("black")
        screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=60, color="red")
        screen.draw.text("Your Score: " + str(score), center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="white")
        screen.draw.text("Enter Initials: " + initials, center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=30, color="white")
        screen.draw.text("Top Scores:", center=(WIDTH // 2, HEIGHT // 2 + 100), fontsize=40, color="white")
        
        for i, (initial, top_score) in enumerate(top_scores):
            screen.draw.text(f"{i + 1}. {initial}: {top_score}", center=(WIDTH // 2, HEIGHT // 2 + 150 + i * 40), fontsize=30, color="white")

def place_actors():
    for actor in actors:
        actor.pos = (randint(10, WIDTH - 10), randint(10, HEIGHT - 10))

def on_mouse_down(pos):
    global score, game_over
    if game_over:
        return
    
    actor_clicked = False  # Flag to track if any actor was clicked
    for actor in actors:
        if actor.collidepoint(pos):
            if actor == apple:
                print("Good shot! You hit the apple!")
                score += 1
            elif actor == pineapple:
                print("Oops! You clicked on the pineapple by mistake!")
            elif actor == orange:
                print("Oops! You clicked on the orange by mistake!")
            elif actor == roland:
                print("Oops! You clicked on the roland by mistake!")
            elif actor == kiwi:
                print("Oops! You clicked on the kiwi by mistake!")
            place_actors()  # Reset actor position
            actor_clicked = True
            break

    if not actor_clicked:
        print("You missed!")

def on_key_down(key):
    global initials, input_active, game_over
    if game_over and input_active:
        if key == keys.BACKSPACE:
            initials = initials[:-1]
        elif key == keys.RETURN and len(initials) > 0:
            save_score()
            input_active = False
        elif len(initials) < 3 and key != keys.RETURN:
            initials += chr(key).upper()

def save_score():
    global top_scores
    top_scores.append((initials, score))
    top_scores = sorted(top_scores, key=lambda x: x[1], reverse=True)[:3]
    print("Scores saved:", top_scores)
    with open("top_scores.txt", "w") as file:
        for initial, top_score in top_scores:
            file.write(f"{initial},{top_score}\n")

def load_scores():
    global top_scores
    try:
        with open("top_scores.txt", "r") as file:
            top_scores = [tuple(line.strip().split(',')) for line in file]
            top_scores = [(initial, int(top_score)) for initial, top_score in top_scores]
    except FileNotFoundError:
        pass

def update():
    global timer, game_over
    if not game_over:
        if timer > 0:
            timer -= 1 / 60
        else:
            game_over = True

def time_up():
    global game_over
    game_over = True

clock.schedule(time_up, 30.0)
place_actors()
load_scores()
pgzrun.go()

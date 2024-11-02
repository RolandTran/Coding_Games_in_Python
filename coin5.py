import pgzrun # Imports Pygame Zero library, provides a framework for creating games.
import os # This imports the os module, which provides functions for interacting with the operating system, including file operations.
from random import randint # This imports the randint function from the random module, which is used later to generate random positions for the coin.

WIDTH = 400
HEIGHT = 400
#  These variables define the width and height of the game window.

score = 0 # This variable stores the player's score.
game_over = False # This variable tracks whether the game is over or not.
initials = "" # This variable stores the player's initials.

top_scores_file = "top_scores.txt" # This variable specifies the name of the file where the top scores will be saved.

fox = Actor("fox")
fox.pos = 100, 100
# These lines create an actor object representing the player character (a fox) and set its initial position.

coin = Actor("coin")
coin.pos = 200, 200
# These lines create an actor object representing the coin and set its initial position.

input_box = Rect(100, 250, 200, 50) # This line defines a rectangular area on the screen where the player can enter their initials.
input_active = True # This variable tracks whether the input box for entering initials is active.

def load_top_scores(): # load top scores fxn
    if os.path.exists(top_scores_file):
        with open(top_scores_file, "r") as file:
            top_scores = file.readlines()
            return [line.strip().split(",") for line in top_scores]
    else:
        return []

# This function loads the top scores from the top_scores.txt file, if it exists. It reads the file line by line, 
# splits each line into initials and score, and returns a list of tuples containing initials and scores.


def save_top_scores(top_scores):
    with open(top_scores_file, "w") as file:
        for score in top_scores:
            file.write(",".join(score) + "\n")

# saves top scores to the top_scores.txt file. Opens the file in write mode, 
# iterates over the top scores, joins each tuple of initials and score with a comma, 
# and writes it to the file.

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

# This function is called to draw the game screen. It fills the screen with a green color, 
# draws the player character (fox), the coin, and the current score. If the game is over, 
# it fills the screen with pink color, displays a "You Win!" or "Game Over" message, 
# prompts the player to enter their initials, and displays the entered initials.

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

# This function is called when a key is pressed. If the game is over and the input box is active, 
# it handles key presses for entering initials. If the Backspace key is pressed, 
# it removes the last character from the initials. If the Enter key is pressed, it saves the score and initials, 
# deactivates the input box, and sets the game over flag to False. 
# If the length of the initials is less than 3 and a valid key is pressed, 
# it adds the pressed key (converted to a character) to the initials.

def save_score():
    global score
    top_scores = load_top_scores()
    top_scores.append([initials, str(score)])
    top_scores.sort(key=lambda x: int(x[1]), reverse=True)
    top_scores = top_scores[:3]  # Keep only top 3 scores
    save_top_scores(top_scores)
    print_top_scores(top_scores)
    pgzrun.quit()

# This function is called to save the score and initials to the top scores file. 
# It loads the current top scores, appends the current score and initials, 
# sorts the top scores in descending order based on the score, keeps only the top 3 scores, 
# saves the updated top scores to the file, prints the top scores to the terminal, and quits the game.


def print_top_scores(top_scores):
    print("Top 3 Scores:")
    for i, (initials, score) in enumerate(top_scores):
        print(f"{i+1}. {initials}: {score}")

# This function prints the top 3 scores to the terminal in the format "Rank. Initials: Score".

def place_coin():
    coin.x = randint(20, WIDTH - 20)
    coin.y = randint(20, HEIGHT - 20)

# This function is called to randomly place the coin on the screen within the game window boundaries.

def time_up():
    global game_over
    game_over = True

# This function is called when the game time is up. It sets the game over flag to True.

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

# This function is called every frame to update the game state. If the game is not over, 
# it checks for keyboard input to move the player character (fox) and detects collisions with the coin to update the score.
# It also schedules the time_up() function to be called after 30 seconds and places the coin on the screen.

clock.schedule(time_up, 30.0) # This line schedules the time_up() function to be called after 30 seconds.
place_coin() # This line calls the place_coin() function to place the coin on the screen.

pgzrun.go() 
# This line starts the Pygame Zero game loop, which handles drawing the screen, updating the game state, and handling user input.


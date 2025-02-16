import pgzrun
from random import randint
import time

WIDTH, HEIGHT = 800, 800
score = {'fox': 0, 'police': 0, 'hedgehog': 0, 'a': 0, 'clicker': 0}
game_over, winner, paused = False, None, False
remaining_time, total_pause_time, pause_start_time = 60, 0, 0

actors = {name: Actor(name, (randint(20, WIDTH - 20), randint(20, HEIGHT - 20))) 
          for name in ['fox', 'police', 'hedgehog', 'a', 'coin', 'quarter', 'dime', 'nickel', 'halfdollar', 'one']}

def draw():
    screen.fill("white")
    # Iterates through all actors (characters and coins) stored in the actors dictionary and draws them on the screen.
    for actor in actors.values(): 
        actor.draw()
    # Loops through the score dictionary, which keeps track of each player's score
    for i, (player, sc) in enumerate(score.items()): # enumerate() is used to get both the index (i) and the key-value pair (player, sc).
        screen.draw.text(f"{player.capitalize()} score: {round(sc, 2)} USD", color="black", topleft=(10, 10 + i * 20))
        # The position of the text is determined dynamically (10 + i * 20), so each score appears below the previous one.
    screen.draw.text(f"Time Left: {remaining_time} seconds", color="black", topright=(750, 10))
    if game_over:
        screen.fill("pink")
        screen.draw.text(f"{winner.capitalize()} wins! {round(score[winner], 2)} USD." if winner else "Game Over", 
                         topleft=(100, 200), fontsize=60, color="black")

def place_actor(name):
    actors[name].pos = (randint(20, WIDTH - 20), randint(20, HEIGHT - 20))

def exit_game():
    quit()
    
def time_up():
    global game_over, winner
    game_over = True
    winner = max(score, key=score.get)
    clock.schedule_unique(exit_game, 5.0)

def update_timer():
    global remaining_time
    if game_over or paused:
        return
    remaining_time -= 1
    if remaining_time <= 0:
        time_up()
    else:
        clock.schedule_unique(update_timer, 1.0)

def on_mouse_down(pos): # function is trigged whenever player clicks mouse on coordinate of mouse clic (pos)
    global score # modificaiton of score dictionary
    # Iterates over a dictionary where coin names are keys and their monetary values are values.
    for name, value in {'coin': 0.01, 'quarter': 0.25, 'dime': 0.10, 'nickel': 0.05, 'halfdollar': 0.50, 'one': 1.00}.items():
        # Checks if the mouse click's position pos intersects (collides) with the position of a coin actor.
        if actors[name].collidepoint(pos):
            print(f"Good click! You hit the {name} and gained ${value:.2f} USD.")
            score['clicker'] += value
            place_actor(name)
            return
    for name in ['fox', 'police', 'hedgehog', 'a']:
        if actors[name].collidepoint(pos):
            print(f"Oh no! You hit the {name} and lost $1.00 USD.")
            score['clicker'] -= 1.00
            place_actor(name)
            return
    print("You missed! Lost $2.00 USD.")
    score['clicker'] -= 2.00

def update(): # runs every frame to update game state, modifes paused, pause_start_time, total_pause_time, 
    global paused, pause_start_time, total_pause_time
    # Toggles the paused state when the spacebar is pressed.
    if keyboard.space:
        paused = not paused
        pause_start_time = time.time() if paused else total_pause_time + time.time() - pause_start_time
        clock.schedule_unique(update_timer, 1.0) if not paused else None
    if paused or game_over:
        return
    # define movement control, A dictionary that maps each character (fox, police, hedgehog, a) to their movement keys.
    movement = {"fox": (keyboard.left, keyboard.right, keyboard.up, keyboard.down),
                "police": (keyboard.a, keyboard.d, keyboard.w, keyboard.s),
                "hedgehog": (keyboard.f, keyboard.h, keyboard.t, keyboard.g),
                "a": (keyboard.j, keyboard.l, keyboard.i, keyboard.k)}
    # moving each character; loops thru each character and assigned key movements
    for name, (left, right, up, down) in movement.items():
        if left: actors[name].x -= 6
        if right: actors[name].x += 6
        if up: actors[name].y -= 6
        if down: actors[name].y += 6
        # Ensures that characters stay inside the screen boundaries.
        actors[name].x = max(0, min(WIDTH, actors[name].x))
        actors[name].y = max(0, min(HEIGHT, actors[name].y))
        # checking for coin collision, 
        for obj in ['coin', 'quarter', 'dime', 'nickel', 'halfdollar', 'one']:
            # Loops through all coin objects and checks if the character collides with one.
            if actors[name].colliderect(actors[obj]):
                # Adds the coin's value to the character’s score.
                score[name] += {'coin': 0.01, 'quarter': 0.25, 'dime': 0.10, 'nickel': 0.05, 'halfdollar': 0.50, 'one': 1.00}[obj]
                place_actor(obj) # moves coin to new random position
        # check for collision between characters
        for opponent in ['fox', 'police', 'hedgehog', 'a']: # Loops through all other characters and checks for collisions
            if opponent != name and actors[name].colliderect(actors[opponent]):
                score[name] -= 0.25
                place_actor(name)

clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

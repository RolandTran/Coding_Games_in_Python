import pgzrun
from random import randint
import time

WIDTH, HEIGHT = 800, 800  # These define the size of the game window: 800 pixels wide and 800 pixels tall.

# Initialize individual player scores
score_fox = score_police = score_hedgehog = score_a = 0
paused = game_over = False
winner = None
remaining_time, total_pause_time = 60, 0

# Define actors
actors = {
    'fox': Actor("fox", (100, 100)), 'police': Actor("police", (150, 150)),
    'hedgehog': Actor("hedgehog", (50, 75)), 'a': Actor("a", (225, 175)),
    'coin': Actor("coin"), 'quarter': Actor("quarter"), 'dime': Actor("dime"),
    'nickel': Actor("nickel"), 'halfdollar': Actor("halfdollar"), 'one': Actor("one")
}
coins = ['coin', 'quarter', 'dime', 'nickel', 'halfdollar', 'one']
values = {'coin': 0.01, 'quarter': 0.25, 'dime': 0.1, 'nickel': 0.05, 'halfdollar': 0.5, 'one': 1.0}  # Coin values


# Place coin randomly (x, y) and update position of specific coin
def place_coin(coin):
    actors[coin].pos = randint(20, WIDTH - 20), randint(20, HEIGHT - 20)


# Draw screen
def draw():
    screen.fill("green")  # Green background
    for actor in actors.values():
        actor.draw()  # Draw all actors on the screen
    # Display individual scores
    screen.draw.text(f"Fox Score: {round(score_fox, 2)} USD", color="black", topleft=(10, 10))
    screen.draw.text(f"Police Score: {round(score_police, 2)} USD", color="black", topleft=(10, 30))
    screen.draw.text(f"Hedgehog Score: {round(score_hedgehog, 2)} USD", color="black", topleft=(10, 50))
    screen.draw.text(f"A Score: {round(score_a, 2)} USD", color="black", topleft=(10, 70))
    # Display paused or remaining time
    if paused:
        screen.draw.text("Paused", color="red", center=(WIDTH // 2, HEIGHT // 2), fontsize=50)
    else:
        screen.draw.text(f"Time Left: {remaining_time} s", color="black", topright=(750, 10))
    # Game over screen
    if game_over:
        screen.fill("pink")
        msg = f"{winner} Wins! {round(max(score_fox, score_police, score_hedgehog, score_a), 2)} USD." if winner else "Game Over"
        screen.draw.text(msg, topleft=(100, 200), fontsize=60, color="black")


# Timer update
def update_timer():
    global remaining_time, game_over, winner
    if game_over or paused:
        return  # Exit if the game is over or paused
    remaining_time -= 1
    if remaining_time <= 0:
        game_over = True
        # Determine the winner based on the highest score
        scores = {'Fox': score_fox, 'Police': score_police, 'Hedgehog': score_hedgehog, 'A': score_a}
        winner = max(scores, key=scores.get) if max(scores.values()) > 0 else None
    else:
        clock.schedule_unique(update_timer, 1.0)


# Update positions and scores
def update():
    global score_fox, score_police, score_hedgehog, score_a, paused, total_pause_time
    if keyboard.space:
        paused = not paused
        total_pause_time += time.time() if not paused else -time.time()
        if not paused:
            clock.schedule_unique(update_timer, 1.0)  # Resume the timer when unpaused
    if paused or game_over:
        return  # Exit function if game is paused or over

    # Define movement keys for each player
    controls = {
        actors['fox']: {'left': 'left', 'right': 'right', 'up': 'up', 'down': 'down'},
        actors['police']: {'left': 'a', 'right': 'd', 'up': 'w', 'down': 's'},
        actors['hedgehog']: {'left': 'f', 'right': 'h', 'up': 't', 'down': 'g'},
        actors['a']: {'left': 'j', 'right': 'l', 'up': 'i', 'down': 'k'}
    }

    # Move players based on keyboard input and keep them within screen boundaries
    for player, keys in controls.items():
        if keyboard[keys['left']]:
            player.x -= 6
        if keyboard[keys['right']]:
            player.x += 6
        if keyboard[keys['up']]:
            player.y -= 6
        if keyboard[keys['down']]:
            player.y += 6
        player.x, player.y = max(0, min(WIDTH, player.x)), max(0, min(HEIGHT, player.y))

    # Detect when a player touches a coin; update scores and move coin to a new random position
    for coin in coins:
        for player, score_var in [(actors['fox'], 'score_fox'), (actors['police'], 'score_police'),
                                  (actors['hedgehog'], 'score_hedgehog'), (actors['a'], 'score_a')]:
            if player.colliderect(actors[coin]):
                globals()[score_var] += values[coin]  # Update the score for the corresponding player
                place_coin(coin)


# Initialize game
for coin in coins:
    place_coin(coin)  # Randomly position all coins at the start
clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

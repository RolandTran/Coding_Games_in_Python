import pgzrun
from random import randint
import time

WIDTH = 800
HEIGHT = 800

score_Team_A = score_Team_B = 0
paused = game_over = False
winner = None
remaining_time, total_pause_time = 60, 0

# Define actors
actors = {
    'fox': Actor("fox", (100, 100)), 'police': Actor("police", (150, 150)),
    'hedgehog': Actor("hedgehog", (50, 75)), 'a': Actor("a", (125, 175)),
    'coin': Actor("coin"), 'quarter': Actor("quarter"), 'dime': Actor("dime"),
    'nickel': Actor("nickel"), 'halfdollar': Actor("halfdollar"), 'one': Actor("one")
}
coins = ['coin', 'quarter', 'dime', 'nickel', 'halfdollar', 'one']     
values = {'coin': 0.01, 'quarter': 0.25, 'dime': 0.1, 'nickel': 0.05, 'halfdollar': 0.5, 'one': 1.0}
Team_A, Team_B = [actors['fox'], actors['hedgehog']], [actors['police'], actors['a']]

# Place coin randomly
def place_coin(coin):
    actors[coin].pos = randint(20, WIDTH - 20), randint(20, HEIGHT - 20)

# Draw screen
def draw():
    screen.fill("green")
    for actor in actors.values(): actor.draw()
    screen.draw.text(f"Team A Score: {round(score_Team_A, 2)} USD", color="black", topleft=(10, 10))
    screen.draw.text(f"Team B Score: {round(score_Team_B, 2)} USD", color="black", topleft=(10, 30))
    if paused:
        screen.draw.text("Paused", color="red", center=(WIDTH // 2, HEIGHT // 2), fontsize=50)
    else:
        screen.draw.text(f"Time Left: {remaining_time} s", color="black", topright=(750, 10))
    if game_over:
        screen.fill("pink")
        msg = f"{winner} Wins! {round(score_Team_A if winner=='Team A' else score_Team_B, 2)} USD." if winner else "Game Over"
        screen.draw.text(msg, topleft=(100, 200), fontsize=60, color="black")

# Timer update
def update_timer():
    global remaining_time, game_over, winner
    if game_over or paused: return
    remaining_time -= 1
    if remaining_time <= 0:
        game_over = True
        winner = "Team A" if score_Team_A > score_Team_B else "Team B" if score_Team_B > score_Team_A else None
    else: clock.schedule_unique(update_timer, 1.0)

# Update positions and scores
def update():
    global score_Team_A, score_Team_B, paused, total_pause_time        
    if keyboard.space:
        paused = not paused
        total_pause_time += time.time() if not paused else -time.time()
        if not paused: clock.schedule_unique(update_timer, 1.0)        
    if paused or game_over: return

    controls = {
        actors['fox']: {'left': 'left', 'right': 'right', 'up': 'up', 'down': 'down'},
        actors['police']: {'left': 'a', 'right': 'd', 'up': 'w', 'down': 's'},  
        actors['hedgehog']: {'left': 'f', 'right': 'h', 'up': 't', 'down': 'g'},
        actors['a']: {'left': 'j', 'right': 'l', 'up': 'i', 'down': 'k'}
    }       

    for player, keys in controls.items():
        if keyboard[keys['left']]: player.x -= 6
        if keyboard[keys['right']]: player.x += 6
        if keyboard[keys['up']]: player.y -= 6
        if keyboard[keys['down']]: player.y += 6
        player.x, player.y = max(0, min(WIDTH, player.x)), max(0, min(HEIGHT, player.y))

    for coin in coins:
        for player in Team_A + Team_B:
            if player.colliderect(actors[coin]):
                if player in Team_A: score_Team_A += values[coin]      
                else: score_Team_B += values[coin]
                place_coin(coin)

# Initialize game
for coin in coins: place_coin(coin)
clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

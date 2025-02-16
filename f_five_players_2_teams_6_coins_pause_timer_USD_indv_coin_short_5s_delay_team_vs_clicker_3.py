import pgzrun
from random import randint
import time

WIDTH, HEIGHT = 800, 800
score_team, score_clicker = 0, 0
paused, game_over, winner = False, False, None
remaining_time, pause_start_time, total_pause_time = 60, 0, 0

# Set FIXED starting positions for actors
fixed_positions = {
    "fox": (100, 100), "police": (300, 100), "hedgehog": (500, 100), "a": (700, 100),
    "coin": (200, 400), "quarter": (400, 400), "dime": (600, 400), 
    "nickel": (200, 600), "halfdollar": (400, 600), "one": (600, 600)
}

# Initialize actors at FIXED positions
actors = {name: Actor(name, pos) for name, pos in fixed_positions.items()}
team = ["fox", "police", "hedgehog", "a"]

values = {"coin": 0.01, "quarter": 0.25, "dime": 0.1, "nickel": 0.05, "halfdollar": 0.5, "one": 1.0}
penalties = {"fox": -1.0, "police": -1.0, "hedgehog": -1.0, "a": -1.0}


def draw():
    screen.fill("white")
    for actor in actors.values():
        actor.draw()
    screen.draw.text(f"Team: {round(score_team, 2)} USD", (10, 10), color="black")
    screen.draw.text(f"Clicker: {round(score_clicker, 2)} USD", (10, 30), color="black")
    screen.draw.text(f"Time Left: {remaining_time}s", (600, 10), color="black", align="right")
    if paused:
        screen.draw.text("Paused", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="red")
    if game_over:
        screen.fill("pink")
        screen.draw.text(f"{winner.capitalize()} wins! {round(max(score_team, score_clicker), 2)} USD.", (100, 200), fontsize=60, color="black")


def move_actor(name):
    """Move an actor to a new random location within the screen."""
    actors[name].pos = (randint(50, WIDTH - 50), randint(50, HEIGHT - 50))


def exit_game():
    quit()

def time_up():
    global game_over, winner
    game_over, winner = True, "team" if score_team > score_clicker else "clicker" if score_clicker > score_team else "none"
    clock.schedule_unique(exit_game, 5.0)


def update_timer():
    global remaining_time
    if not (game_over or paused):
        remaining_time -= 1
        if remaining_time <= 0:
            time_up()
        else:
            clock.schedule_unique(update_timer, 1.0)


def on_mouse_down(pos):
    global score_clicker
    for name, actor in actors.items():
        if actor.collidepoint(pos):
            if name in values:
                score_clicker += values[name]
                print(f"Clicked {name}! +${values[name]:.2f} USD")
            else:
                score_clicker -= 1.00
                print(f"Clicked {name}! -$1.00 USD")
            move_actor(name)  # Move the clicked actor
            return
    print("You missed! -$2.00 USD")
    score_clicker -= 2.00


def update():
    global paused, pause_start_time, total_pause_time, score_team
    if keyboard.space:
        paused = not paused
        if paused:
            pause_start_time = time.time()
        else:
            total_pause_time += time.time() - pause_start_time
            clock.schedule_unique(update_timer, 1.0)
    if paused or game_over:
        return

    # Player movement controls
    controls = {
        "fox": (keyboard.left, keyboard.right, keyboard.up, keyboard.down),
        "police": (keyboard.a, keyboard.d, keyboard.w, keyboard.s),
        "hedgehog": (keyboard.f, keyboard.h, keyboard.t, keyboard.g),
        "a": (keyboard.j, keyboard.l, keyboard.i, keyboard.k)
    }
    
    # Move each player only when keys are pressed
    for name, (left, right, up, down) in controls.items():
        if left: actors[name].x -= 6
        if right: actors[name].x += 6
        if up: actors[name].y -= 6
        if down: actors[name].y += 6

        # Keep within bounds
        actors[name].x = max(0, min(WIDTH, actors[name].x))
        actors[name].y = max(0, min(HEIGHT, actors[name].y))
        
        # Actor colliding with coins (collecting them)
        for coin in values:
            if actors[name].colliderect(actors[coin]):
                score_team += values[coin]
                print(f"{name} collected {coin}! +${values[coin]:.2f} USD")
                move_actor(coin)  # Move the collected coin
        
        # Actor colliding with another actor (penalty & movement)
        for teammate in team:
            if name != teammate and actors[name].colliderect(actors[teammate]):
                score_team -= 0.25
                print(f"{name} collided with {teammate}! -$0.25 USD")
                move_actor(name)  # Move the colliding actor
                move_actor(teammate)  # Move the teammate too

clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

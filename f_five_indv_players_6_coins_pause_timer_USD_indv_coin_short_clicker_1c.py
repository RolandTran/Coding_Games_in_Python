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
    for actor in actors.values():
        actor.draw()
    for i, (player, sc) in enumerate(score.items()):
        screen.draw.text(f"{player.capitalize()} score: {round(sc, 2)} USD", color="black", topleft=(10, 10 + i * 20))
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

def on_mouse_down(pos):
    global score
    for name, value in {'coin': 0.01, 'quarter': 0.25, 'dime': 0.10, 'nickel': 0.05, 'halfdollar': 0.50, 'one': 1.00}.items():
        if actors[name].collidepoint(pos):
            score['clicker'] += value
            place_actor(name)
            return
    for name in ['fox', 'police', 'hedgehog', 'a']:
        if actors[name].collidepoint(pos):
            score['clicker'] -= 1.00
            place_actor(name)
            return
    score['clicker'] -= 2.00

def update():
    global paused, pause_start_time, total_pause_time
    if keyboard.space:
        paused = not paused
        pause_start_time = time.time() if paused else total_pause_time + time.time() - pause_start_time
        clock.schedule_unique(update_timer, 1.0) if not paused else None
    if paused or game_over:
        return
    movement = {"fox": (keyboard.left, keyboard.right, keyboard.up, keyboard.down),
                "police": (keyboard.a, keyboard.d, keyboard.w, keyboard.s),
                "hedgehog": (keyboard.f, keyboard.h, keyboard.t, keyboard.g),
                "a": (keyboard.j, keyboard.l, keyboard.i, keyboard.k)}
    for name, (left, right, up, down) in movement.items():
        if left: actors[name].x -= 6
        if right: actors[name].x += 6
        if up: actors[name].y -= 6
        if down: actors[name].y += 6
        actors[name].x = max(0, min(WIDTH, actors[name].x))
        actors[name].y = max(0, min(HEIGHT, actors[name].y))
        for obj in ['coin', 'quarter', 'dime', 'nickel', 'halfdollar', 'one']:
            if actors[name].colliderect(actors[obj]):
                score[name] += {'coin': 0.01, 'quarter': 0.25, 'dime': 0.10, 'nickel': 0.05, 'halfdollar': 0.50, 'one': 1.00}[obj]
                place_actor(obj)
        for opponent in ['fox', 'police', 'hedgehog', 'a']:
            if opponent != name and actors[name].colliderect(actors[opponent]):
                score[name] -= 0.25
                place_actor(name)

clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

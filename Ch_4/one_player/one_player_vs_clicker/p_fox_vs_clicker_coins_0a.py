import pgzrun
from random import randint

WIDTH = 800
HEIGHT = 800

fox = Actor("fox", (100, 100))
score_fox = 0.0
score_clicker = 0.0
game_over = False
time_left = 90

coins = {
    Actor("coin"): 1.00,
    Actor("penny"): 0.01,
    Actor("nickel"): 0.05,
    Actor("dime"): 0.10,
    Actor("quarter"): 0.25,
    Actor("halfdollar"): 0.50,
    Actor("dollar"): 1.00
}

def place(actor):
    actor.pos = randint(20, WIDTH-20), randint(20, HEIGHT-20)

for c in coins:
    place(c)

def draw():
    screen.fill("white")
    fox.draw()
    for c in coins: c.draw()

    screen.draw.text(f"Fox Score: {score_fox:.2f}", (10,10), color="black")
    screen.draw.text(f"Clicker Score: {score_clicker:.2f}", (10,30), color="black")
    screen.draw.text(f"Time Left: {time_left}", (10,50), color="red")

    if game_over:
        screen.fill("lightblue")
        if score_fox > score_clicker: msg = "Fox Wins! 🦊"
        elif score_clicker > score_fox: msg = "Clicker Wins! 🖱️"
        else: msg = "It's a Tie! 🤝"

        screen.draw.text(msg, center=(WIDTH/2, HEIGHT/2), fontsize=60, color="black")
        screen.draw.text(
            f"Fox: {score_fox:.2f} | Clicker: {score_clicker:.2f}",
            center=(WIDTH/2, HEIGHT/2+60),
            fontsize=40,
            color="black"
        )

def update():
    global score_fox
    if game_over: return

    if keyboard.left: fox.x -= 6
    if keyboard.right: fox.x += 6
    if keyboard.up: fox.y -= 6
    if keyboard.down: fox.y += 6

    for c, val in coins.items():
        if fox.colliderect(c):
            score_fox += val
            place(c)

def on_mouse_down(pos):
    global score_clicker
    if game_over: return

    for c, val in coins.items():
        if c.collidepoint(pos):
            score_clicker += val
            place(c)
            break

def countdown():
    global time_left, game_over
    time_left -= 1
    if time_left <= 0:
        game_over = True

clock.schedule_interval(countdown, 1.0)
pgzrun.go()

import pgzrun
from random import randint

WIDTH, HEIGHT = 800, 600
actors = {
    "apple": Actor("apple"),
    "pineapple": Actor("pineapple"),
    "orange": Actor("orange")
}

def draw():
    screen.clear()
    for actor in actors.values():
        actor.draw()

def place(actor, margin=20):
    actor.pos = (randint(margin, WIDTH - margin), randint(margin, HEIGHT - margin))

def close_game():
    print("Closing game...")
    quit()

def on_mouse_down(pos):
    for name, actor in actors.items():
        if actor.collidepoint(pos):
            if name == "apple":
                print("Good shot! You hit the apple!")
            else:
                print(f"Oops! You clicked on the {name} by mistake!")
            place(actor)
            return
    print("You missed! Game over!")
    clock.schedule_unique(close_game, 3.0)

# Initial placement with optional margins
place(actors["apple"], 20)
place(actors["pineapple"], 25)
place(actors["orange"], 15)

pgzrun.go()

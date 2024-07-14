import pgzrun

WIDTH = 800
HEIGHT = 600

# Initialize the actors with images
apple = Actor("apple")
orange = Actor("orange")
pineapple = Actor("pineapple")
kiwi = Actor("kiwi")
roland = Actor("roland")

# Initial positions
apple.pos = (WIDTH // 2, HEIGHT // 2)
orange.pos = (WIDTH - orange.width // 2 - 50, orange.height // 2 + 50)
pineapple.pos = (pineapple.width // 2 + 50, pineapple.height // 2 + 50)
kiwi.pos = (WIDTH - kiwi.width // 2 - 50, HEIGHT - kiwi.height // 2 - 50)
roland.pos = (roland.width // 2 + 50, HEIGHT - roland.height // 2 - 50)

def draw():
    screen.clear()

    apple.draw()
    orange.draw()
    pineapple.draw()
    kiwi.draw()
    roland.draw()

def on_mouse_down(pos):
    if apple.collidepoint(pos):
        print("Apple clicked! Moving to bottom right.")
        move_to_bottom_right(apple)
    elif orange.collidepoint(pos):
        print("Orange clicked! Moving to center.")
        move_to_center(orange)
    elif pineapple.collidepoint(pos):
        print("Pineapple clicked! Moving to top left.")
        move_to_top_left(pineapple)
    elif kiwi.collidepoint(pos):
        print("Kiwi clicked! Moving to top left.")
        move_to_top_left(kiwi)
    elif roland.collidepoint(pos):
        print("Roland clicked! Moving to bottom left.")
        move_to_bottom_left(roland)
    else:
        print("Game over!")
        quit()

def move_to_center(actor):
    actor.pos = (WIDTH // 2, HEIGHT // 2)

def move_to_bottom_right(actor):
    actor.pos = (WIDTH - actor.width // 2 - 50, HEIGHT - actor.height // 2 - 50)

def move_to_top_left(actor):
    actor.pos = (actor.width // 2 + 50, actor.height // 2 + 50)

def move_to_bottom_left(actor):
    actor.pos = (actor.width // 2 + 50, HEIGHT - actor.height // 2 - 50)

pgzrun.go()

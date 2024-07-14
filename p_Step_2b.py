import pgzrun

WIDTH = 800
HEIGHT = 600

apple = Actor("apple")

def draw():
    screen.clear()
    apple.draw()

def place_apple_center():
    apple.x = WIDTH // 2
    apple.y = HEIGHT // 2

def place_apple_top_right():
    apple.x = WIDTH - apple.width // 2
    apple.y = apple.height // 2

def place_apple_top_left():
    apple.x = apple.width // 2
    apple.y = apple.height // 2

def place_apple_bottom_right():
    apple.x = WIDTH - apple.width // 2
    apple.y = HEIGHT - apple.height // 2

def place_apple_bottom_left():
    apple.x = apple.width // 2
    apple.y = HEIGHT - apple.height // 2

# Initially place the apple in the center
place_apple_center()

pgzrun.go()

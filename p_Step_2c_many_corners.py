import pgzrun

WIDTH = 800
HEIGHT = 600

apple = Actor("apple")
orange = Actor("orange")
pineapple = Actor("pineapple")
kiwi = Actor("kiwi")
roland = Actor("roland")

def draw():
    screen.clear()
    apple.draw()
    orange.draw()
    pineapple.draw()
    kiwi.draw()
    roland.draw()

def place_apple_center():
    apple.x = WIDTH // 2
    apple.y = HEIGHT // 2

def place_orange_top_right():
    orange.x = WIDTH - orange.width // 2
    orange.y = orange.height // 2

def place_pineapple_top_left():
    pineapple.x = pineapple.width // 2
    pineapple.y = pineapple.height // 2

def place_kiwi_bottom_right():
    kiwi.x = WIDTH - kiwi.width // 2
    kiwi.y = HEIGHT - kiwi.height // 2

def place_roland_bottom_left():
    roland.x = roland.width // 2
    roland.y = HEIGHT - roland.height // 2

# Place the images in their respective positions
place_apple_center()
place_orange_top_right()
place_pineapple_top_left()
place_kiwi_bottom_right()
place_roland_bottom_left()

pgzrun.go()


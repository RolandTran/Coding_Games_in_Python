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

    # Place apple at the center
    apple.pos = (WIDTH // 2, HEIGHT // 2)
    apple.draw()

    # Place orange at the top right
    orange.pos = (WIDTH - orange.width // 2 - 50, orange.height // 2 + 50)
    orange.draw()

    # Place pineapple at the top left
    pineapple.pos = (pineapple.width // 2 + 10, pineapple.height // 2 + 10)
    pineapple.draw()

    # Place kiwi at the bottom right
    kiwi.pos = (WIDTH - kiwi.width // 2 - 50, HEIGHT - kiwi.height // 2 - 50)
    kiwi.draw()

    # Place roland at the bottom left
    roland.pos = (roland.width // 2 + 50, HEIGHT - roland.height // 2 - 50)
    roland.draw()

pgzrun.go()


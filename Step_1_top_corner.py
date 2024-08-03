import pgzrun

WIDTH = 800
HEIGHT = 600

apple = Actor("apple")
def draw():
    screen.clear( )
    apple.draw( )


# Start the Pygame Zero loop
pgzrun.go()

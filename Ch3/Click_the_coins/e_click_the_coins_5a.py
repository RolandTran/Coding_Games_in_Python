import pygame
import pgzrun
from random import randint, choice

score, time_left, paused, game_over, space_pressed = 0, 60, False, False, False
WIDTH, HEIGHT = 800, 800

pygame.mixer.init()
pygame.mixer.music.load("music/jamesbondtheme.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Coin setup
coin_names = ["coin", "penny", "nickel", "dime", "quarter", "halfdollar", "dollar"]
coin_values = [1.00, 0.01, 0.05, 0.10, 0.25, 0.50, 1.00]
coins = [Actor(name, pos=(randint(10, WIDTH), randint(10, HEIGHT)), 
               dx=choice([-3, -2, -1, 1, 2, 3]), dy=choice([-3, -2, -1, 1, 2, 3]), angle=0) 
         for name in coin_names]

def draw():
    screen.fill("white")
    for coin in coins:
        coin.draw()
    screen.draw.text(f"Score: {round(score,2)} USD", topright=(WIDTH-15, 10), fontsize=30, color="black")
    screen.draw.text(f"Time: {time_left}s", topleft=(10, 10), fontsize=30, color="black")
    if game_over:
        screen.draw.text(f"Time's up! Final score is {round(score,2)}", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")

def update_timer():
    global time_left, game_over
    if not paused and not game_over:
        time_left -= 1
        if time_left <= 0:
            game_over = True
            print(f"Time's up! Your final score was {score}.")
            clock.schedule_unique(lambda: quit(), 3.0)
        else:
            clock.schedule_unique(update_timer, 1.0)

def move_coins():
    for coin in coins:
        coin.x += coin.dx
        coin.y += coin.dy
        if coin.left < 0 or coin.right > WIDTH: coin.dx *= -1
        if coin.top < 0 or coin.bottom > HEIGHT: coin.dy *= -1
        coin.angle = (coin.angle + 5) % 360  # Rotate

def update():
    global paused, space_pressed
    if keyboard.space and not space_pressed and not game_over:
        paused = not paused
        space_pressed = True
        pygame.mixer.music.pause() if paused else pygame.mixer.music.unpause()
        if not paused: clock.schedule_unique(update_timer, 1.0)
    elif not keyboard.space:
        space_pressed = False
    if not paused and not game_over: move_coins()

def on_mouse_down(pos):
    global score
    if paused or game_over: return
    for coin, value in zip(coins, coin_values):
        if coin.collidepoint(pos):
            score += value
            print(f"You clicked on {coin.image}! Score: {round(score,2)} USD.")
            coin.pos = (randint(10, WIDTH), randint(10, HEIGHT))
            return
    print(f"You missed! Game over! Final score: {round(score,2)}")
    clock.schedule_unique(lambda: quit(), 1.5)

clock.schedule_unique(update_timer, 1.0)
pgzrun.go()

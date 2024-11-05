import pgzrun

# Define screen dimensions
WIDTH = 800
HEIGHT = 600

# Create actor instances
apple = Actor("apple")
orange = Actor("orange")
pineapple = Actor("pineapple")
kiwi = Actor("kiwi")
roland = Actor("roland")

# List of actors for easy management
actors = [apple, orange, pineapple, kiwi, roland]

# Counterclockwise positions for the apple
apple_positions = [
    (WIDTH // 2, HEIGHT // 2),             # Center
    (WIDTH - apple.width // 2 - 50, apple.height // 2 + 50),  # Top right
    (WIDTH - apple.width // 2 - 50, HEIGHT - apple.height // 2 - 50), # Bottom right
    (apple.width // 2 + 50, HEIGHT - apple.height // 2 - 50), # Bottom left
    (apple.width // 2 + 50, apple.height // 2 + 50),          # Top left
]

# Counterclockwise positions for the kiwi
kiwi_positions = [
    (WIDTH // 2, HEIGHT // 2),             # Center
    (apple.width // 2 + 50, apple.height // 2 + 50),          # Top left
    (apple.width // 2 + 50, HEIGHT - apple.height // 2 - 50), # Bottom left
    (WIDTH - apple.width // 2 - 50, HEIGHT - apple.height // 2 - 50), # Bottom right
    (WIDTH - apple.width // 2 - 50, apple.height // 2 + 50),  # Top right
]

# Initialize positions indices
apple_position_index = 0  # Start at the center for apple
kiwi_position_index = 0   # Start at the center for kiwi

# Place actors in their initial positions
def place_actors():
    global apple_position_index, kiwi_position_index

    # Update apple's position to the next in the list
    apple.pos = apple_positions[apple_position_index]
    apple_position_index = (apple_position_index - 1) % len(apple_positions)

    # Update kiwi's position to the next in the list
    kiwi.pos = kiwi_positions[kiwi_position_index]
    kiwi_position_index = (kiwi_position_index - 1) % len(kiwi_positions)

    # Position the other fruits in fixed positions
    orange.pos = (WIDTH - orange.width // 2 - 50, orange.height // 2 + 50)
    pineapple.pos = (pineapple.width // 2 + 50, pineapple.height // 2 + 50)
    roland.pos = (roland.width // 2 + 50, HEIGHT - roland.height // 2 - 50)

place_actors()  # Initialize positions

def draw():
    # Clear the screen
    screen.clear()

    # Draw each actor
    for actor in actors:
        actor.draw()

# Handle mouse click events
def on_mouse_down(pos):
    actor_clicked = False  # Track if any actor was clicked

    # Check each actor for collision
    for actor in actors:
        if actor.collidepoint(pos):
            actor_clicked = True  # An actor was clicked
            if actor == apple or actor == kiwi:
                print(f"You clicked the {actor.image}! It's moving counterclockwise.")
                # Move the apple and kiwi to the next counterclockwise position
                place_actors()
            else:
                print(f"Oops! You clicked on the {actor.image} by mistake!")

            break

    if not actor_clicked:
        print("You missed!")
        quit()

pgzrun.go()

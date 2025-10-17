import pygame
import pymunk
import pymunk.pygame_util
import sys
import random

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Game")

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Pymunk setup
space = pymunk.Space()
space.gravity = (0, -50)  # Negative gravity makes balloons rise
balloons = []

draw_options = pymunk.pygame_util.DrawOptions(screen)
frame_count = 0
running = True

# Load images
balloon_image = pygame.image.load("balloon.png").convert_alpha()
balloon_image = pygame.transform.scale(balloon_image, (150, 150))
background = pygame.image.load("balloonbg.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load sounds
pop_sound = pygame.mixer.Sound("balloon-pop.mp3")
background_music = pygame.mixer.Sound("background_music.mp3")

# Play background music on loop
background_music.set_volume(0.3)
background_music.play(-1)

# Function to create a balloon
def create_balloon():
    x = random.randint(75, 725)  # X position
    y = 500  # Starting Y position
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 25))  # Body of the balloon
    body.position = x, y
    shape = pymunk.Circle(body, 25)  # Shape of the balloon
    shape.elasticity = 0
    shape.friction = 0.5
    space.add(body, shape)
    return body, shape

# Timer logic
frame_count = 0
max_frames = 900  # 30 seconds at 60 FPS

# Game loop
while running:
    screen.blit(background, (0, 0))

    # Randomly create balloons
    if random.randint(1, 30) == 1:
        balloons.append(create_balloon())

    # Timer display
    time_left = max(0, (max_frames - frame_count) // 60)
    font = pygame.font.SysFont(None, 36)
    screen.blit(font.render(f"Time Left: {time_left}s", True, (0, 0, 0)), (600, 10))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)

            popped_balloons = []
            for body, shape in balloons:
                x, y = body.position
                balloon_rect = pygame.Rect(x - 75, y - 75, 150, 150)
                if balloon_rect.colliderect(mouse_rect):
                    pop_sound.play()  # Play pop sound when balloon clicked
                    popped_balloons.append((body, shape))

            # Remove popped balloons
            for balloon in popped_balloons:
                balloons.remove(balloon)
                space.remove(*balloon)

    # Draw balloons
    for body, shape in balloons:
        x, y = body.position
        screen.blit(balloon_image, (x - 75, y - 75))

    # Physics step
    space.step(1 / FPS)

    # Update frame counter
    frame_count += 1

    pygame.display.flip()
    clock.tick(FPS)

# Quit pygame
pygame.quit()
sys.exit()

# ------------------- Difficulty -------------------
import random

difficulty = input("Select difficulty (E=Easy, M=Medium, H=Hard, R=Random): ").strip().upper()

if difficulty == "R":
    difficulty = random.choice(["E", "M", "H"])
    print(f"Your difficulty is - '{difficulty}'")

if difficulty == "E":
    balloon_spawn_rate = 45
    star_spawn_rate = 45
    winning_score = 3000
    max_frames = 3600
elif difficulty == "M":
    balloon_spawn_rate = 50
    star_spawn_rate = 35
    winning_score = 4000
    max_frames = 3600
elif difficulty == "H":
    balloon_spawn_rate = 55
    star_spawn_rate = 25
    winning_score = 5000
    max_frames = 3600
else:
    print(f"Invalid input '{difficulty}', defaulting to Medium")
    # Use actual Medium values for default
    balloon_spawn_rate = 50
    star_spawn_rate = 40
    winning_score = 4000
    max_frames = 3600


# ---- Libraries ----
import pygame
import pymunk
import pymunk.pygame_util
import sys

# --- Initialize Pygame ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Game")
clock = pygame.time.Clock()
FPS = 60

# --- Pymunk Setup ---
space = pymunk.Space()
space.gravity = (0, -50)  # Negative gravity makes balloons rise

# --- Font ---
font = pygame.font.Font(None, 48)

# --- Game State Variables ---
frame_count = 0
running = True
balloons = []
stars = []
score = 0
gameover = False
gamewin = False
gameover_sound_played = False  # New flag to play sound only once

# --- Load Assets ---
balloon_image = pygame.image.load("balloon_image.png").convert_alpha()
balloon_image = pygame.transform.scale(balloon_image, (150, 150))

star_image = pygame.image.load("star_image.png").convert_alpha()
star_image = pygame.transform.scale(star_image, (60, 60))

background = pygame.image.load("balloon_background_image.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

pop_sound = pygame.mixer.Sound("balloon-pop.mp3")
pop_sound.set_volume(0.3)

gameover_sound = pygame.mixer.Sound("gameover_balloon_game.mp3")
gamewin_sound = pygame.mixer.Sound("gamewin_balloon_game.mp3")
lose_points_sound = pygame.mixer.Sound("lose_points_sound.mp3")

background_music = pygame.mixer.Sound("background_music_balloon_game.mp3")
background_music.set_volume(0.3)
background_music.play(-1)

draw_options = pymunk.pygame_util.DrawOptions(screen)


# --- Functions ---
def create_balloon():
    x = random.randint(75, 725)
    y = 500
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 25))
    body.position = x, y
    shape = pymunk.Circle(body, 25)
    shape.elasticity = 0
    shape.friction = 0.5
    space.add(body, shape)
    return body, shape


def create_star():
    x = random.randint(75, 725)
    y = 500
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 25))
    body.position = x, y
    shape = pymunk.Circle(body, 25)
    shape.elasticity = 0
    shape.friction = 0.5
    space.add(body, shape)
    return body, shape


def timer(frame_count, fps, total_frames):
    time_left = max(0, (total_frames - frame_count) // fps)
    timer_text = font.render(f"Time: {time_left}", True, (255, 255, 255))
    screen.blit(timer_text, (WIDTH - 200, 20))
    return time_left


# --- Main Game Loop ---
while running:
    screen.blit(background, (0, 0))
    frame_count += 1

    # Randomly create balloons and stars based on difficulty
    if not gameover and random.randint(1, balloon_spawn_rate) == 1:
        balloons.append(create_balloon())
    if not gameover and random.randint(1, star_spawn_rate) == 1:
        stars.append(create_star())

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not gameover:
            mouse_pos = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 5, 5)  # slightly bigger click area

            # BALLOONS
            popped_balloons = []
            for body, shape in balloons:
                x, y = body.position
                balloon_rect = pygame.Rect(x - 75, y - 75, 150, 150)
                if balloon_rect.colliderect(mouse_rect):
                    pop_sound.play()
                    popped_balloons.append((body, shape))
                    score += 100

            # STARS
            clicked_stars = []
            for body, shape in stars:
                x, y = body.position
                star_rect = pygame.Rect(x - 30, y - 30, 60, 60)
                if star_rect.colliderect(mouse_rect):
                    lose_points_sound.play()
                    clicked_stars.append((body, shape))
                    score -= 100

            # Remove popped balloons
            for balloon in popped_balloons:
                balloons.remove(balloon)
                space.remove(balloon[0], balloon[1])

            # Remove clicked stars
            for star in clicked_stars:
                stars.remove(star)
                space.remove(star[0], star[1])

    # Draw balloons and stars
    if not gameover:
        for body, shape in balloons[:]:
            x, y = body.position
            screen.blit(balloon_image, (x - 75, y - 75))
            if y < -100:
                balloons.remove((body, shape))
                space.remove(body, shape)

        for body, shape in stars[:]:
            x, y = body.position
            screen.blit(star_image, (x - 30, y - 30))
            if y < -100:
                stars.remove((body, shape))
                space.remove(body, shape)

    # Display score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    # Display timer
    time_left = timer(frame_count, FPS, max_frames)

    # Game conditions
    if not gameover:
        if score >= winning_score:
            gamewin = True
            gameover = True
        elif frame_count >= max_frames:
            gamewin = False
            gameover = True
            # Handle Game Over / Win
    if gameover:
        if not gameover_sound_played:
            background_music.stop()
            if gamewin:
                gamewin_sound.play()
                text_surface = font.render("YOU WIN!", True, (255, 255, 0))
            else:
                gameover_sound.play()
                text_surface = font.render("YOU LOST!", True, (255, 0, 0))
            
            gameover_sound_played = True

            # Display message
            screen.blit(background, (0, 0))
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.delay(3000)

            # Exit game cleanly after showing message
            running = False
            break

    # Physics step
    space.step(1 / FPS)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
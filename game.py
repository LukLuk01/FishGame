import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 300, 600  # Overall screen size
PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT = 27, 290  # Play area dimensions
FPS = 60
SLOW_UP_SPEED = 0.6  # Slightly increased speed for slow upward movement
FAST_UP_SPEED = 1.5  # Speed for fast upward movement
FISH_GRAVITY = 0.1  # Gravity effect on the fish
FISH_JUMP_FORCE = -2  # Jump force applied to the fish
MAX_FALL_SPEED = 0.5  # Maximum speed when falling

# Colors
GREEN = (39, 78, 19)  # Slow upward movement
PURPLE = (88, 47, 100)  # Slow downward movement
BROWN = (82, 82, 33)  # Stop movement
BLUE = (35, 74, 93)  # Fast upward movement
BLACK = (0, 0, 0)  # Background color
WHITE = (255, 255, 255)  # Text color
GREY = (100, 100, 100)  # Button color

# Initialize the screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Fish Game")

# Load the fish image
fish_image = pygame.image.load("image.png")
fish_rect = fish_image.get_rect()

# Initial positions
play_area_x = (WINDOW_WIDTH - PLAY_AREA_WIDTH) // 2  # Position play area in the center-left
play_area_y = (WINDOW_HEIGHT - PLAY_AREA_HEIGHT) // 2
rect_height = random.randint(90, 120)  # Randomized height for the rectangle
rect_y = play_area_y + PLAY_AREA_HEIGHT - rect_height  # Align rectangle to the bottom of the play area
fish_rect.center = (play_area_x + PLAY_AREA_WIDTH // 2, rect_y + rect_height // 2)  # Fish centered in the rectangle
movement_mode = "slow_up"  # Default movement mode

# Fish velocity
fish_velocity = 0

# Score
score = 0

# Effects
effects_used = 0
MAX_EFFECTS = 2
current_effect_duration = 0
space_pressed = False

# Buttons
button_font = pygame.font.Font(None, 24)
start_button = pygame.Rect(10, 10, 80, 30)
stop_button = pygame.Rect(10, 50, 80, 30)

# Font for displaying text
font = pygame.font.Font(None, 36)

# Countdown function
def countdown():
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, (play_area_x, rect_y, PLAY_AREA_WIDTH, rect_height))
        pygame.draw.rect(screen, WHITE, (play_area_x - 2, play_area_y - 2, PLAY_AREA_WIDTH + 4, PLAY_AREA_HEIGHT + 4), 2)  # Play area outline
        screen.blit(fish_image, fish_rect)
        countdown_text = font.render(str(i), True, WHITE)
        screen.blit(countdown_text, (WINDOW_WIDTH // 2 - countdown_text.get_width() // 2, WINDOW_HEIGHT // 2))
        pygame.display.flip()
        time.sleep(1)
    start_text = font.render("Start!", True, WHITE)
    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, (play_area_x, rect_y, PLAY_AREA_WIDTH, rect_height))
    pygame.draw.rect(screen, WHITE, (play_area_x - 2, play_area_y - 2, PLAY_AREA_WIDTH + 4, PLAY_AREA_HEIGHT + 4), 2)  # Play area outline
    screen.blit(fish_image, fish_rect)
    screen.blit(start_text, (WINDOW_WIDTH // 2 - start_text.get_width() // 2, WINDOW_HEIGHT // 2))
    pygame.display.flip()
    time.sleep(1)

# Reset game function
def reset_game():
    global rect_height, rect_y, fish_rect, movement_mode, fish_velocity, score, effects_used, current_effect_duration
    rect_height = random.randint(90, 120)
    rect_y = play_area_y + PLAY_AREA_HEIGHT - rect_height
    fish_rect.center = (play_area_x + PLAY_AREA_WIDTH // 2, rect_y + rect_height // 2)
    movement_mode = "slow_up"  # Reset to default green effect
    fish_velocity = 0
    effects_used = 0
    current_effect_duration = 0

# Game state
game_active = False

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            space_pressed = True
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            space_pressed = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                if not game_active:
                    countdown()
                    game_active = True
                    reset_game()
            if stop_button.collidepoint(event.pos):
                game_active = False

    if game_active:
        # Fish controls
        if space_pressed:
            fish_velocity = FISH_JUMP_FORCE
            space_pressed = False  # Reset after jump

        # Apply gravity to the fish
        fish_velocity += FISH_GRAVITY
        fish_velocity = min(fish_velocity, MAX_FALL_SPEED)  # Limit falling speed
        fish_rect.y += fish_velocity

        # Check if the fish is outside the play area
        if not fish_rect.colliderect(pygame.Rect(play_area_x, play_area_y, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT)) \
            or not fish_rect.colliderect(pygame.Rect(play_area_x, rect_y, PLAY_AREA_WIDTH, rect_height)):
            game_active = False  # End game

        # Update rectangle movement based on the mode
        if current_effect_duration <= 0:
            if effects_used < MAX_EFFECTS and random.random() < 0.005:
                movement_mode = random.choice(["fast_up", "slow_down", "stopped"])
                effects_used += 1

                # Set effect duration
                current_effect_duration = random.randint(60, 240)  # 1 to 4 seconds
            else:
                movement_mode = "slow_up"  # Default green mode after effects

        else:
            current_effect_duration -= 1

        if movement_mode == "slow_up":
            rect_y -= SLOW_UP_SPEED
        elif movement_mode == "fast_up":
            rect_y -= FAST_UP_SPEED
        elif movement_mode == "slow_down":
            rect_y += SLOW_UP_SPEED

        # Ensure rectangle stays within bounds
        if rect_y < play_area_y:
            rect_y = play_area_y
            movement_mode = "stopped"
        if rect_y + rect_height > play_area_y + PLAY_AREA_HEIGHT:
            rect_y = play_area_y + PLAY_AREA_HEIGHT - rect_height
            movement_mode = "stopped"

        # Check for scoring
        if fish_rect.colliderect(pygame.Rect(play_area_x, rect_y, PLAY_AREA_WIDTH, rect_height)):
            if rect_y <= play_area_y:
                score += 1
                reset_game()

    # Drawing elements
    screen.fill(BLACK)

    pygame.draw.rect(screen, WHITE, (play_area_x - 2, play_area_y - 2, PLAY_AREA_WIDTH + 4, PLAY_AREA_HEIGHT + 4), 2)  # Play area outline

    if game_active:
        # Draw rectangle and effects
        if movement_mode == "slow_up":
            pygame.draw.rect(screen, GREEN, (play_area_x, rect_y, PLAY_AREA_WIDTH, rect_height))
        elif movement_mode == "fast_up":
            pygame.draw.rect(screen, BLUE, (play_area_x, rect_y, PLAY_AREA_WIDTH, rect_height))
        elif movement_mode == "slow_down":
            pygame.draw.rect(screen, PURPLE, (play_area_x, rect_y, PLAY_AREA_WIDTH, rect_height))
        elif movement_mode == "stopped":
            pygame.draw.rect(screen, BROWN, (play_area_x, rect_y, PLAY_AREA_WIDTH, rect_height))

        screen.blit(fish_image, fish_rect)

        # Draw the score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    # Draw buttons
    pygame.draw.rect(screen, GREY, start_button)
    pygame.draw.rect(screen, GREY, stop_button)
    start_text = button_font.render("Start", True, WHITE)
    stop_text = button_font.render("Stop", True, WHITE)
    screen.blit(start_text, (start_button.x + 10, start_button.y + 5))
    screen.blit(stop_text, (stop_button.x + 10, stop_button.y + 5))

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

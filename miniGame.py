import pygame
import random
import time

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class FishMiniGame:
    def __init__(self,fish_game, screen):
        self.fish_game = fish_game
        self.screen = screen

        self.PLAY_AREA_WIDTH, self.PLAY_AREA_HEIGHT = 27, 290
        self.FPS = 60
        self.SLOW_UP_SPEED = 0.6
        self.FAST_UP_SPEED = 1.5
        self.FISH_GRAVITY = 0.1
        self.FISH_JUMP_FORCE = -2
        self.MAX_FALL_SPEED = 0.5
        
        # Colors
        self.COLORS = {
            "slow_up": (39, 78, 19),  # Green
            "fast_up": (35, 74, 93),  # Blue
            "slow_down": (88, 47, 100),  # Purple
            "stopped": (82, 82, 33),  # Brown
            "background": (0, 0, 0),
            "text": (255, 255, 255),
            "button": (100, 100, 100)
        }
        
        self.fish_image = pygame.image.load("fish.png")
        self.minigame_background = pygame.image.load("minigame.png") # minigame background
        self.fish_rect = self.fish_image.get_rect()

        self.game_active = False
        self.running = True
        self.game_lost = False
        self.clock = pygame.time.Clock()

        # Fish velocity
        self.fish_velocity = 0
        
        # Effects
        self.effects_used = 0
        self.MAX_EFFECTS = 2
        self.current_effect_duration = 0
        self.space_pressed = False

        self.score = 0

        
        # Initial positions
        self.play_area_x = (self.fish_game.WINDOW_WIDTH - self.PLAY_AREA_WIDTH) // 2  # Position play area in the center-left
        self.play_area_y = (self.fish_game.WINDOW_HEIGHT - self.PLAY_AREA_HEIGHT) // 2
        self.play_area_x = self.play_area_x -100
        self.play_area_y = self.play_area_y
        self.rect_height = random.randint(90, 120)  # Randomized height for the rectangle
        self.rect_y = self.play_area_y + self.PLAY_AREA_HEIGHT - self.rect_height  # Align rectangle to the bottom of the play area
        self.fish_rect.center = (self.play_area_x + self.PLAY_AREA_WIDTH // 2, self.rect_y + self.rect_height // 2)  # Fish centered in the rectangle
        self.movement_mode = "slow_up"  # Default movement mode


    def reset_game(self):
        self.play_area_x = (self.fish_game.WINDOW_WIDTH - self.PLAY_AREA_WIDTH) // 2
        self.play_area_y = (self.fish_game.WINDOW_HEIGHT - self.PLAY_AREA_HEIGHT) // 2
        self.play_area_x = self.play_area_x - 225
        self.play_area_y = self.play_area_y
        self.rect_height = random.randint(90, 120)
        self.rect_y = self.play_area_y + self.PLAY_AREA_HEIGHT - self.rect_height
        self.fish_rect.center = (self.play_area_x + self.PLAY_AREA_WIDTH // 2, self.rect_y + self.rect_height // 2)
        self.movement_mode = "slow_up"
        self.fish_velocity = 0
        self.effects_used = 0
        self.current_effect_duration = 0
        self.game_active = False
        self.space_pressed = False
        self.running = False


    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_active:
                        self.space_pressed = True

    def update_game(self):
        if self.game_active:
            # Fish controls
            if self.space_pressed:
                self.fish_velocity = self.FISH_JUMP_FORCE
                self.space_pressed = False  # Reset after jump

            # Apply gravity to the fish
            self.fish_velocity += self.FISH_GRAVITY
            self.fish_velocity = min(self.fish_velocity, self.MAX_FALL_SPEED)  # Limit falling speed
            self.fish_rect.y += self.fish_velocity

            # Check if the fish is outside the play area
            if not self.fish_rect.colliderect(pygame.Rect(self.play_area_x, self.play_area_y, self.PLAY_AREA_WIDTH, self.PLAY_AREA_HEIGHT)) \
                or not self.fish_rect.colliderect(pygame.Rect(self.play_area_x, self.rect_y, self.PLAY_AREA_WIDTH, self.rect_height)):
                self.game_active = False  # End game
                self.reset_game()

            # Update rectangle movement based on the mode
            if self.current_effect_duration <= 0: 
                if self.effects_used < self.MAX_EFFECTS and random.random() < 0.005:
                    self.movement_mode = random.choice(["fast_up", "slow_down", "stopped"])
                    self.effects_used += 1

                    # Set effect duration
                    self.current_effect_duration = random.randint(60, 240)  # 1 to 4 seconds
                else:
                    self.movement_mode = "slow_up"  # Default green mode after effects

            else:
                self.current_effect_duration -= 1

            if self.movement_mode == "slow_up":
                self.rect_y -= self.SLOW_UP_SPEED
            elif self.movement_mode == "fast_up":
                self.rect_y -= self.FAST_UP_SPEED
            elif self.movement_mode == "slow_down":
                self.rect_y += self.SLOW_UP_SPEED

            # Ensure rectangle stays within bounds
            if self.rect_y < self.play_area_y:
                self.rect_y = self.play_area_y
                self.movement_mode = "stopped"
            if self.rect_y + self.rect_height > self.play_area_y + self.PLAY_AREA_HEIGHT:
                self.rect_y = self.play_area_y + self.PLAY_AREA_HEIGHT - self.rect_height
                self.movement_mode = "stopped"

            # Check for scoring
            if self.fish_rect.colliderect(pygame.Rect(self.play_area_x, self.rect_y, self.PLAY_AREA_WIDTH, self.rect_height)):
                if self.rect_y <= self.play_area_y:
                    self.score += 1
                    self.reset_game()
                    print("Score:", self.score)

        elif not self.game_active:
            if self.game_lost:
                print("Fish escaped")
                time.sleep(1)
                print("Resetting game")
                self.reset_game()


    def draw_ui(self):
        pass

    def draw_game(self):
        self.screen.blit(self.fish_game.background_image, self.fish_game.background_rect)   
        self.screen.blit(self.minigame_background, (50, 50))
        pygame.draw.rect(self.screen, WHITE, (self.play_area_x - 2, self.play_area_y - 2, self.PLAY_AREA_WIDTH + 4, self.PLAY_AREA_HEIGHT + 4), 2)  # Play area outline

        if not self.game_active and self.running:
            self.countdown()
            self.game_active = True
        elif self.game_active:
            # Draw rectangle and effects
            if self.movement_mode == "slow_up":
                pygame.draw.rect(self.screen, self.COLORS["slow_up"], (self.play_area_x, self.rect_y, self.PLAY_AREA_WIDTH, self.rect_height))
            elif self.movement_mode == "fast_up":
                pygame.draw.rect(self.screen, self.COLORS["fast_up"], (self.play_area_x, self.rect_y, self.PLAY_AREA_WIDTH, self.rect_height))
            elif self.movement_mode == "slow_down":
                pygame.draw.rect(self.screen, self.COLORS["slow_down"], (self.play_area_x, self.rect_y, self.PLAY_AREA_WIDTH, self.rect_height))
            elif self.movement_mode == "stopped":
                pygame.draw.rect(self.screen, self.COLORS["stopped"], (self.play_area_x, self.rect_y, self.PLAY_AREA_WIDTH, self.rect_height))

            self.screen.blit(self.fish_image, self.fish_rect)



    def run(self):
        self.reset_game()
        self.running = True
        while self.running:
            self.handle_events()
            self.update_game()
            self.draw_game()
            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(FPS)
        
        if not self.running:
            return True

    def countdown(self):
        for i in range(3, 0, -1):
            self.screen.blit(self.fish_game.background_image, self.fish_game.background_rect)   
            self.screen.blit(self.minigame_background, (50, 50))
            pygame.draw.rect(self.screen, self.COLORS["slow_up"], (self.play_area_x, self.rect_y, self.PLAY_AREA_WIDTH, self.rect_height))
            pygame.draw.rect(self.screen, self.COLORS["text"], (self.play_area_x - 2, self.play_area_y - 2, self.PLAY_AREA_WIDTH + 4, self.PLAY_AREA_HEIGHT + 4), 2)
            self.screen.blit(self.fish_image, self.fish_rect)
            countdown_text = self.fish_game.font.render(str(i), True, self.COLORS["text"])
            self.screen.blit(countdown_text, (self.fish_game.WINDOW_WIDTH // 2 - countdown_text.get_width() // 2, self.fish_game.WINDOW_HEIGHT // 2))
            pygame.display.flip()
            time.sleep(1)
        pygame.draw.rect(self.screen, self.COLORS["slow_up"], (self.play_area_x, self.rect_y, self.PLAY_AREA_WIDTH, self.rect_height))
        pygame.draw.rect(self.screen, WHITE, (self.play_area_x - 2, self.play_area_y - 2, self.PLAY_AREA_WIDTH + 4, self.PLAY_AREA_HEIGHT + 4), 2)  # Play area outline
        self.screen.blit(self.fish_image, self.fish_rect)
        pygame.display.flip()
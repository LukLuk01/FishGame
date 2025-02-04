import pygame
import random
import time

from miniGame import FishMiniGame
# Initialize Pygame
pygame.init()

# Constants
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Classes
class FishGame:
    def __init__(self, background_image_path):
        # Load background image and set window size based on it
        self.background_image = pygame.image.load(background_image_path)
        self.background_rect = self.background_image.get_rect()
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = self.background_rect.size

        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Fishing Game")
        self.clock = pygame.time.Clock()
        # Load images
        self.bite_image = pygame.image.load("bite.png")
        self.bite_image = pygame.transform.scale(self.bite_image, (70, 70))  # Scale the bite icon
        self.bite_rect = self.bite_image.get_rect()

        # Define fixed position for the bite icon (top-right corner)
        self.bite_fixed_position = (self.WINDOW_WIDTH - 70, 20)  # Slight padding from edges

        # Game state
        #---------------------------------
        self.running = True
        self.game_active = False
        #---------------------------------
        self.bait_attached = False
        self.bait_thrown = False
        self.fish_biting_icone = False
        self.catch_allowed = False  # Allow catching only after bite icon disappears
        self.catch_attempt = False
        self.minigame = False # Mini game state
        self.fish_caught = False
        self.missed_catch = False  # Track if fish escaped
        self.draw_bite = False

        # Timing
        self.bite_icon_duration = 3000  # Bite icon appears for 3 seconds (in milliseconds)
        self.catch_window_duration = 3000  # Time allowed to catch after bite icon disappears (in milliseconds)
        self.bite_wait_time = random.randint(2000, 4000)  # Random wait time for bite (in milliseconds)
        self.fish_bite_start = 0
        self.catch_window_start = 0

        # Font
        self.font = pygame.font.Font(None, 36)

        #minigame
        self.fishMiniGame = FishMiniGame(self,self.screen)
        

    def reset_game(self):
        self.bait_attached = False
        self.bait_thrown = False
        self.fish_biting = False
        self.catch_allowed = False
        self.catch_attempt = False
        self.fish_caught = False
        self.missed_catch = False
        self.bite_wait_time = random.randint(2000, 4000)
        self.fish_bite_start = 0
        self.catch_window_start = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if not self.bait_attached and not self.bait_thrown:
                        self.bait_attached = True
                if event.key == pygame.K_SPACE:
                    if self.bait_attached and not self.bait_thrown:
                        self.bait_thrown = True
                        self.fish_bite_start = pygame.time.get_ticks() + self.bite_wait_time  # Schedule bite start
                    elif self.catch_allowed:
                        self.catch_attempt = True
         
    def update_game(self):
        current_time = pygame.time.get_ticks()

        if self.missed_catch:
            print("Fish escaped")
            time.sleep(1)
            print("Resetting game")
            self.reset_game()

        if self.bait_attached and self.bait_thrown:
            if current_time >= self.fish_bite_start:

                self.bait_attached = False
                self.fish_biting_icone = True

                self.fish_bite_start = current_time  # Start bite timer

        if self.fish_biting_icone: 
            if current_time - self.fish_bite_start > self.bite_icon_duration:

                self.fish_biting_icone = False
                self.catch_allowed = True

                self.catch_window_start = current_time  # Start catch window timer

        if self.catch_allowed:
            if current_time - self.catch_window_start > self.catch_window_duration:
                self.missed_catch = True

        if self.catch_allowed and self.catch_attempt:
            print("Try to catch fish")
            self.catch_attempt = False
            self.catch_allowed = False
            if random.random() < 1:  # 70% chance to catch the fish
                print("Fish mingame started")
                self.fishMiniGame.run()
                self.reset_game()
            else:
                self.missed_catch = True

    def draw_ui(self):
        if not self.bait_attached and not self.bait_thrown:
            bait_text = self.font.render("Press 1 to attach bait", True, WHITE)
            self.screen.blit(bait_text, (10, 10))
        elif not self.bait_thrown:
            throw_text = self.font.render("Press SPACE to throw bait", True, WHITE)
            self.screen.blit(throw_text, (10, 10))
        elif self.bait_thrown and self.bait_attached:
            wait_text = self.font.render("Waiting for a fish...", True, WHITE)
            self.screen.blit(wait_text, (10, 10))
        elif self.fish_biting_icone:
            bite_text = self.font.render("Fish on hook !", True, WHITE)
            self.screen.blit(bite_text, (10, 10))
        elif self.catch_allowed:
            bite_text = self.font.render("Press space", True, WHITE)
            self.screen.blit(bite_text, (10, 10))
        elif self.missed_catch:
            missed_text = self.font.render("The fish escaped!", True, WHITE)
            self.screen.blit(missed_text, (10, 10))

        if self.fish_caught:
            caught_text = self.font.render("You caught a fish!", True, WHITE)
            self.screen.blit(caught_text, (10, 50))

    def draw_game(self):
        self.screen.blit(self.background_image, self.background_rect)
        if self.fish_biting_icone:
            self.bite_rect.topleft = self.bite_fixed_position
            self.screen.blit(self.bite_image, self.bite_rect)

    def run(self):
        while self.running:
            self.handle_events()
            self.update_game()
            self.screen.fill(BLACK)
            self.draw_game()
            self.draw_ui()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

# Main
if __name__ == "__main__":
    game = FishGame("background.png")
    game.run()

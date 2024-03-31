import pygame
import sys
import random
import time
from pygame.locals import *

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Define colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Define screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Initial speed and scores
SPEED = 3
COIN_SCORE = 0
PASSED_SCORE = 0

# Load font
font_small = pygame.font.SysFont("Verdana", 20)

# Create "Game Over" text
game_over = font_small.render("Game Over", True, BLACK)

# Adjusting the position of "Game Over" text
game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Load background image and set up display
background = pygame.image.load("lab8/imgsnd/AnimatedStreet.png")
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer")

# Load background music and play it
pygame.mixer.music.load("lab8/imgsnd/background.wav")
pygame.mixer.music.play(-1)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lab8/imgsnd/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global PASSED_SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            PASSED_SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lab8/imgsnd/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# Create player and enemy sprites
P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Define an event for increasing speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Load sounds
coinsound = pygame.mixer.Sound("lab8/imgsnd/coinsound.mp3")
crashsound = pygame.mixer.Sound("lab8/imgsnd/crash.wav")

# List to hold positions of coins
coins = []

# Generate coins on the road
def generate_coins():
    while len(coins) < 5:
        coin_x = random.randint(40, SCREEN_WIDTH - 40)
        coin_y = random.randint(-1000, -40)
        coins.append((coin_x, coin_y))

generate_coins()

# Main game loop
while True:

    # Event handling
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
            for i in range(len(coins)):
                coins[i] = (coins[i][0], coins[i][1] + SPEED * 10)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Blit background image
    DISPLAYSURF.blit(background, (0, 0))

    # Render and blit scores
    coin_scores = font_small.render("Coins: " + str(COIN_SCORE), True, BLACK)
    passed_scores = font_small.render("Score: " + str(PASSED_SCORE), True, BLACK)
    DISPLAYSURF.blit(coin_scores, (10, 10))
    DISPLAYSURF.blit(passed_scores, (10, 30))

    # Move sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Check collisions between player and enemies
    if pygame.sprite.spritecollideany(P1, enemies):
        crashsound.play()
        time.sleep(1)

        # Show "Game Over" text
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, game_over_rect)
        pygame.display.update()

        # Remove all sprites and quit the game
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Check collisions between player and coins
    for coin in coins[:]:
        coin_rect = pygame.Rect(coin[0], coin[1], 32, 32)
        if P1.rect.colliderect(coin_rect):
            coinsound.play()
            coins.remove(coin)
            COIN_SCORE += 1

    # Remove coins that have gone off the screen and generate new ones
    for coin in coins:
        if coin[1] > SCREEN_HEIGHT:
            coins.remove(coin)
    generate_coins()

    # Draw coins on the road
    for coin in coins:
        pygame.draw.circle(DISPLAYSURF, YELLOW, coin, 10)

    # Update display and maintain FPS
    pygame.display.update()
    FramePerSec.tick(FPS)

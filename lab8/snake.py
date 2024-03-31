import pygame
import time
import random
import sys

# Initialize Pygame
pygame.init()

# Define colors
yellow = (255, 255, 102)
black = (0, 0, 0)
green = (0, 255, 0)
dark_purple = (75, 0, 130)  

# Define display dimensions
dis_width = 800
dis_height = 600

# Set up display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake')

# Set up clock
clock = pygame.time.Clock()

# Define block size and snake speed
snake_block = 10
snake_speed = 15

# Define font
font = pygame.font.SysFont(None, 40)  # Using default system font

# Function to display score
def Your_score(score):
    value = font.render("Score: " + str(score), True, yellow)
    dis.blit(value, [10, 10])

# Function to draw snake
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

# Main game loop
def gameLoop():
    # Initialize game variables
    game_over = False
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    score = 0

    # Main game loop
    while not game_over:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Move snake
        x1 += x1_change
        y1 += y1_change
        dis.fill(dark_purple)  # Fill display with background color

        # Draw food
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        # Update snake list
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check for collision with self
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_over = True

        # Draw snake
        our_snake(snake_block, snake_List)

        # Display score
        Your_score(score)

        # Check for food consumption
        if x1 == foodx and y1 == foody:
            score += 1
            Length_of_snake += 1
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        # Update display
        pygame.display.update()

        # Set game speed
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game loop
gameLoop()

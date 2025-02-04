import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

def display_message(text, color, y_offset=0):
    font = pygame.font.Font(None, 36)
    message = font.render(text, True, color)
    message_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(message, message_rect)

def game_loop():
    # Snake and food setup
    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = (CELL_SIZE, 0)
    food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
            random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
    game_over = False

    # Reduce delay for key press response
    pygame.key.set_repeat(1, 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True

        if not game_over:
            # Control the snake with W/A/S/D keys
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)  # Move up
            elif keys[pygame.K_s] and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)  # Move down
            elif keys[pygame.K_a] and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)  # Move left
            elif keys[pygame.K_d] and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)  # Move right

            # Move the snake
            head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            if head in snake or head[0] < 0 or head[1] < 0 or head[0] >= WIDTH or head[1] >= HEIGHT:
                game_over = True
            else:
                snake.insert(0, head)
                if head == food:
                    food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                            random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
                else:
                    snake.pop()

        # Draw everything
        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

        if game_over:
            display_message("Game Over! Press SPACE to restart.", WHITE)

        pygame.display.flip()
        clock.tick(3)

while True:
    if not game_loop():
        break

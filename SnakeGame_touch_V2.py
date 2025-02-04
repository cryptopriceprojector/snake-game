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
GRAY = (128, 128, 128)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

def draw_button(rect, text):
    pygame.draw.rect(screen, GRAY, rect)
    font = pygame.font.Font(None, 36)
    label = font.render(text, True, WHITE)
    label_rect = label.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
    screen.blit(label, label_rect)

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
    score = 0  # Score starts at 0

    # Button dimensions
    button_size = 60
    up_button = pygame.Rect((WIDTH // 2 - button_size // 2, HEIGHT - 150, button_size, button_size))
    left_button = pygame.Rect((WIDTH // 2 - button_size - 10, HEIGHT - 80, button_size, button_size))
    right_button = pygame.Rect((WIDTH // 2 + 10, HEIGHT - 80, button_size, button_size))
    down_button = pygame.Rect((WIDTH // 2 - button_size // 2, HEIGHT - 80, button_size, button_size))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if up_button.collidepoint(mouse_pos) and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)  # Move up
                elif down_button.collidepoint(mouse_pos) and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)  # Move down
                elif left_button.collidepoint(mouse_pos) and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)  # Move left
                elif right_button.collidepoint(mouse_pos) and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)  # Move right

        if not game_over:
            # Move the snake
            head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            if head in snake or head[0] < 0 or head[1] < 0 or head[0] >= WIDTH or head[1] >= HEIGHT:
                game_over = True
            else:
                snake.insert(0, head)
                if head == food:
                    food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                            random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
                    score += 1  # Increase score when food is eaten
                else:
                    snake.pop()

        # Draw everything
        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

        # Draw buttons
        draw_button(up_button, "↑")
        draw_button(left_button, "←")
        draw_button(right_button, "→")
        draw_button(down_button, "↓")

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            display_message(f"Game Over! Final Score: {score}", WHITE)
            display_message("Tap to restart.", WHITE, 40)

        pygame.display.flip()

        # **Dynamic Speed Increase**
        speed = 3 + (score // 3)  # Increase speed every 3 points
        clock.tick(speed)  # Adjust speed dynamically

while True:
    if not game_loop():
        break

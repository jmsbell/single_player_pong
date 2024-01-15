import pygame
import sys
import random

pygame.init()

# Set up game window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Breakout Game")

black = (0, 0, 0)
white = (255, 255, 255)

# Paddle
paddle_width, paddle_height = 100, 10
paddle_x, paddle_y = (width - paddle_width) // 2, height - 20
paddle_speed = 6

# Ball
ball_radius = 10
ball_x, ball_y = width // 20 - 20, height // 2  # Start slightly to the left
ball_speed_x, ball_speed_y = 0, 0  # Initialize ball speed

# Counter
hit_counter = 0

# Blocks
block_size = 5
blocks = []

# Game state
game_active = False

# Main game loop
clock = pygame.time.Clock()

def generate_block():
    block_x = random.randint(0, width - block_size)
    block_y = random.randint(0, height - block_size)
    return pygame.Rect(block_x, block_y, block_size, block_size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Start/restart the game on space bar press
                game_active = True
                ball_x, ball_y = width // 20 - 20, height // 2  # Reset ball position
                ball_speed_x, ball_speed_y = 5, 5  # Set initial ball speed

    if game_active:
        # Move the paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < width - paddle_width:
            paddle_x += paddle_speed

        # Move the ball
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Bounce off walls
        if ball_x <= 0 or ball_x >= width:
            ball_speed_x = -ball_speed_x
        if ball_y <= 0:
            ball_speed_y = -ball_speed_y

        # Reset game if the ball misses the paddle
        if ball_y >= height:
            game_active = False
            ball_x, ball_y = width // 20 - 20, height // 2  # Reset ball position
            ball_speed_x, ball_speed_y = 0, 0
            hit_counter = 0
            blocks = []  # Clear blocks on game over

        # Check collision with paddle
        if (
            paddle_x <= ball_x <= paddle_x + paddle_width
            and paddle_y <= ball_y <= paddle_y + paddle_height
            and ball_speed_y > 0  # Only count hits when the ball is moving downward
        ):
            hit_counter += 1

            # Generate a new block
            blocks.append(generate_block())

            # Increase ball speed slightly on each hit
            ball_speed_y = -ball_speed_y
            if ball_speed_x < 0:
                ball_speed_x -= 0.5
            else:
                ball_speed_x += 0.5

        # Check if the ball hits a block
        hit_block = None
        for block in blocks:
            if block.colliderect((ball_x - ball_radius, ball_y - ball_radius, 2 * ball_radius, 2 * ball_radius)):
                hit_block = block
                break

        if hit_block:
            # Bounce off the block
            ball_speed_y = -ball_speed_y
            blocks.remove(hit_block)

        # Draw everything
        screen.fill(white)  # Set background color to white

        pygame.draw.rect(screen, black, (paddle_x, paddle_y, paddle_width, paddle_height))
        pygame.draw.circle(screen, black, (int(ball_x), int(ball_y)), ball_radius)

        # Draw blocks
        for block in blocks:
            pygame.draw.rect(screen, black, block)

        # Display hit counter
        font = pygame.font.Font(None, 36)
        text = font.render(f"Hits: {hit_counter}", True, black)
        screen.blit(text, (10, 10))

    else:
        # Display "Press Space Bar to Start" message
        screen.fill(white)  # Set background color to white
        font = pygame.font.Font(None, 36)
        text = font.render("Press Space Bar to Start", True, black)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second

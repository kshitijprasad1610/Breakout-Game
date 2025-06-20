import pygame
import random

# Initialize pygame
pygame.init()

# Get the screen resolution of the current laptop
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

# Set up the screen to run in fullscreen mode
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Breakout Game")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Ball properties
ball_radius = 15
ball_speed_x = 5 * random.choice([1, -1])  # Random direction
ball_speed_y = -5

# Paddle properties
paddle_width = screen_width // 8
paddle_height = screen_height // 40
paddle_speed = screen_width // 80

# Block properties
block_spacing = 5  # Space between blocks
rows = 5
col=5
block_width = (screen_width - (block_spacing * (rows + 1))) // rows  # Adjust block width dynamically
block_height = screen_height // 30
blocks = []

# Load textures
brick_texture = pygame.image.load("brick_texture.png")  # Replace with your brick texture file
brick_texture = pygame.transform.scale(brick_texture, (block_width, block_height))
try:
    ball_texture = pygame.image.load("ball.png")  # Replace with your ball texture file
    ball_texture = pygame.transform.scale(ball_texture, (ball_radius * 2, ball_radius * 2))
except pygame.error:
    ball_texture = None 

# Setup font for scoring
font = pygame.font.Font(None, 36)

# Create blocks
for i in range(rows):
    for j in range(col):
        blocks.append(pygame.Rect(j * (block_width + block_spacing), i * (block_height + block_spacing), block_width, block_height))

# Define the paddle and ball objects
paddle = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - paddle_height - 10, paddle_width, paddle_height)
ball = pygame.Rect(screen_width // 2 - ball_radius, screen_height - paddle_height - ball_radius - 20, ball_radius * 2, ball_radius * 2)

# Game variables
score = 0
lives = 3
running = True

# Clock for frame rate control
clock = pygame.time.Clock()

# Game loop
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Move paddle
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < screen_width:
        paddle.x += paddle_speed

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with walls
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y = -ball_speed_y
    if ball.bottom >= screen_height:
        lives -= 1
        ball = pygame.Rect(screen_width // 2 - ball_radius, screen_height - paddle_height - ball_radius - 20, ball_radius * 2, ball_radius * 2)
        ball_speed_x = 5 * random.choice([1, -1])
        ball_speed_y = -5
        pygame.time.wait(1000)  # Pause after losing a life
        if lives == 0:
            screen.fill(BLACK)
            game_over_text = font.render("Game Over!", True, WHITE)
            screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2))
            pygame.display.update()
            pygame.time.wait(3000)
            running = False

    # Ball collision with paddle
    if ball.colliderect(paddle):
        ball_speed_y = -ball_speed_y
        offset = max(-1, min(1, (ball.centerx - paddle.centerx) / (paddle.width / 2)))
        ball_speed_x = 5 * offset

    # Ball collision with blocks
    for block in blocks[:]:
        if ball.colliderect(block):
            blocks.remove(block)
            ball_speed_y = -ball_speed_y
            score += 10

    # Draw blocks
    for block in blocks:
        screen.blit(brick_texture, block)

    # Draw paddle and ball
    screen.blit(ball_texture, ball)
    pygame.draw.rect(screen, BLUE, paddle)

    # Display score and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (screen_width - lives_text.get_width() - 10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
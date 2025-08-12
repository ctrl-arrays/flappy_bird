import pygame
import sys
import random

pygame.init() # Initialize all pygame modules

# Window size
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

CLOCK = pygame.time.Clock()
FPS = 60

# Load images from file
background_img = pygame.image.load('background.png').convert()
# Convert () optimizes image for faster blitting (no alpha chaneel)

bird_img = pygame.image.load('bird.png').convert_alpha()
# Convert_alpha() preserves transparency

pipe_img = pygame.image.load('pipe.png').convert_alpha()

# Scale images to fit game. Optional adjust size here
BIRD_WIDTH, BIRD_HEIGHT = 40, 30
PIPE_WIDTH = 70
PIPE_GAP = 150

bird_img = pygame.transform.scale(bird_img, (BIRD_WIDTH, BIRD_HEIGHT))
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, pipe_img.get_height()))

# Bird position and physics
bird_x = 50 # Birds horizontal position fixed
bird_y = HEIGHT // 2 # Start vertically centered
bird_velocity = 0
gravity = 0.5
jump_strength = -7

# Pipes list hold dictionaries with 'x' and 'top_height'
pipes = []
pipe_speed = 3
pipe_frequency = 1500 # milliseconds

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, pipe_frequency)

game_over = False

def draw_bird(x, y):
    """Draw the bird image at the current position"""
    SCREEN.blit(bird_img, (x, y))

def draw_pipes(pipes):
    """Draw pipes using the pipe image. Bottom pipe is normal, top pipe is flipped vertically"""
    for pipe in pipes:
        # Bottom pipe position
        bottom_y = pipe['top_height'] + PIPE_GAP
        SCREEN.blit(pipe_img, (pipe['x'], bottom_y))

        # Flip pipe image verticaly for top pipe
        flipped_pipe = pygame.transform.flip(pipe_img, False, True)
        # Draw pipe so bottom aligns with pipe['top_height']
        top_y = pipe['top_height'] - pipe_img.get_height()
        SCREEN.blit(flipped_pipe, (pipe['x'], top_y))

def check_collision(bird_rect, pipes):
    """Check if bird collides with any pipe or screen edges"""
    for pipe in pipes:
        # Top pipe rectangle for collision
        top_pipe_rect = pygame.Rect(pipe['x'], 0, PIPE_WIDTH, pipe['top_height'])
        # Bottom pipe rectangle for collision
        bottom_pipe_rect = pygame.Rect(pipe['x'], pipe['top_height'] + PIPE_GAP, PIPE_WIDTH, HEIGHT)
        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            return True
        
    # Check collision with top and bottom edged of screen 
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return True
    
    return False

def display_text(text, font, color, x, y):
    """Helper function to display centered text at x, y"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    SCREEN.blit(text_surface, text_rect)

def run_game():
    global bird_y, bird_velocity, game_over, pipes

    bird_y = HEIGHT // 2 # Reset bird position
    bird_velocity = 0 # Reset velocity
    pipes = [] # Clear existing pipes
    game_over = False # Reset game over
    score = 0 # Reset score
    passed_pipes = [] # Track pipes already passed for scoring

    waiting_to_start = True # Track players

    FONT = pygame.font.SysFont('Arial', 40)
    SMALL_FONT = pygame.font.SysFont('Arial', 25)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == SPAWNPIPE and not game_over and not waiting_to_start:
                top_pipe_height = random.randint(50, HEIGHT - PIPE_GAP - 50)
                pipes.append({'x': WIDTH, 'top_height': top_pipe_height})

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if waiting_to_start:
                        waiting_to_start = False # Start game on space press
                    elif not game_over:
                        bird_velocity = jump_strength # Make bird jump
                    else:
                        return  # Restart the game

        if not game_over and not waiting_to_start:
            bird_velocity += gravity # Apply gravity
            bird_y += bird_velocity # Update bird position

            if bird_y + BIRD_HEIGHT >= HEIGHT:
                game_over = True # Bird hit bottom

            for pipe in pipes:
                pipe['x'] -= pipe_speed # Move pipes left

            pipes = [pipe for pipe in pipes if pipe['x'] + PIPE_WIDTH > 0]

            bird_rect = pygame.Rect(bird_x, int(bird_y), BIRD_WIDTH, BIRD_HEIGHT)

            if check_collision(bird_rect, pipes):
                game_over = True

            for pipe in pipes:
                if pipe['x'] + PIPE_WIDTH < bird_x and pipe not in passed_pipes:
                    score += 1
                    passed_pipes.append(pipe)

        # Draw everything
        SCREEN.blit(background_img, (0, 0))
        draw_bird(bird_x, int(bird_y))
        draw_pipes(pipes)
        display_text(f"Score: {score}", SMALL_FONT, (0, 0, 0), WIDTH // 2, 30)

        if waiting_to_start:
            display_text("Press SPACE to Start", FONT, (0, 0, 255), WIDTH // 2, HEIGHT // 2)

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((50, 50, 50))
            SCREEN.blit(overlay, (0, 0))
            display_text("GAME OVER", FONT, (255, 0, 0), WIDTH // 2, HEIGHT // 2 - 30)
            display_text("Press SPACE to Restart", SMALL_FONT, (255, 255, 255), WIDTH // 2, HEIGHT // 2 + 30)

        # Always update display and tick clock
        pygame.display.update()
        CLOCK.tick(FPS)

if __name__ == "__main__":
    while True:
        run_game() 

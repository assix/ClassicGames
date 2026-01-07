import pygame
import random
import sys

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_RADIUS = 10
BRICK_WIDTH = 80  # Slightly wider since we have fewer columns
BRICK_HEIGHT = 30
# Reduced bricks for a shorter game
BRICK_ROWS = 3    
BRICK_COLS = 8    
GAP = 10
FPS = 60

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(
            (SCREEN_WIDTH // 2) - (PADDLE_WIDTH // 2),
            SCREEN_HEIGHT - 50,
            PADDLE_WIDTH,
            PADDLE_HEIGHT
        )
        self.speed = 9

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(
            SCREEN_WIDTH // 2 - BALL_RADIUS,
            SCREEN_HEIGHT // 2,
            BALL_RADIUS * 2,
            BALL_RADIUS * 2
        )
        # Drop vertically initially
        self.dx = 0
        self.dy = 5
        self.active = False 

    def move(self):
        if self.active:
            self.rect.x += self.dx
            self.rect.y += self.dy

            # Wall Collisions
            if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
                self.dx *= -1
            if self.rect.top <= 0:
                self.dy *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, self.rect.center, BALL_RADIUS)

class Brick:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

def create_bricks(layout_style='standard'):
    bricks = []
    colors = [RED, ORANGE, GREEN, YELLOW, CYAN]
    
    total_bricks_width = BRICK_COLS * (BRICK_WIDTH + GAP) - GAP
    start_x = (SCREEN_WIDTH - total_bricks_width) // 2
    
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            # Logic for different layouts
            if layout_style == 'random_gaps':
                if random.random() < 0.3: # 30% chance to skip a brick
                    continue
            elif layout_style == 'pyramid':
                # Skip bricks to form a rough pyramid shape
                if col < row or col >= (BRICK_COLS - row):
                    continue

            x = start_x + col * (BRICK_WIDTH + GAP)
            y = 60 + row * (BRICK_HEIGHT + GAP)
            
            # Random color or row-based color
            color = random.choice(colors) if layout_style == 'random_colors' else colors[row % len(colors)]
            
            brick = Brick(x, y, color)
            bricks.append(brick)
    
    # Fallback if random generation made 0 bricks
    if not bricks:
        return create_bricks('standard')
        
    return bricks

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Brick Breaker - Pause & Layouts")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks('standard')
    lives = 5

    game_over = False
    won = False
    paused = False

    while True:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                # SPACE HANDLER (Launch or Pause)
                if event.key == pygame.K_SPACE:
                    if not game_over:
                        if not ball.active:
                            ball.active = True # Launch
                        else:
                            paused = not paused # Toggle Pause

                # 'R' HANDLER (Reset or Change Layout)
                if event.key == pygame.K_r:
                    if game_over:
                        # Full Reset after game over
                        lives = 5
                        bricks = create_bricks('standard')
                        ball.reset()
                        game_over = False
                        won = False
                        paused = False
                    elif not ball.active:
                        # Randomize layout only before launching
                        modes = ['standard', 'random_gaps', 'pyramid', 'random_colors']
                        current_mode = random.choice(modes)
                        bricks = create_bricks(current_mode)

        # 2. Logic Updates (Only if not paused and not game over)
        if not paused and not game_over:
            paddle.move()
            ball.move()

            # Paddle Collision
            if ball.rect.colliderect(paddle.rect) and ball.dy > 0:
                ball.dy *= -1
                # Add horizontal angle based on where it hits the paddle
                offset = (ball.rect.centerx - paddle.rect.centerx) / (PADDLE_WIDTH / 2)
                ball.dx = offset * 6  # Multiplier determines how sharp the angle is

            # Brick Collision
            hit_index = ball.rect.collidelist([brick.rect for brick in bricks])
            if hit_index != -1:
                hit_brick = bricks.pop(hit_index)
                ball.dy *= -1
            
            # Win Check
            if len(bricks) == 0:
                game_over = True
                won = True

            # Lose Life Check
            if ball.rect.top > SCREEN_HEIGHT:
                lives -= 1
                if lives > 0:
                    ball.reset()
                    paused = False # Optional: Auto-pause after death? Currently keeps going but ball inactive.
                else:
                    game_over = True
                    won = False

        # 3. Drawing
        screen.fill(BLACK)
        
        paddle.draw(screen)
        ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)

        # UI Text
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (10, 10))

        # Context-sensitive Messages
        if game_over:
            if won:
                msg = font.render("YOU WIN! Press R to Restart", True, GREEN)
            else:
                msg = font.render("GAME OVER! Press R to Restart", True, RED)
            screen.blit(msg, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2))
        
        elif paused and ball.active:
            msg = font.render("PAUSED - Press SPACE", True, YELLOW)
            screen.blit(msg, (SCREEN_WIDTH//2 - 130, SCREEN_HEIGHT//2))
            
        elif not ball.active:
            msg = font.render("Press SPACE to Drop Ball", True, WHITE)
            sub_msg = small_font.render("Press 'R' to randomize Layout", True, (200, 200, 200))
            screen.blit(msg, (SCREEN_WIDTH//2 - 140, SCREEN_HEIGHT//2 + 40))
            screen.blit(sub_msg, (SCREEN_WIDTH//2 - 110, SCREEN_HEIGHT//2 + 70))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

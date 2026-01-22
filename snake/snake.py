import pygame
import sys
import random
import os

# --- CONFIGURATION ---
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 40
COLS, ROWS = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
FPS = 10

# COLORS
BG_COLOR = (10, 10, 15)
SNAKE_COLOR = (0, 255, 100)
FOOD_COLOR = (255, 50, 100)
TEXT_COL = (255, 255, 255)
GRID_COL = (20, 20, 30)

# HIGH SCORE FILE
SCORE_FILE = "snake_highscore.txt"

# --- PIXEL FONT ENGINE ---
PIXEL_FONT = {
    '0': [0x70, 0x88, 0x98, 0xA8, 0xC8, 0x88, 0x70],
    '1': [0x20, 0x60, 0x20, 0x20, 0x20, 0x20, 0x70],
    '2': [0x70, 0x88, 0x08, 0x30, 0x40, 0x80, 0xF8],
    '3': [0xF8, 0x08, 0x10, 0x30, 0x08, 0x88, 0x70],
    '4': [0x10, 0x30, 0x50, 0x90, 0xF8, 0x10, 0x10],
    '5': [0xF8, 0x80, 0xF0, 0x08, 0x08, 0x88, 0x70],
    '6': [0x30, 0x40, 0x80, 0xF0, 0x88, 0x88, 0x70],
    '7': [0xF8, 0x08, 0x10, 0x20, 0x40, 0x40, 0x40],
    '8': [0x70, 0x88, 0x88, 0x70, 0x88, 0x88, 0x70],
    '9': [0x70, 0x88, 0x88, 0x78, 0x08, 0x88, 0x70],
    'G': [0x78, 0x80, 0x80, 0x98, 0x88, 0x88, 0x70],
    'A': [0x70, 0x88, 0x88, 0xF8, 0x88, 0x88, 0x88],
    'M': [0x88, 0xD8, 0xA8, 0xA8, 0x88, 0x88, 0x88],
    'E': [0xF8, 0x80, 0x80, 0xF0, 0x80, 0x80, 0xF8],
    'O': [0x70, 0x88, 0x88, 0x88, 0x88, 0x88, 0x70],
    'V': [0x88, 0x88, 0x88, 0x88, 0x88, 0x50, 0x20],
    'R': [0xF0, 0x88, 0x88, 0xF0, 0xA0, 0x90, 0x88],
    'H': [0x88, 0x88, 0x88, 0xF8, 0x88, 0x88, 0x88],
    'I': [0x70, 0x20, 0x20, 0x20, 0x20, 0x20, 0x70],
    'S': [0x70, 0x88, 0x80, 0x70, 0x08, 0x88, 0x70],
    'C': [0x70, 0x88, 0x80, 0x80, 0x80, 0x88, 0x70],
    ':': [0x00, 0x60, 0x60, 0x00, 0x60, 0x60, 0x00],
    ' ': [0x00] * 7
}

def draw_text(surface, text, x, y, scale=2, color=TEXT_COL, center=False):
    text = str(text).upper()
    width = 0
    for char in text: width += 6 * scale
    start_x = x - width // 2 if center else x
    cursor_x = start_x
    for char in text:
        if char in PIXEL_FONT:
            rows = PIXEL_FONT[char]
            for r, row_val in enumerate(rows):
                for c in range(5):
                    if (row_val >> (7 - c)) & 1:
                        pygame.draw.rect(surface, color, (cursor_x + c * scale, y + r * scale, scale, scale))
        cursor_x += 6 * scale

# --- GAME LOGIC ---
class SnakeGame:
    def __init__(self):
        self.reset()
        self.load_highscore()

    def reset(self):
        self.snake = [(5, 5), (4, 5), (3, 5)] # Head at index 0
        self.direction = (1, 0) # Moving Right
        self.next_direction = (1, 0) # Input buffer
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.paused = False

    def spawn_food(self):
        while True:
            x, y = random.randint(0, COLS-1), random.randint(0, ROWS-1)
            if (x, y) not in self.snake:
                return (x, y)

    def load_highscore(self):
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, 'r') as f:
                try: self.highscore = int(f.read())
                except: self.highscore = 0
        else:
            self.highscore = 0

    def save_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            with open(SCORE_FILE, 'w') as f:
                f.write(str(self.highscore))

    def update(self):
        if self.game_over or self.paused: return

        # Apply buffered direction (prevents 180 suicide turns)
        if (self.next_direction[0] * -1, self.next_direction[1] * -1) != self.direction:
            self.direction = self.next_direction

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Wall Collision (Wrap or Die? Let's Die for Classic feel)
        if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
            self.die()
            return

        # Self Collision
        if new_head in self.snake:
            self.die()
            return

        # Move
        self.snake.insert(0, new_head)
        
        # Eat Food
        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop() # Remove tail

    def die(self):
        self.game_over = True
        self.save_highscore()

# --- GRAPHICS ---
def draw_glow_rect(surface, color, rect, radius=10):
    # Main rect
    pygame.draw.rect(surface, color, rect)
    # Glow (Fake bloom by drawing transparent larger rects)
    s = pygame.Surface((rect.width + radius*2, rect.height + radius*2), pygame.SRCALPHA)
    glow_col = (color[0], color[1], color[2], 50)
    pygame.draw.rect(s, glow_col, (radius, radius, rect.width, rect.height), border_radius=5)
    surface.blit(s, (rect.x - radius, rect.y - radius))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neon Snake")
    clock = pygame.time.Clock()
    
    game = SnakeGame()
    
    while True:
        # Input speed (dash check)
        current_fps = FPS * 2 if pygame.key.get_mods() & pygame.KMOD_SHIFT else FPS
        clock.tick(current_fps)
        
        # --- INPUT ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if game.game_over:
                    if event.key == pygame.K_SPACE: game.reset()
                else:
                    if event.key == pygame.K_UP and game.direction != (0, 1):
                        game.next_direction = (0, -1)
                    elif event.key == pygame.K_DOWN and game.direction != (0, -1):
                        game.next_direction = (0, 1)
                    elif event.key == pygame.K_LEFT and game.direction != (1, 0):
                        game.next_direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and game.direction != (-1, 0):
                        game.next_direction = (1, 0)
                    elif event.key == pygame.K_p:
                        game.paused = not game.paused

        game.update()

        # --- DRAW ---
        screen.fill(BG_COLOR)
        
        # Grid (Subtle)
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, GRID_COL, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, GRID_COL, (0, y), (WIDTH, y))

        # Food (Pulsing)
        pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500 * 5
        food_rect = pygame.Rect(game.food[0]*GRID_SIZE + 2, game.food[1]*GRID_SIZE + 2, GRID_SIZE-4, GRID_SIZE-4)
        draw_glow_rect(screen, FOOD_COLOR, food_rect, int(10+pulse))

        # Snake
        for i, segment in enumerate(game.snake):
            rect = pygame.Rect(segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE)
            # Head is slightly different color
            col = (200, 255, 200) if i == 0 else SNAKE_COLOR
            # Draw slightly smaller to show segments
            inner_rect = rect.inflate(-4, -4)
            pygame.draw.rect(screen, col, inner_rect)

        # UI
        if game.game_over:
            draw_text(screen, "GAME OVER", WIDTH//2, HEIGHT//2 - 50, 5, (255, 0, 0), center=True)
            draw_text(screen, f"SCORE: {game.score}", WIDTH//2, HEIGHT//2 + 30, 3, center=True)
            draw_text(screen, f"HI-SCORE: {game.highscore}", WIDTH//2, HEIGHT//2 + 80, 2, (100, 100, 100), center=True)
            draw_text(screen, "PRESS SPACE", WIDTH//2, HEIGHT//2 + 150, 2, center=True)
        else:
            draw_text(screen, f"{game.score}", WIDTH - 50, 30, 3, (255, 255, 255), center=True)
            if game.paused:
                draw_text(screen, "PAUSED", WIDTH//2, HEIGHT//2, 4, center=True)

        pygame.display.flip()

if __name__ == "__main__":
    main()
import pygame
import random
import copy
import sys

# --- CONFIGURATION ---
# Dimensions
CELL_SIZE = 35
COLS = 10
ROWS = 20
SIDEBAR_WIDTH = 200
WIDTH = COLS * CELL_SIZE + SIDEBAR_WIDTH
HEIGHT = ROWS * CELL_SIZE
FPS = 60

# Colors (Palette chosen for distinct, appealing look)
BG_COLOR = (20, 20, 30)
GRID_COLOR = (40, 40, 50)
SIDEBAR_COLOR = (30, 30, 40)
TEXT_COLOR = (255, 255, 255)

# Tetromino Colors (Standard-ish hues)
COLORS = [
    (0, 0, 0),       # 0: Empty
    (0, 240, 240),   # 1: I (Cyan)
    (0, 0, 240),     # 2: J (Blue)
    (240, 160, 0),   # 3: L (Orange)
    (240, 240, 0),   # 4: O (Yellow)
    (0, 240, 0),     # 5: S (Green)
    (160, 0, 240),   # 6: T (Purple)
    (240, 0, 0)      # 7: Z (Red)
]

# Shapes (defined within 4x4 or 3x3 grids)
SHAPES = [
    [], # 0 placeholder
    [[1, 1, 1, 1]], # I
    [[1, 0, 0], [1, 1, 1]], # J
    [[0, 0, 1], [1, 1, 1]], # L
    [[1, 1], [1, 1]], # O
    [[0, 1, 1], [1, 1, 0]], # S
    [[0, 1, 0], [1, 1, 1]], # T
    [[1, 1, 0], [0, 1, 1]]  # Z
]

# Scoring schemes
SCORES = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}

# --- HIGH QUALITY RENDERING HELPER ---
def draw_block3d(surface, x, y, color_idx, alpha=255, size=CELL_SIZE):
    if color_idx == 0: return
    
    base_color = COLORS[color_idx]
    
    # Create temporary surface for alpha transparency support (used by ghost piece)
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Calculate lighter and darker shades for bevel effect
    light = tuple(min(255, c + 60) for c in base_color)
    dark = tuple(max(0, c - 60) for c in base_color)
    
    # Main body
    pygame.draw.rect(s, (*base_color, alpha), (0, 0, size, size))
    
    # Top and Left highlights (Lighter)
    pygame.draw.polygon(s, (*light, alpha), [(0,0), (size,0), (size-4,4), (4,4), (4,size-4), (0,size)])
    
    # Bottom and Right shadows (Darker)
    pygame.draw.polygon(s, (*dark, alpha), [(size,size), (0,size), (4,size-4), (size-4,size-4), (size-4,4), (size,0)])
    
    # Thin border definition
    pygame.draw.rect(s, (min(255, base_color[0]+30), min(255, base_color[1]+30), min(255, base_color[2]+30), alpha), (0,0,size,size), 1)

    surface.blit(s, (x, y))

# --- GAME CLASSES ---
class Piece:
    def __init__(self, shape_idx):
        self.shape_idx = shape_idx
        # Deepcopy ensures rotation doesn't affect base shape definition
        self.shape = [list(row) for row in SHAPES[shape_idx]]
        self.color = shape_idx # Color index matches shape index
        # Starting position (centered horizontally, top)
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0
        
    def rotate(self):
        # Matrix rotation: zip and reverse
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class TetrisGame:
    def __init__(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        # Drop speeds (ms) per level
        self.drop_speeds = [800, 720, 630, 550, 470, 380, 300, 220, 130, 100, 80]
        self.drop_timer = pygame.time.get_ticks()
        
    def new_piece(self):
        # Choose random shape index (1-7)
        return Piece(random.randint(1, len(SHAPES) - 1))

    def get_drop_speed(self):
        idx = min(self.level - 1, len(self.drop_speeds) - 1)
        return self.drop_speeds[idx]

    def valid_move(self, piece, dx=0, dy=0):
        for r, row in enumerate(piece.shape):
            for c, cell in enumerate(row):
                if cell:
                    new_x = piece.x + c + dx
                    new_y = piece.y + r + dy
                    
                    # Walls and Floor bounds
                    if new_x < 0 or new_x >= COLS or new_y >= ROWS:
                        return False
                    # Collision with existing blocks (ignore if above board)
                    if new_y >= 0 and self.grid[new_y][new_x] != 0:
                        return False
        return True

    def lock_piece(self):
        for r, row in enumerate(self.current_piece.shape):
            for c, cell in enumerate(row):
                if cell:
                    gy = self.current_piece.y + r
                    gx = self.current_piece.x + c
                    if gy >= 0:
                        self.grid[gy][gx] = self.current_piece.color
        
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        
        # Check if new piece spawns colliding (Game Over)
        if not self.valid_move(self.current_piece):
            self.game_over = True

    def clear_lines(self):
        lines_to_clear = 0
        for r in range(ROWS - 1, -1, -1):
            if 0 not in self.grid[r]:
                lines_to_clear += 1
                # Move all rows above down
                for nr in range(r, 0, -1):
                    self.grid[nr] = self.grid[nr-1][:]
                self.grid[0] = [0] * COLS # New empty top row
                # Since we shifted down, we need to re-check the current row index
                # A simple way in python loop is just to not decrement r in the next iteration, 
                # but since range is fixed, a recursive call or while loop is safer for multi-lines.
                # Simplified approach: just recall clear_lines if a line was found.
                self.clear_lines() 
                return

        if lines_to_clear > 0:
            self.lines_cleared += lines_to_clear
            self.score += SCORES.get(lines_to_clear, 0) * self.level
            self.level = 1 + self.lines_cleared // 10

    def rotate_piece(self):
        # Basic rotation with wall-kick attempt (try rotating back if fails)
        original_shape = copy.deepcopy(self.current_piece.shape)
        self.current_piece.rotate()
        if not self.valid_move(self.current_piece):
             # Restore if invalid
            self.current_piece.shape = original_shape

    def move(self, dx, dy):
        if self.valid_move(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False

    def hard_drop(self):
        while self.move(0, 1):
            pass
        self.lock_piece()
        self.drop_timer = pygame.time.get_ticks() # Reset timer

    def update(self):
        if self.game_over: return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.drop_timer > self.get_drop_speed():
            if not self.move(0, 1):
                self.lock_piece()
            self.drop_timer = current_time

    def get_ghost_piece(self):
        ghost = copy.deepcopy(self.current_piece)
        # Push down until collision
        while self.valid_move(ghost, 0, 1):
            ghost.y += 1
        return ghost

    def draw(self, screen, font_big, font_small):
        # 1. Draw Board Background & Grid
        pygame.draw.rect(screen, BG_COLOR, (0, 0, COLS*CELL_SIZE, HEIGHT))
        for x in range(0, COLS*CELL_SIZE, CELL_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (COLS*CELL_SIZE, y))
            
        # 2. Draw Sidebar
        sidebar_x = COLS*CELL_SIZE
        pygame.draw.rect(screen, SIDEBAR_COLOR, (sidebar_x, 0, SIDEBAR_WIDTH, HEIGHT))
        pygame.draw.line(screen, GRID_COLOR, (sidebar_x, 0), (sidebar_x, HEIGHT), 3)

        # 3. Draw Locked Grid Blocks
        for r in range(ROWS):
            for c in range(COLS):
                if self.grid[r][c]:
                    draw_block3d(screen, c*CELL_SIZE, r*CELL_SIZE, self.grid[r][c])

        if not self.game_over:
            # 4. Draw Ghost Piece (Transparent)
            ghost = self.get_ghost_piece()
            for r, row in enumerate(ghost.shape):
                for c, cell in enumerate(row):
                    if cell:
                        draw_block3d(screen, (ghost.x+c)*CELL_SIZE, (ghost.y+r)*CELL_SIZE, ghost.color, alpha=80)

            # 5. Draw Current Piece
            for r, row in enumerate(self.current_piece.shape):
                for c, cell in enumerate(row):
                    if cell:
                         draw_block3d(screen, (self.current_piece.x+c)*CELL_SIZE, (self.current_piece.y+r)*CELL_SIZE, self.current_piece.color)

        # 6. Draw UI Text
        def draw_text(text, y, font, color=TEXT_COLOR):
            lbl = font.render(text, True, color)
            screen.blit(lbl, (sidebar_x + 20, y))

        draw_text("TETRIS", 30, font_big)
        draw_text(f"SCORE: {self.score}", 100, font_small)
        draw_text(f"LEVEL: {self.level}", 140, font_small)
        draw_text(f"LINES: {self.lines_cleared}", 180, font_small)
        draw_text("NEXT:", 250, font_small)

        # 7. Draw Next Piece Preview
        preview_x = sidebar_x + 40
        preview_y = 300
        # Center the preview based on shape size
        offset_y = 0 if len(self.next_piece.shape) == 2 else -CELL_SIZE//2
        offset_x = 0 if len(self.next_piece.shape[0]) > 2 else CELL_SIZE//2

        for r, row in enumerate(self.next_piece.shape):
            for c, cell in enumerate(row):
                if cell:
                    draw_block3d(screen, preview_x + c*CELL_SIZE + offset_x, preview_y + r*CELL_SIZE + offset_y, self.next_piece.color)

        if self.game_over:
             s = pygame.Surface((COLS*CELL_SIZE, HEIGHT), pygame.SRCALPHA)
             s.fill((0,0,0, 180))
             screen.blit(s, (0,0))
             go_txt = font_big.render("GAME OVER", True, (255, 50, 50))
             res_txt = font_small.render("Press SPACE to restart", True, TEXT_COLOR)
             screen.blit(go_txt, (COLS*CELL_SIZE//2 - go_txt.get_width()//2, HEIGHT//2 - 40))
             screen.blit(res_txt, (COLS*CELL_SIZE//2 - res_txt.get_width()//2, HEIGHT//2 + 20))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris Pro")
    clock = pygame.time.Clock()
    
    # Fonts
    font_big = pygame.font.SysFont('Arial Black', 30)
    font_small = pygame.font.SysFont('Arial', 18, bold=True)

    game = TetrisGame()
    
    # Input handling for sustained movement (DAS - Delayed Auto Shift style simple implementation)
    move_ticker = 0
    MOVE_DELAY = 8 # Frames between lateral moves when holding key

    while True:
        clock.tick(FPS)
        
        # Input Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if game.game_over:
                    if event.key == pygame.K_SPACE:
                        game = TetrisGame()
                else:
                    if event.key == pygame.K_UP:
                        game.rotate_piece()
                    elif event.key == pygame.K_LEFT:
                        game.move(-1, 0)
                        move_ticker = 0
                    elif event.key == pygame.K_RIGHT:
                        game.move(1, 0)
                        move_ticker = 0
                    elif event.key == pygame.K_DOWN:
                        game.move(0, 1)
                        game.drop_timer = pygame.time.get_ticks() # Reset gravity timer on soft drop
                    elif event.key == pygame.K_SPACE:
                        game.hard_drop()

        # Sustained Input Handling
        if not game.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_DOWN]:
                move_ticker += 1
                if move_ticker > MOVE_DELAY:
                    if keys[pygame.K_LEFT]: game.move(-1, 0)
                    if keys[pygame.K_RIGHT]: game.move(1, 0)
                    if keys[pygame.K_DOWN]: 
                        game.move(0, 1)
                        game.score += 1 # Bonus for soft dropping
                    move_ticker = 0 # Reset ticker for sustained speed

        # Game Logic & Render
        game.update()
        game.draw(screen, font_big, font_small)
        pygame.display.flip()

if __name__ == "__main__":
    main()
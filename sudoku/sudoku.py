import pygame
import sys
import random

# --- CONFIGURATION ---
WIDTH, HEIGHT = 600, 700
GRID_SIZE = 600
CELL_SIZE = GRID_SIZE // 9

# COLORS
BG_COLOR = (250, 250, 250)
GRID_BLACK = (0, 0, 0)
GRID_GRAY = (200, 200, 200)
HIGHLIGHT = (230, 240, 255)
SELECTED = (180, 210, 255)
TEXT_BLACK = (20, 20, 20)
TEXT_BLUE = (0, 0, 200)
TEXT_RED = (220, 0, 0)

# --- PIXEL FONT ENGINE ---
PIXEL_FONT = {
    '1': [0x20, 0x60, 0x20, 0x20, 0x20, 0x20, 0x70],
    '2': [0x70, 0x88, 0x08, 0x30, 0x40, 0x80, 0xF8],
    '3': [0xF8, 0x08, 0x10, 0x30, 0x08, 0x88, 0x70],
    '4': [0x10, 0x30, 0x50, 0x90, 0xF8, 0x10, 0x10],
    '5': [0xF8, 0x80, 0xF0, 0x08, 0x08, 0x88, 0x70],
    '6': [0x30, 0x40, 0x80, 0xF0, 0x88, 0x88, 0x70],
    '7': [0xF8, 0x08, 0x10, 0x20, 0x40, 0x40, 0x40],
    '8': [0x70, 0x88, 0x88, 0x70, 0x88, 0x88, 0x70],
    '9': [0x70, 0x88, 0x88, 0x78, 0x08, 0x88, 0x70],
    'N': [0x88, 0xC8, 0xA8, 0x98, 0x88, 0x88, 0x88],
    'E': [0xF8, 0x80, 0x80, 0xF0, 0x80, 0x80, 0xF8],
    'W': [0x88, 0x88, 0x88, 0xA8, 0xA8, 0xD8, 0x88],
    'G': [0x78, 0x80, 0x80, 0x98, 0x88, 0x88, 0x70],
    'A': [0x70, 0x88, 0x88, 0xF8, 0x88, 0x88, 0x88],
    'M': [0x88, 0xD8, 0xA8, 0xA8, 0x88, 0x88, 0x88],
    ' ': [0x00] * 7
}

def draw_text(surface, text, x, y, scale=2, color=TEXT_BLACK, center=False):
    text = str(text).upper()
    width = len(text) * 6 * scale
    start_x = x
    if center: start_x = x - width // 2
    
    cursor_x = start_x
    for char in text:
        if char in PIXEL_FONT:
            rows = PIXEL_FONT[char]
            for r, row_val in enumerate(rows):
                for c in range(5):
                    if (row_val >> (7 - c)) & 1:
                        pygame.draw.rect(surface, color, (cursor_x + c * scale, y + r * scale, scale, scale))
        cursor_x += 6 * scale

# --- SUDOKU GENERATOR (FIXED) ---
class SudokuGenerator:
    def __init__(self):
        self.grid = [[0]*9 for _ in range(9)]
        self.fill_diagonal()
        self.solve(self.grid)
        self.remove_digits()

    def fill_diagonal(self):
        for i in range(0, 9, 3):
            self.fill_box(i, i)

    def fill_box(self, row, col):
        # Optimization: Shuffle 1-9 and place them directly
        # This prevents the infinite loop of guessing random numbers
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                self.grid[row+i][col+j] = nums.pop()

    def is_safe(self, grid, row, col, num):
        # Row check
        for x in range(9):
            if grid[row][x] == num: return False
        # Col check
        for x in range(9):
            if grid[x][col] == num: return False
        # Box check
        startRow, startCol = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + startRow][j + startCol] == num: return False
        return True

    def solve(self, grid):
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    for num in range(1, 10):
                        if self.is_safe(grid, r, c, num):
                            grid[r][c] = num
                            if self.solve(grid): return True
                            grid[r][c] = 0
                    return False
        return True

    def remove_digits(self):
        # Optimization: Collect valid spots first, then shuffle
        # Prevents infinite loop if grid is sparse
        candidates = [(r,c) for r in range(9) for c in range(9) if self.grid[r][c] != 0]
        random.shuffle(candidates)
        
        count = 40 # Difficulty
        for r, c in candidates:
            if count <= 0: break
            self.grid[r][c] = 0
            count -= 1

# --- MAIN GAME ---
def main():
    print("Initializing Pygame...")
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")
    clock = pygame.time.Clock()
    
    print("Generating Puzzle...")
    # Generate Solution
    full_gen = SudokuGenerator()
    solution = [row[:] for row in full_gen.grid]
    
    # Generate Playable Board
    game_grid = [row[:] for row in solution]
    
    # Remove digits safely
    candidates = [(r,c) for r in range(9) for c in range(9)]
    random.shuffle(candidates)
    
    holes = 45 # Difficulty
    for r, c in candidates:
        if holes <= 0: break
        game_grid[r][c] = 0
        holes -= 1
            
    # Track original numbers
    immutable = [[(game_grid[r][c] != 0) for c in range(9)] for r in range(9)]
    selected = (0, 0)
    
    print("Game Loop Started!")
    while True:
        clock.tick(30)
        screen.fill(BG_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < GRID_SIZE:
                    selected = (y // CELL_SIZE, x // CELL_SIZE)
                if y > GRID_SIZE + 20 and x > WIDTH//2 - 60 and x < WIDTH//2 + 60:
                    main() # Restart

            if event.type == pygame.KEYDOWN:
                r, c = selected
                if event.key == pygame.K_UP: selected = ((r-1)%9, c)
                if event.key == pygame.K_DOWN: selected = ((r+1)%9, c)
                if event.key == pygame.K_LEFT: selected = (r, (c-1)%9)
                if event.key == pygame.K_RIGHT: selected = (r, (c+1)%9)
                
                val = 0
                if event.key == pygame.K_1 or event.key == pygame.K_KP1: val = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2: val = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3: val = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4: val = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5: val = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6: val = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7: val = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP8: val = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9: val = 9
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE: val = 0
                
                if val is not None and not immutable[r][c]:
                    game_grid[r][c] = val

        # Drawing
        sr, sc = selected
        
        # Highlights
        pygame.draw.rect(screen, HIGHLIGHT, (0, sr*CELL_SIZE, WIDTH, CELL_SIZE))
        pygame.draw.rect(screen, HIGHLIGHT, (sc*CELL_SIZE, 0, CELL_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, SELECTED, (sc*CELL_SIZE, sr*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Grid
        for i in range(10):
            th = 4 if i % 3 == 0 else 1
            pygame.draw.line(screen, GRID_BLACK if i%3==0 else GRID_GRAY, (0, i*CELL_SIZE), (WIDTH, i*CELL_SIZE), th)
            pygame.draw.line(screen, GRID_BLACK if i%3==0 else GRID_GRAY, (i*CELL_SIZE, 0), (i*CELL_SIZE, GRID_SIZE), th)

        # Numbers
        for r in range(9):
            for c in range(9):
                val = game_grid[r][c]
                if val != 0:
                    color = TEXT_BLACK if immutable[r][c] else TEXT_BLUE
                    if not immutable[r][c]:
                        is_conflict = False
                        if game_grid[r].count(val) > 1: is_conflict = True
                        if [game_grid[x][c] for x in range(9)].count(val) > 1: is_conflict = True
                        br, bc = r//3 * 3, c//3 * 3
                        box = [game_grid[br+i][bc+j] for i in range(3) for j in range(3)]
                        if box.count(val) > 1: is_conflict = True
                        if is_conflict: color = TEXT_RED

                    draw_text(screen, str(val), c*CELL_SIZE + CELL_SIZE//2, r*CELL_SIZE + CELL_SIZE//2 - 10, 3, color, center=True)

        # UI
        pygame.draw.rect(screen, (220, 220, 220), (WIDTH//2 - 60, GRID_SIZE + 20, 120, 40))
        draw_text(screen, "NEW GAME", WIDTH//2, GRID_SIZE + 32, 2, (50, 50, 50), center=True)

        pygame.display.flip()

if __name__ == "__main__":
    main()
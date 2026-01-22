import pygame
import sys
import random

# --- CONFIGURATION ---
WIDTH, HEIGHT = 800, 900
ROWS, COLS = 16, 16
MINES = 40
CELL_SIZE = 40
MARGIN_X = (WIDTH - (COLS * CELL_SIZE)) // 2
MARGIN_Y = 100

# COLORS
BG_COLOR = (192, 192, 192)
CELL_BG = (180, 180, 180)
CELL_HIDDEN = (220, 220, 220)
BORDER_LIGHT = (255, 255, 255)
BORDER_DARK = (100, 100, 100)
TEXT_COL = (0, 0, 0)
HIGHLIGHT_COL = (180, 220, 255) # Color when chording
NUM_COLORS = {
    1: (0, 0, 255), 2: (0, 128, 0), 3: (255, 0, 0), 4: (0, 0, 128),
    5: (128, 0, 0), 6: (0, 128, 128), 7: (0, 0, 0), 8: (128, 128, 128)
}

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
    'F': [0xF8, 0x80, 0x80, 0xF0, 0x80, 0x80, 0x80],
    'M': [0x88, 0xD8, 0xA8, 0xA8, 0x88, 0x88, 0x88],
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
        elif char in ['0',' ']: pass
        else:
            pygame.draw.rect(surface, color, (cursor_x, y, 5*scale, 7*scale))
        cursor_x += 6 * scale

class Minesweeper:
    def __init__(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)] 
        self.visible = [[False for _ in range(COLS)] for _ in range(ROWS)]
        self.flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
        self.game_over = False
        self.won = False
        self.first_click = True
        self.start_time = 0
        self.highlight_neighbors = None # For chording highlight

    def generate_mines(self, safe_r, safe_c):
        count = 0
        while count < MINES:
            r, c = random.randint(0, ROWS-1), random.randint(0, COLS-1)
            if self.grid[r][c] != 9 and abs(r-safe_r) > 1 and abs(c-safe_c) > 1:
                self.grid[r][c] = 9
                count += 1
        
        for r in range(ROWS):
            for c in range(COLS):
                if self.grid[r][c] == 9: continue
                mines_near = 0
                for dr in [-1,0,1]:
                    for dc in [-1,0,1]:
                        if 0 <= r+dr < ROWS and 0 <= c+dc < COLS:
                            if self.grid[r+dr][c+dc] == 9: mines_near += 1
                self.grid[r][c] = mines_near

    def flood_fill(self, r, c):
        if not (0 <= r < ROWS and 0 <= c < COLS): return
        if self.visible[r][c] or self.flagged[r][c]: return
        
        self.visible[r][c] = True
        
        if self.grid[r][c] == 0:
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    if dr == 0 and dc == 0: continue
                    self.flood_fill(r+dr, c+dc)

    def reveal(self, r, c):
        if self.game_over or self.flagged[r][c]: return
        
        if self.first_click:
            self.generate_mines(r, c)
            self.first_click = False
            self.start_time = pygame.time.get_ticks()

        if self.grid[r][c] == 9:
            self.game_over = True
            self.won = False
            for nr in range(ROWS):
                for nc in range(COLS):
                    if self.grid[nr][nc] == 9: self.visible[nr][nc] = True
        else:
            self.flood_fill(r, c)
            self.check_win()

    def toggle_flag(self, r, c):
        if not self.visible[r][c] and not self.game_over:
            self.flagged[r][c] = not self.flagged[r][c]

    def chord(self, r, c):
        """Trigger neighbors if flags match number, else highlight."""
        if not self.visible[r][c] or self.grid[r][c] == 0 or self.game_over:
            return

        # 1. Count Flags around
        flags_near = 0
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr==0 and dc==0: continue
                nr, nc = r+dr, c+dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    neighbors.append((nr, nc))
                    if self.flagged[nr][nc]: flags_near += 1
        
        # 2. Logic
        if flags_near == self.grid[r][c]:
            # Chord Open
            for nr, nc in neighbors:
                if not self.visible[nr][nc] and not self.flagged[nr][nc]:
                    self.reveal(nr, nc)
            self.highlight_neighbors = None
        else:
            # Highlight only (Not enough flags)
            self.highlight_neighbors = []
            for nr, nc in neighbors:
                if not self.visible[nr][nc] and not self.flagged[nr][nc]:
                    self.highlight_neighbors.append((nr, nc))

    def check_win(self):
        for r in range(ROWS):
            for c in range(COLS):
                if self.grid[r][c] != 9 and not self.visible[r][c]:
                    return
        self.game_over = True
        self.won = True

# --- GRAPHICS ---
def draw_3d_rect(screen, rect, pressed=False, highlight=False):
    color = CELL_HIDDEN
    if pressed: color = CELL_BG
    if highlight: color = HIGHLIGHT_COL # For chording hint
    
    pygame.draw.rect(screen, color, rect)
    
    if not pressed and not highlight:
        pygame.draw.line(screen, BORDER_LIGHT, rect.topleft, rect.topright, 3)
        pygame.draw.line(screen, BORDER_LIGHT, rect.topleft, rect.bottomleft, 3)
        pygame.draw.line(screen, BORDER_DARK, rect.bottomleft, rect.bottomright, 3)
        pygame.draw.line(screen, BORDER_DARK, rect.topright, rect.bottomright, 3)
    else:
        pygame.draw.rect(screen, (150,150,150), rect, 1)

def draw_mine(screen, x, y):
    cx, cy = x + CELL_SIZE//2, y + CELL_SIZE//2
    pygame.draw.circle(screen, (0,0,0), (cx, cy), CELL_SIZE//3)
    pygame.draw.line(screen, (0,0,0), (cx-10, cy), (cx+10, cy), 3)
    pygame.draw.line(screen, (0,0,0), (cx, cy-10), (cx, cy+10), 3)
    pygame.draw.line(screen, (0,0,0), (cx-7, cy-7), (cx+7, cy+7), 3)
    pygame.draw.line(screen, (0,0,0), (cx-7, cy+7), (cx+7, cy-7), 3)
    pygame.draw.circle(screen, (255,255,255), (cx-5, cy-5), 3)

def draw_flag(screen, x, y):
    cx, cy = x + CELL_SIZE//2, y + CELL_SIZE//2
    pygame.draw.line(screen, (0,0,0), (cx-5, cy+10), (cx-5, cy-10), 2)
    pygame.draw.polygon(screen, (255,0,0), [(cx-5, cy-10), (cx+8, cy-5), (cx-5, cy)])
    pygame.draw.line(screen, (0,0,0), (cx-8, cy+10), (cx+5, cy+10), 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper Pro")
    clock = pygame.time.Clock()
    
    game = Minesweeper()
    left_down = False
    right_down = False
    
    while True:
        clock.tick(30)
        screen.fill(BG_COLOR)
        
        # --- UI HEADER ---
        pygame.draw.rect(screen, (150,150,150), (MARGIN_X, 10, COLS*CELL_SIZE, 80))
        pygame.draw.line(screen, BORDER_DARK, (MARGIN_X, 10), (MARGIN_X+COLS*CELL_SIZE, 10), 3)
        
        face_x, face_y = WIDTH//2, 50
        pygame.draw.circle(screen, (255,255,0), (face_x, face_y), 25)
        pygame.draw.circle(screen, (0,0,0), (face_x, face_y), 25, 2)
        
        if game.game_over:
            if game.won: 
                 pygame.draw.line(screen, (0,0,0), (face_x-10, face_y-5), (face_x+10, face_y-5), 4)
                 pygame.draw.arc(screen, (0,0,0), (face_x-10, face_y, 20, 10), 0, 3.14, 2)
            else:
                 draw_text(screen, "X X", face_x, face_y-5, 2, (0,0,0), center=True)
                 pygame.draw.arc(screen, (0,0,0), (face_x-10, face_y+10, 20, 10), 0, 3.14, 2)
        else:
            pygame.draw.circle(screen, (0,0,0), (face_x-8, face_y-5), 3)
            pygame.draw.circle(screen, (0,0,0), (face_x+8, face_y-5), 3)
            pygame.draw.arc(screen, (0,0,0), (face_x-10, face_y, 20, 15), 3.14, 0, 2)

        flags_placed = sum([row.count(True) for row in game.flagged])
        draw_text(screen, f"{MINES - flags_placed}", MARGIN_X + 40, 50, 4, (255,0,0), center=True)
        elapsed = 0
        if not game.first_click and not game.game_over:
            elapsed = (pygame.time.get_ticks() - game.start_time) // 1000
        draw_text(screen, f"{elapsed:03}", MARGIN_X + COLS*CELL_SIZE - 50, 50, 4, (255,0,0), center=True)

        # --- GRID ---
        for r in range(ROWS):
            for c in range(COLS):
                x = MARGIN_X + c * CELL_SIZE
                y = MARGIN_Y + r * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                # Highlight check
                is_highlighted = False
                if game.highlight_neighbors and (r, c) in game.highlight_neighbors:
                    is_highlighted = True

                if game.visible[r][c]:
                    draw_3d_rect(screen, rect, pressed=True)
                    val = game.grid[r][c]
                    if val == 9: draw_mine(screen, x, y)
                    elif val > 0:
                        col = NUM_COLORS.get(val, (0,0,0))
                        draw_text(screen, str(val), x+CELL_SIZE//2, y+CELL_SIZE//2 - 10, 3, col, center=True)
                else:
                    draw_3d_rect(screen, rect, pressed=False, highlight=is_highlighted)
                    if game.flagged[r][c]: draw_flag(screen, x, y)
        
        # --- INPUT ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                
                if (mx-face_x)**2 + (my-face_y)**2 < 25**2:
                    game = Minesweeper()
                    continue

                if MARGIN_X <= mx < MARGIN_X + COLS*CELL_SIZE and MARGIN_Y <= my < MARGIN_Y + ROWS*CELL_SIZE:
                    c = (mx - MARGIN_X) // CELL_SIZE
                    r = (my - MARGIN_Y) // CELL_SIZE
                    
                    # Track Double Click State
                    if event.button == 1: left_down = True
                    if event.button == 3: right_down = True
                    
                    # CHORDING (Left+Right OR Middle Click)
                    if (left_down and right_down) or event.button == 2:
                        game.chord(r, c)
                    # Normal Click (Only if not chording)
                    elif event.button == 1: 
                        game.reveal(r, c)
                        game.highlight_neighbors = None
                    elif event.button == 3: 
                        game.toggle_flag(r, c)
                        game.highlight_neighbors = None

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: left_down = False
                if event.button == 3: right_down = False
                # Clear highlight on release
                game.highlight_neighbors = None

        pygame.display.flip()

if __name__ == "__main__":
    main()
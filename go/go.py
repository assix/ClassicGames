import pygame
import sys
import copy
import time
import random

# --- CONFIGURATION ---
GRID_SIZE = 9  # 9x9 is standard for quick games. 13 or 19 also work.
CELL_SIZE = 70
MARGIN = 60
WIDTH = GRID_SIZE * CELL_SIZE + (MARGIN * 2)
HEIGHT = GRID_SIZE * CELL_SIZE + (MARGIN * 2) + 80 # Extra space for UI

# COLORS
WOOD_DARK = (180, 130, 70)
WOOD_LIGHT = (220, 170, 110)
BLACK = (20, 20, 20)
WHITE = (240, 240, 240)
HIGHLIGHT = (255, 50, 50)  # Red for last move
GHOST = (0, 0, 0, 100)
TEXT_COL = (255, 255, 255)
UI_BG = (40, 40, 50)

# STATES
EMPTY = 0
B_STONE = 1
W_STONE = 2

# --- PIXEL FONT ENGINE ---
PIXEL_FONT = {
    'A': [0x70, 0x88, 0x88, 0xF8, 0x88, 0x88, 0x88],
    'B': [0xF0, 0x88, 0x88, 0xF0, 0x88, 0x88, 0xF0],
    'C': [0x70, 0x88, 0x80, 0x80, 0x80, 0x88, 0x70],
    'D': [0xF0, 0x88, 0x88, 0x88, 0x88, 0x88, 0xF0],
    'E': [0xF8, 0x80, 0x80, 0xF0, 0x80, 0x80, 0xF8],
    'G': [0x78, 0x80, 0x80, 0x98, 0x88, 0x88, 0x70],
    'H': [0x88, 0x88, 0x88, 0xF8, 0x88, 0x88, 0x88],
    'I': [0x70, 0x20, 0x20, 0x20, 0x20, 0x20, 0x70],
    'K': [0x88, 0x90, 0xA0, 0xC0, 0xA0, 0x90, 0x88],
    'L': [0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0xF8],
    'M': [0x88, 0xD8, 0xA8, 0xA8, 0x88, 0x88, 0x88],
    'N': [0x88, 0xC8, 0xA8, 0x98, 0x88, 0x88, 0x88],
    'O': [0x70, 0x88, 0x88, 0x88, 0x88, 0x88, 0x70],
    'P': [0xF0, 0x88, 0x88, 0xF0, 0x80, 0x80, 0x80],
    'R': [0xF0, 0x88, 0x88, 0xF0, 0xA0, 0x90, 0x88],
    'S': [0x70, 0x88, 0x80, 0x70, 0x08, 0x88, 0x70],
    'T': [0xF8, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20],
    'U': [0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x70],
    'W': [0x88, 0x88, 0x88, 0xA8, 0xA8, 0xD8, 0x88],
    'Y': [0x88, 0x88, 0x50, 0x20, 0x20, 0x20, 0x20],
    ' ': [0x00] * 7,
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
    '.': [0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x60],
    ':': [0x00, 0x60, 0x60, 0x00, 0x60, 0x60, 0x00],
}

def draw_text(surface, text, x, y, scale=2, color=TEXT_COL):
    cursor_x = x
    for char in str(text).upper():
        if char in PIXEL_FONT:
            rows = PIXEL_FONT[char]
            for r, row_val in enumerate(rows):
                for c in range(5):
                    if (row_val >> (7 - c)) & 1:
                        pygame.draw.rect(surface, color, 
                                       (cursor_x + c * scale, y + r * scale, scale, scale))
        cursor_x += 6 * scale

# --- GO LOGIC ---
class GoBoard:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.turn = B_STONE
        self.last_move = None
        self.prisoners = {B_STONE: 0, W_STONE: 0} # Stones captured BY this color
        self.history = [] # For Ko checking
        self.passed = False
        self.game_over = False
        self.score_res = None
        self.save_state()

    def save_state(self):
        # Save a deep copy of grid for Ko checking
        self.history.append([row[:] for row in self.grid])

    def get_group(self, r, c, board=None):
        if board is None: board = self.grid
        color = board[r][c]
        if color == EMPTY: return set()
        
        group = set()
        stack = [(r, c)]
        while stack:
            cur_r, cur_c = stack.pop()
            if (cur_r, cur_c) in group: continue
            group.add((cur_r, cur_c))
            
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = cur_r + dr, cur_c + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                    if board[nr][nc] == color:
                        stack.append((nr, nc))
        return group

    def count_liberties(self, group, board=None):
        if board is None: board = self.grid
        liberties = set()
        for r, c in group:
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                    if board[nr][nc] == EMPTY:
                        liberties.add((nr, nc))
        return len(liberties)

    def is_valid_move(self, r, c, color):
        if self.grid[r][c] != EMPTY: return False
        
        # Simulate move
        temp_board = [row[:] for row in self.grid]
        temp_board[r][c] = color
        
        # Check Captures
        opponent = W_STONE if color == B_STONE else B_STONE
        captured_any = False
        
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                if temp_board[nr][nc] == opponent:
                    grp = self.get_group(nr, nc, temp_board)
                    if self.count_liberties(grp, temp_board) == 0:
                        captured_any = True
                        for gr, gc in grp: temp_board[gr][gc] = EMPTY
        
        # Check Suicide
        my_grp = self.get_group(r, c, temp_board)
        if self.count_liberties(my_grp, temp_board) == 0:
            return False # Suicide is illegal (unless we handled capture above, but simplified here)

        # Check Ko (Board repetition)
        if len(self.history) > 1 and temp_board == self.history[-2]:
            return False

        return True

    def place_stone(self, r, c):
        if not self.is_valid_move(r, c, self.turn): return False
        
        self.grid[r][c] = self.turn
        opponent = W_STONE if self.turn == B_STONE else B_STONE
        
        # Handle Captures
        captured_count = 0
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                if self.grid[nr][nc] == opponent:
                    grp = self.get_group(nr, nc)
                    if self.count_liberties(grp) == 0:
                        for gr, gc in grp:
                            self.grid[gr][gc] = EMPTY
                            captured_count += 1
        
        self.prisoners[self.turn] += captured_count
        self.last_move = (r, c)
        self.turn = opponent
        self.passed = False
        self.save_state()
        return True

    def pass_turn(self):
        if self.passed: # Second consecutive pass
            self.game_over = True
            self.calculate_score()
        else:
            self.passed = True
            self.turn = W_STONE if self.turn == B_STONE else B_STONE
            # Add current state again to history to keep Ko logic simple
            self.history.append([row[:] for row in self.grid]) 

    def calculate_score(self):
        # Simplified Area Scoring + Prisoners
        # 1. Count stones
        # 2. Flood fill empty spots to see if they reach only ONE color
        
        b_area = 0
        w_area = 0
        
        visited = set()
        
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == B_STONE:
                    b_area += 1
                elif self.grid[r][c] == W_STONE:
                    w_area += 1
                elif (r,c) not in visited:
                    # Empty spot flood fill
                    region = []
                    stack = [(r, c)]
                    reaches_b = False
                    reaches_w = False
                    
                    while stack:
                        cur_r, cur_c = stack.pop()
                        if (cur_r, cur_c) in visited: continue
                        visited.add((cur_r, cur_c))
                        region.append((cur_r, cur_c))
                        
                        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                            nr, nc = cur_r + dr, cur_c + dc
                            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                                if self.grid[nr][nc] == B_STONE: reaches_b = True
                                elif self.grid[nr][nc] == W_STONE: reaches_w = True
                                else: stack.append((nr, nc))
                    
                    if reaches_b and not reaches_w: b_area += len(region)
                    if reaches_w and not reaches_b: w_area += len(region)
        
        # Add Prisoners? In Area scoring usually captures don't count, 
        # but in Japanese territory scoring they do. 
        # Let's use simple Area scoring (Chinese style) which is robust for bots.
        # Komi for White (standard 7.5 usually, let's use 6.5)
        komi = 6.5
        w_total = w_area + komi
        
        self.score_res = (b_area, w_total)

# --- AI ---
class AI:
    def __init__(self, color):
        self.color = color

    def get_move(self, board):
        # 1. Check for immediate captures (Atari)
        opponent = W_STONE if self.color == B_STONE else B_STONE
        
        # Look for opponent groups with 1 liberty
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if board.grid[r][c] == opponent:
                    grp = board.get_group(r, c)
                    if board.count_liberties(grp) == 1:
                        # Find the killing move
                        for lr, lc in board.grid: pass # dummy
                        # Actual liberty finding
                        for gr, gc in grp:
                             for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                                nr, nc = gr + dr, gc + dc
                                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                                    if board.grid[nr][nc] == EMPTY:
                                        if board.is_valid_move(nr, nc, self.color):
                                            return (nr, nc)

        # 2. Check for self Atari (Save own stones)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if board.grid[r][c] == self.color:
                    grp = board.get_group(r, c)
                    if board.count_liberties(grp) == 1:
                        # Try to extend
                        for gr, gc in grp:
                             for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                                nr, nc = gr + dr, gc + dc
                                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                                    if board.grid[nr][nc] == EMPTY:
                                        if board.is_valid_move(nr, nc, self.color):
                                            return (nr, nc)

        # 3. Play near existing stones (shape) or center
        valid_moves = []
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if board.is_valid_move(r, c, self.color):
                    weight = 1
                    # Prefer moves near other stones
                    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                         nr, nc = r + dr, c + dc
                         if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                             if board.grid[nr][nc] != EMPTY: weight += 2
                    
                    # Avoid edges early game
                    if r == 0 or r == GRID_SIZE-1 or c == 0 or c == GRID_SIZE-1:
                        weight -= 0.5
                    
                    valid_moves.append((weight, r, c))
        
        if valid_moves:
            valid_moves.sort(key=lambda x: x[0], reverse=True)
            # Pick from top 5 weighted
            candidates = valid_moves[:5]
            return random.choice(candidates)[1:]
        
        return None # Pass

# --- MAIN GAME ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Go (9x9) vs AI")
    clock = pygame.time.Clock()
    
    board = GoBoard()
    ai = AI(W_STONE) # AI is White
    
    # UI Buttons
    btn_pass = pygame.Rect(WIDTH - 200, HEIGHT - 70, 80, 40)
    btn_reset = pygame.Rect(WIDTH - 100, HEIGHT - 70, 80, 40)
    
    run = True
    while run:
        clock.tick(30)
        
        # AI Turn
        if not board.game_over and board.turn == ai.color:
            pygame.display.set_caption("Go (AI Thinking...)")
            pygame.time.wait(500)
            move = ai.get_move(board)
            if move:
                board.place_stone(move[0], move[1])
            else:
                board.pass_turn()
            pygame.display.set_caption("Go (Your Turn)")

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not board.game_over:
                if board.turn != ai.color: # Human Turn
                    x, y = event.pos
                    
                    # Check Board Click
                    # Grid starts at MARGIN, cells are CELL_SIZE
                    # Nearest intersection
                    col = round((x - MARGIN) / CELL_SIZE)
                    row = round((y - MARGIN) / CELL_SIZE)
                    
                    # Snap check
                    grid_x = MARGIN + col * CELL_SIZE
                    grid_y = MARGIN + row * CELL_SIZE
                    dist = ((x - grid_x)**2 + (y - grid_y)**2)**0.5
                    
                    if dist < CELL_SIZE * 0.4:
                        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                            board.place_stone(row, col)

                    # Check Pass
                    if btn_pass.collidepoint(event.pos):
                        board.pass_turn()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                 if btn_reset.collidepoint(event.pos):
                    board = GoBoard()
        
        # Drawing
        screen.fill(UI_BG)
        
        # Draw Board Background
        board_rect = pygame.Rect(MARGIN - 20, MARGIN - 20, (GRID_SIZE-1)*CELL_SIZE + 40, (GRID_SIZE-1)*CELL_SIZE + 40)
        pygame.draw.rect(screen, WOOD_DARK, board_rect)
        pygame.draw.rect(screen, WOOD_LIGHT, (MARGIN, MARGIN, (GRID_SIZE-1)*CELL_SIZE, (GRID_SIZE-1)*CELL_SIZE))
        
        # Draw Lines
        for i in range(GRID_SIZE):
            # Horizontal
            start = (MARGIN, MARGIN + i * CELL_SIZE)
            end = (MARGIN + (GRID_SIZE-1) * CELL_SIZE, MARGIN + i * CELL_SIZE)
            pygame.draw.line(screen, BLACK, start, end, 2)
            # Vertical
            start = (MARGIN + i * CELL_SIZE, MARGIN)
            end = (MARGIN + i * CELL_SIZE, MARGIN + (GRID_SIZE-1) * CELL_SIZE)
            pygame.draw.line(screen, BLACK, start, end, 2)
        
        # Draw Hoshi (Star points for 9x9)
        stars = [(2,2), (6,2), (4,4), (2,6), (6,6)]
        for r, c in stars:
            sx = MARGIN + c * CELL_SIZE
            sy = MARGIN + r * CELL_SIZE
            pygame.draw.circle(screen, BLACK, (sx, sy), 5)
            
        # Draw Stones
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if board.grid[r][c] != EMPTY:
                    cx = MARGIN + c * CELL_SIZE
                    cy = MARGIN + r * CELL_SIZE
                    col = BLACK if board.grid[r][c] == B_STONE else WHITE
                    pygame.draw.circle(screen, col, (cx, cy), CELL_SIZE//2 - 2)
                    
                    # Shading
                    if col == WHITE:
                         pygame.draw.circle(screen, (200,200,200), (cx, cy), CELL_SIZE//2 - 2, 1)
        
        # Highlight Last Move
        if board.last_move:
            lr, lc = board.last_move
            cx = MARGIN + lc * CELL_SIZE
            cy = MARGIN + lr * CELL_SIZE
            col = WHITE if board.grid[lr][lc] == B_STONE else BLACK
            pygame.draw.circle(screen, HIGHLIGHT, (cx, cy), 5)
            
        # UI
        pygame.draw.rect(screen, (60, 60, 70), btn_pass)
        pygame.draw.rect(screen, (60, 60, 70), btn_reset)
        draw_text(screen, "PASS", btn_pass.x + 15, btn_pass.y + 12)
        draw_text(screen, "RST", btn_reset.x + 20, btn_reset.y + 12)
        
        status = f"BLACK:{board.prisoners[B_STONE]}  WHITE:{board.prisoners[W_STONE]}"
        if board.turn == B_STONE: status += " (YOUR TURN)"
        else: status += " (AI TURN)"
        
        if board.game_over:
            b_s, w_s = board.score_res
            status = f"GAME OVER! B:{b_s} W:{w_s}"
            winner = "YOU WIN" if b_s > w_s else "AI WINS"
            draw_text(screen, winner, WIDTH//2 - 60, HEIGHT - 130, 3, HIGHLIGHT)
            
        draw_text(screen, status, 20, HEIGHT - 120)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
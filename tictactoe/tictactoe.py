import pygame
import sys
import random
import math

# --- CONFIGURATION ---
WIDTH, HEIGHT = 600, 700 # Extra height for UI
BOARD_SIZE = 600
CELL_SIZE = BOARD_SIZE // 3
LINE_WIDTH = 10
MARGIN = 15

# COLORS
BG_COLOR = (20, 20, 30)
GRID_COLOR = (50, 50, 70)
X_COLOR = (84, 214, 247)  # Cyan
O_COLOR = (255, 100, 100) # Red
WIN_LINE_COLOR = (255, 215, 0) # Gold
TEXT_COL = (255, 255, 255)

# --- PIXEL FONT ENGINE (Crash-Proof) ---
PIXEL_FONT = {
    'A': [0x70, 0x88, 0x88, 0xF8, 0x88, 0x88, 0x88],
    'B': [0xF0, 0x88, 0x88, 0xF0, 0x88, 0x88, 0xF0],
    'C': [0x70, 0x88, 0x80, 0x80, 0x80, 0x88, 0x70],
    'D': [0xF0, 0x88, 0x88, 0x88, 0x88, 0x88, 0xF0],
    'E': [0xF8, 0x80, 0x80, 0xF0, 0x80, 0x80, 0xF8],
    'G': [0x78, 0x80, 0x80, 0x98, 0x88, 0x88, 0x70],
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
    'V': [0x88, 0x88, 0x88, 0x88, 0x88, 0x50, 0x20],
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
    '!': [0x20, 0x20, 0x20, 0x20, 0x00, 0x20, 0x00],
    ':': [0x00, 0x60, 0x60, 0x00, 0x60, 0x60, 0x00],
    '-': [0x00, 0x00, 0x00, 0xFC, 0x00, 0x00, 0x00],
}

def draw_text(surface, text, x, y, scale=2, color=TEXT_COL, center=False):
    text = str(text).upper()
    width = 0
    for char in text:
        width += 6 * scale
    
    start_x = x
    if center:
        start_x = x - width // 2
    
    cursor_x = start_x
    for char in text:
        if char in PIXEL_FONT:
            rows = PIXEL_FONT[char]
            for r, row_val in enumerate(rows):
                for c in range(5):
                    if (row_val >> (7 - c)) & 1:
                        pygame.draw.rect(surface, color, 
                                       (cursor_x + c * scale, y + r * scale, scale, scale))
        cursor_x += 6 * scale

# --- GAME LOGIC ---
class Game:
    def __init__(self):
        self.board = [None] * 9 # 0-8
        self.turn = 'X' # Player starts
        self.winner = None
        self.winning_line = None
        self.scores = {'X': 0, 'O': 0}
        self.ai_timer = 0

    def reset(self):
        self.board = [None] * 9
        self.turn = 'X'
        self.winner = None
        self.winning_line = None

    def check_win(self, board):
        # Rows
        for i in range(0, 9, 3):
            if board[i] and board[i] == board[i+1] == board[i+2]:
                return board[i], (i, i+1, i+2)
        # Cols
        for i in range(3):
            if board[i] and board[i] == board[i+3] == board[i+6]:
                return board[i], (i, i+3, i+6)
        # Diagonals
        if board[0] and board[0] == board[4] == board[8]:
            return board[0], (0, 4, 8)
        if board[2] and board[2] == board[4] == board[6]:
            return board[2], (2, 4, 6)
        
        if None not in board:
            return 'DRAW', None
        return None, None

    def make_move(self, idx):
        if self.board[idx] is None and not self.winner:
            self.board[idx] = self.turn
            res, line = self.check_win(self.board)
            if res:
                self.winner = res
                self.winning_line = line
                if res != 'DRAW': self.scores[res] += 1
            else:
                self.turn = 'O' if self.turn == 'X' else 'X'
                if self.turn == 'O': self.ai_timer = 20 # Delay for AI feel

    # --- MINIMAX AI ---
    def minimax(self, board, depth, is_max):
        res, _ = self.check_win(board)
        if res == 'O': return 10 - depth
        if res == 'X': return depth - 10
        if res == 'DRAW': return 0

        if is_max:
            best = -1000
            for i in range(9):
                if board[i] is None:
                    board[i] = 'O'
                    best = max(best, self.minimax(board, depth+1, False))
                    board[i] = None
            return best
        else:
            best = 1000
            for i in range(9):
                if board[i] is None:
                    board[i] = 'X'
                    best = min(best, self.minimax(board, depth+1, True))
                    board[i] = None
            return best

    def ai_move(self):
        best_val = -1000
        best_move = -1
        
        # Optimization: If center is open, take it (speeds up processing)
        if self.board[4] is None: return 4

        for i in range(9):
            if self.board[i] is None:
                self.board[i] = 'O'
                move_val = self.minimax(self.board, 0, False)
                self.board[i] = None
                
                if move_val > best_val:
                    best_val = move_val
                    best_move = i
        
        return best_move

# --- RENDERING ---
def draw_grid(screen):
    # Vertical
    pygame.draw.line(screen, GRID_COLOR, (CELL_SIZE, 0), (CELL_SIZE, BOARD_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, GRID_COLOR, (CELL_SIZE*2, 0), (CELL_SIZE*2, BOARD_SIZE), LINE_WIDTH)
    # Horizontal
    pygame.draw.line(screen, GRID_COLOR, (0, CELL_SIZE), (WIDTH, CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, GRID_COLOR, (0, CELL_SIZE*2), (WIDTH, CELL_SIZE*2), LINE_WIDTH)

def draw_marks(screen, board):
    for i in range(9):
        if board[i] is None: continue
        
        r = i // 3
        c = i % 3
        cx = c * CELL_SIZE + CELL_SIZE // 2
        cy = r * CELL_SIZE + CELL_SIZE // 2
        
        if board[i] == 'X':
            start_off = CELL_SIZE // 3
            pygame.draw.line(screen, X_COLOR, (cx - start_off, cy - start_off), (cx + start_off, cy + start_off), 12)
            pygame.draw.line(screen, X_COLOR, (cx + start_off, cy - start_off), (cx - start_off, cy + start_off), 12)
        else:
            pygame.draw.circle(screen, O_COLOR, (cx, cy), CELL_SIZE // 3, 10)

def draw_win_line(screen, line):
    if not line: return
    start_idx = line[0]
    end_idx = line[2]
    
    r1, c1 = start_idx // 3, start_idx % 3
    r2, c2 = end_idx // 3, end_idx % 3
    
    start_pos = (c1 * CELL_SIZE + CELL_SIZE//2, r1 * CELL_SIZE + CELL_SIZE//2)
    end_pos = (c2 * CELL_SIZE + CELL_SIZE//2, r2 * CELL_SIZE + CELL_SIZE//2)
    
    pygame.draw.line(screen, WIN_LINE_COLOR, start_pos, end_pos, 15)

# --- MAIN ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic-Tac-Toe AI")
    clock = pygame.time.Clock()
    game = Game()
    
    while True:
        clock.tick(30)
        screen.fill(BG_COLOR)
        
        # Draw UI
        pygame.draw.rect(screen, (30,30,40), (0, BOARD_SIZE, WIDTH, HEIGHT-BOARD_SIZE))
        score_text = f"YOU: {game.scores['X']}   AI: {game.scores['O']}"
        draw_text(screen, score_text, WIDTH//2, BOARD_SIZE + 20, 3, center=True)
        
        if game.winner:
            msg = "DRAW!" if game.winner == 'DRAW' else f"{game.winner} WINS!"
            draw_text(screen, msg, WIDTH//2, BOARD_SIZE + 60, 2, WIN_LINE_COLOR, center=True)
            draw_text(screen, "PRESS SPACE TO RESTART", WIDTH//2, BOARD_SIZE + 85, 1, (150,150,150), center=True)
        else:
            turn_msg = "YOUR TURN" if game.turn == 'X' else "AI THINKING..."
            draw_text(screen, turn_msg, WIDTH//2, BOARD_SIZE + 60, 2, (100,200,255), center=True)

        # Draw Game
        draw_grid(screen)
        draw_marks(screen, game.board)
        if game.winning_line:
            draw_win_line(screen, game.winning_line)
        
        # AI Logic
        if not game.winner and game.turn == 'O':
            if game.ai_timer > 0:
                game.ai_timer -= 1
            else:
                move = game.ai_move()
                game.make_move(move)

        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game.winner:
                    game.reset()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game.winner and game.turn == 'X':
                x, y = event.pos
                if y < BOARD_SIZE:
                    c = x // CELL_SIZE
                    r = y // CELL_SIZE
                    idx = r * 3 + c
                    game.make_move(idx)

        pygame.display.flip()

if __name__ == "__main__":
    main()
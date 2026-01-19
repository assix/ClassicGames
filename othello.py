import pygame
import sys
import copy
import random

# --- CONFIGURATION ---
WIDTH, HEIGHT = 600, 700
BOARD_SIZE = 600
GRID_SIZE = 8
CELL_SIZE = BOARD_SIZE // GRID_SIZE

# COLORS
BOARD_GREEN = (34, 139, 34)
GRID_LINE = (0, 0, 0)
BLACK_PIECE = (20, 20, 20)
WHITE_PIECE = (240, 240, 240)
HIGHLIGHT = (0, 0, 0, 50)     # Valid move dot
HINT_COLOR = (255, 215, 0)    # Gold for Hint
BG_COLOR = (40, 40, 50)
TEXT_COL = (255, 255, 255)

# STATES
EMPTY = 0
BLACK = 1
WHITE = 2

# --- PIXEL FONT ENGINE ---
PIXEL_FONT = {
    'A': [0x70, 0x88, 0x88, 0xF8, 0x88, 0x88, 0x88],
    'B': [0xF0, 0x88, 0x88, 0xF0, 0x88, 0x88, 0xF0],
    'C': [0x70, 0x88, 0x80, 0x80, 0x80, 0x88, 0x70],
    'D': [0xF0, 0x88, 0x88, 0x88, 0x88, 0x88, 0xF0],
    'E': [0xF8, 0x80, 0x80, 0xF0, 0x80, 0x80, 0xF8],
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
    ':': [0x00, 0x60, 0x60, 0x00, 0x60, 0x60, 0x00],
    '!': [0x20, 0x20, 0x20, 0x20, 0x00, 0x20, 0x00],
}

def draw_text(surface, text, x, y, scale=2, color=TEXT_COL, center=False):
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
                        pygame.draw.rect(surface, color, 
                                       (cursor_x + c * scale, y + r * scale, scale, scale))
        cursor_x += 6 * scale

# --- GAME LOGIC ---
class Board:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        mid = GRID_SIZE // 2
        self.grid[mid-1][mid-1] = WHITE
        self.grid[mid][mid] = WHITE
        self.grid[mid-1][mid] = BLACK
        self.grid[mid][mid-1] = BLACK
        self.turn = BLACK
        self.winner = None
        self.passes = 0
        self.history = [] # Stack for undo

    def save_state(self):
        # Deep copy the grid and state vars
        state = {
            'grid': [row[:] for row in self.grid],
            'turn': self.turn,
            'winner': self.winner,
            'passes': self.passes
        }
        self.history.append(state)

    def undo(self):
        if not self.history: return False
        
        # We usually want to undo 2 steps to get back to Player turn (AI moved, then Player moved)
        # But if history has 1 (rare), just pop 1
        steps = 2 if len(self.history) >= 2 else 1
        
        state = None
        for _ in range(steps):
            if self.history:
                state = self.history.pop()
        
        if state:
            self.grid = state['grid']
            self.turn = state['turn']
            self.winner = state['winner']
            self.passes = state['passes']
            return True
        return False

    def get_valid_moves(self, player):
        moves = []
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.is_valid_move(r, c, player): moves.append((r, c))
        return moves

    def is_valid_move(self, r, c, player):
        if self.grid[r][c] != EMPTY: return False
        opponent = WHITE if player == BLACK else BLACK
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            found_opponent = False
            while 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                if self.grid[nr][nc] == opponent: found_opponent = True
                elif self.grid[nr][nc] == player:
                    if found_opponent: return True
                    break
                else: break
                nr += dr
                nc += dc
        return False

    def make_move(self, r, c, player):
        if not self.is_valid_move(r, c, player): return False
        
        self.save_state() # SAVE BEFORE MODIFYING
        
        self.grid[r][c] = player
        opponent = WHITE if player == BLACK else BLACK
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            flip = []
            while 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                if self.grid[nr][nc] == opponent: flip.append((nr, nc))
                elif self.grid[nr][nc] == player:
                    if flip:
                        for fr, fc in flip: self.grid[fr][fc] = player
                    break
                else: break
                nr += dr
                nc += dc
        
        self.turn = opponent
        self.passes = 0
        return True

    def check_state(self):
        if not self.get_valid_moves(self.turn):
            self.turn = WHITE if self.turn == BLACK else BLACK
            self.passes += 1
            if self.passes >= 2 or not self.get_valid_moves(self.turn):
                self.end_game()

    def end_game(self):
        b, w = self.count_pieces()
        self.winner = "BLACK WINS" if b > w else "WHITE WINS" if w > b else "DRAW"

    def count_pieces(self):
        b = sum(r.count(BLACK) for r in self.grid)
        w = sum(r.count(WHITE) for r in self.grid)
        return b, w

# --- AI ---
class AI:
    def __init__(self, color):
        self.color = color

    def get_best_move(self, board, player_color=None, depth=3):
        # Allow calling for either AI color or providing a specific color (for hints)
        p_color = player_color if player_color else self.color
        
        moves = board.get_valid_moves(p_color)
        if not moves: return None
        
        best_val = -float('inf')
        best_move = random.choice(moves)
        
        for r, c in moves:
            temp = copy.deepcopy(board)
            temp.make_move(r, c, p_color)
            # Minimize opponent
            val = self.minimax(temp, depth-1, -float('inf'), float('inf'), False, p_color)
            if val > best_val:
                best_val = val
                best_move = (r, c)
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing, root_player):
        if depth == 0 or board.winner: return self.evaluate(board, root_player)
        
        curr_player = root_player if maximizing else (WHITE if root_player == BLACK else BLACK)
        moves = board.get_valid_moves(curr_player)
        
        if not moves: return self.minimax(board, depth-1, alpha, beta, not maximizing, root_player)

        if maximizing:
            max_eval = -float('inf')
            for r, c in moves:
                temp = copy.deepcopy(board)
                temp.make_move(r, c, curr_player)
                eval = self.minimax(temp, depth-1, alpha, beta, False, root_player)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha: break
            return max_eval
        else:
            min_eval = float('inf')
            for r, c in moves:
                temp = copy.deepcopy(board)
                temp.make_move(r, c, curr_player)
                eval = self.minimax(temp, depth-1, alpha, beta, True, root_player)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha: break
            return min_eval

    def evaluate(self, board, root_player):
        score = 0
        op = WHITE if root_player == BLACK else BLACK
        weights = [
            [100, -20, 10, 5, 5, 10, -20, 100],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [10, -2, 5, 1, 1, 5, -2, 10],
            [5, -2, 1, 1, 1, 1, -2, 5],
            [5, -2, 1, 1, 1, 1, -2, 5],
            [10, -2, 5, 1, 1, 5, -2, 10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [100, -20, 10, 5, 5, 10, -20, 100]
        ]
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if board.grid[r][c] == root_player: score += weights[r][c]
                elif board.grid[r][c] == op: score -= weights[r][c]
        return score

# --- MAIN ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Othello Pro")
    clock = pygame.time.Clock()
    
    board = Board()
    ai = AI(WHITE)
    hint_pos = None
    
    while True:
        clock.tick(30)
        
        # AI Turn
        if not board.winner and board.turn == ai.color:
            draw_game(screen, board, hint_pos)
            pygame.display.flip()
            pygame.time.wait(500)
            
            move = ai.get_best_move(board)
            if move: board.make_move(move[0], move[1], ai.color)
            else: board.check_state()
            board.check_state()
            hint_pos = None # Clear hint on turn change

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not board.winner and board.turn != ai.color:
                x, y = event.pos
                if y < BOARD_SIZE:
                    c = x // CELL_SIZE
                    r = y // CELL_SIZE
                    if board.make_move(r, c, BLACK):
                        board.check_state()
                        hint_pos = None # Clear hint on move
            
            if event.type == pygame.KEYDOWN:
                if board.winner and event.key == pygame.K_SPACE:
                    board = Board()
                    hint_pos = None
                
                if not board.winner:
                    # UNDO
                    if event.key == pygame.K_u:
                        if board.undo():
                            hint_pos = None
                    
                    # HINT
                    if event.key == pygame.K_h and board.turn == BLACK:
                        hint_pos = ai.get_best_move(board, player_color=BLACK, depth=3)

        draw_game(screen, board, hint_pos)
        pygame.display.flip()

def draw_game(screen, board, hint_pos):
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, BOARD_GREEN, (0, 0, WIDTH, BOARD_SIZE))
    
    # Grid
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, GRID_LINE, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)
        pygame.draw.line(screen, GRID_LINE, (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_SIZE), 2)
    
    # Pieces
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board.grid[r][c] != EMPTY:
                col = BLACK_PIECE if board.grid[r][c] == BLACK else WHITE_PIECE
                cx, cy = c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(screen, col, (cx, cy), CELL_SIZE // 2 - 4)
                pygame.draw.circle(screen, (100,100,100) if col==BLACK_PIECE else (200,200,200), (cx-2, cy-2), 5)

    # Hints & Valid Moves
    if board.turn == BLACK and not board.winner:
        # Valid moves (Gray Dots)
        for r, c in board.get_valid_moves(BLACK):
            s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(s, HIGHLIGHT, (CELL_SIZE//2, CELL_SIZE//2), 6)
            screen.blit(s, (c*CELL_SIZE, r*CELL_SIZE))
            
        # Best Move Hint (Gold Ring)
        if hint_pos:
            hr, hc = hint_pos
            cx, cy = hc * CELL_SIZE + CELL_SIZE // 2, hr * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, HINT_COLOR, (cx, cy), CELL_SIZE // 2 - 8, 4)

    # UI
    b, w = board.count_pieces()
    draw_text(screen, f"BLACK: {b}", 20, BOARD_SIZE + 20, 2)
    draw_text(screen, f"WHITE: {w}", 20, BOARD_SIZE + 50, 2)
    
    if board.winner:
        draw_text(screen, board.winner, WIDTH//2, BOARD_SIZE + 35, 3, (255, 215, 0), center=True)
        draw_text(screen, "SPACE TO RESTART", WIDTH//2, BOARD_SIZE + 70, 1, center=True)
    else:
        status = "YOUR TURN" if board.turn == BLACK else "AI THINKING"
        col = (100, 200, 255) if board.turn == BLACK else (200, 200, 200)
        draw_text(screen, status, WIDTH - 140, BOARD_SIZE + 25, 2, col)
        
        # Controls Legend
        draw_text(screen, "H: HINT   U: UNDO", WIDTH - 160, BOARD_SIZE + 60, 1, (180, 180, 180))

if __name__ == "__main__":
    main()
import pygame
import sys
import random

# --- CONFIGURATION ---
WIDTH, HEIGHT = 800, 300
CELL_SIZE = 100
COLS = 8
MARGIN_X = (WIDTH - (COLS * CELL_SIZE)) // 2
MARGIN_Y = (HEIGHT - CELL_SIZE) // 2

# COLORS
BG_COLOR = (30, 30, 35)
BOARD_WHITE = (220, 220, 220)
BOARD_BLACK = (60, 60, 70)
HIGHLIGHT = (100, 200, 255, 120)
SELECT_COL = (255, 215, 0, 100)
TEXT_COL = (255, 255, 255)

# PIECE COLORS
P_WHITE = (250, 250, 250)
P_WHITE_OUT = (20, 20, 20)
P_BLACK = (20, 20, 20)
P_BLACK_OUT = (200, 200, 200)

# PIECES
EMPTY = 0
W_KING = 1; W_ROOK = 2; W_KNIGHT = 3
B_KING = 4; B_ROOK = 5; B_KNIGHT = 6

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
    '!': [0x20, 0x20, 0x20, 0x20, 0x00, 0x00, 0x20],
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
                        pygame.draw.rect(surface, color, (cursor_x + c * scale, y + r * scale, scale, scale))
        cursor_x += 6 * scale

# --- GAME LOGIC ---
class OneDChess:
    def __init__(self):
        # Initial Setup: K R N . . n r k
        self.board = [W_KING, W_ROOK, W_KNIGHT, EMPTY, EMPTY, B_KNIGHT, B_ROOK, B_KING]
        self.turn = 'WHITE'
        self.winner = None

    def get_piece_owner(self, piece):
        if piece in [W_KING, W_ROOK, W_KNIGHT]: return 'WHITE'
        if piece in [B_KING, B_ROOK, B_KNIGHT]: return 'BLACK'
        return None

    def get_valid_moves(self, idx):
        moves = []
        p = self.board[idx]
        owner = self.get_piece_owner(p)
        dirs = [-1, 1]
        
        if p in [W_KNIGHT, B_KNIGHT]:
            for d in dirs:
                target = idx + (d * 2)
                if 0 <= target < COLS:
                    target_p = self.board[target]
                    if target_p == EMPTY or self.get_piece_owner(target_p) != owner:
                        moves.append(target)
                        
        elif p in [W_ROOK, B_ROOK]:
            for d in dirs:
                for i in range(1, COLS):
                    target = idx + (d * i)
                    if 0 <= target < COLS:
                        target_p = self.board[target]
                        if target_p == EMPTY:
                            moves.append(target)
                        elif self.get_piece_owner(target_p) != owner:
                            moves.append(target)
                            break 
                        else: break
                    else: break
                    
        elif p in [W_KING, B_KING]:
            for d in dirs:
                target = idx + d
                if 0 <= target < COLS:
                    target_p = self.board[target]
                    if target_p == EMPTY or self.get_piece_owner(target_p) != owner:
                        moves.append(target)
        return moves

    def make_move(self, start, end):
        target_p = self.board[end]
        if target_p == W_KING: self.winner = "BLACK WINS!"
        if target_p == B_KING: self.winner = "WHITE WINS!"
        
        self.board[end] = self.board[start]
        self.board[start] = EMPTY
        self.turn = 'BLACK' if self.turn == 'WHITE' else 'WHITE'

    def ai_move(self):
        my_pieces = [i for i, x in enumerate(self.board) if self.get_piece_owner(x) == 'BLACK']
        all_moves = []
        
        for idx in my_pieces:
            moves = self.get_valid_moves(idx)
            for m in moves:
                score = 0
                target = self.board[m]
                if target == W_KING: score = 100
                elif target != EMPTY: score = 10
                
                # Small bias to move forward (Left for Black)
                if m < idx: score += 1
                all_moves.append((score, idx, m))
        
        if all_moves:
            all_moves.sort(key=lambda x: x[0], reverse=True)
            best_score = all_moves[0][0]
            candidates = [m for m in all_moves if m[0] == best_score]
            choice = random.choice(candidates)
            self.make_move(choice[1], choice[2])

# --- HIGH QUALITY RENDERING ---
def draw_piece(screen, piece, x, y):
    cx = x + CELL_SIZE // 2
    cy = y + CELL_SIZE // 2
    
    # Determine Style
    if piece in [W_KING, W_ROOK, W_KNIGHT]:
        fill_col = P_WHITE
        line_col = P_WHITE_OUT
    else:
        fill_col = P_BLACK
        line_col = P_BLACK_OUT
    
    # Draw Shadow
    pygame.draw.ellipse(screen, (0,0,0,80), (cx-30, cy+25, 60, 15))

    # --- KING ---
    if piece in [W_KING, B_KING]:
        # Cross
        pygame.draw.rect(screen, fill_col, (cx-3, cy-35, 6, 15)) # Vert
        pygame.draw.rect(screen, fill_col, (cx-8, cy-30, 16, 6)) # Horz
        # Crown
        points = [(cx-15, cy-15), (cx-5, cy-15), (cx, cy-25), (cx+5, cy-15), (cx+15, cy-15), (cx+10, cy+10), (cx-10, cy+10)]
        pygame.draw.polygon(screen, fill_col, points)
        pygame.draw.polygon(screen, line_col, points, 2)
        # Base
        pygame.draw.rect(screen, fill_col, (cx-15, cy+10, 30, 15))
        pygame.draw.rect(screen, line_col, (cx-15, cy+10, 30, 15), 2)
        
    # --- ROOK ---
    elif piece in [W_ROOK, B_ROOK]:
        # Battlements
        pygame.draw.rect(screen, fill_col, (cx-15, cy-25, 8, 10))
        pygame.draw.rect(screen, fill_col, (cx-4, cy-25, 8, 10))
        pygame.draw.rect(screen, fill_col, (cx+7, cy-25, 8, 10))
        # Body
        pygame.draw.rect(screen, fill_col, (cx-12, cy-15, 24, 30))
        pygame.draw.rect(screen, line_col, (cx-12, cy-15, 24, 30), 2)
        # Base
        pygame.draw.rect(screen, fill_col, (cx-15, cy+15, 30, 10))
        pygame.draw.rect(screen, line_col, (cx-15, cy+15, 30, 10), 2)
        
        # Outline details
        pygame.draw.line(screen, line_col, (cx-15, cy-25), (cx-15, cy-15), 2)
        pygame.draw.line(screen, line_col, (cx+15, cy-25), (cx+15, cy-15), 2)
        pygame.draw.line(screen, line_col, (cx-15, cy-15), (cx+15, cy-15), 2)

    # --- KNIGHT ---
    elif piece in [W_KNIGHT, B_KNIGHT]:
        # Horse Head Profile (Vector points)
        # Facing Right if White, Left if Black? No, simpler to face center.
        facing = 1 if piece == W_KNIGHT else -1
        
        pts = [
            (cx + 5*facing, cy - 30), # Ear tip
            (cx + 10*facing, cy - 15), # Forehead
            (cx + 20*facing, cy - 5), # Nose
            (cx + 15*facing, cy + 5), # Jaw
            (cx + 10*facing, cy + 15), # Neck base front
            (cx - 15*facing, cy + 15), # Neck base back
            (cx - 10*facing, cy - 10), # Neck back
            (cx - 5*facing, cy - 25), # Ear base
        ]
        pygame.draw.polygon(screen, fill_col, pts)
        pygame.draw.polygon(screen, line_col, pts, 2)
        
        # Base
        pygame.draw.rect(screen, fill_col, (cx-15, cy+15, 30, 10))
        pygame.draw.rect(screen, line_col, (cx-15, cy+15, 30, 10), 2)
        
        # Eye
        pygame.draw.circle(screen, line_col, (cx + 5*facing, cy-10), 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("1D Chess (HD)")
    clock = pygame.time.Clock()
    
    game = OneDChess()
    selected = None
    
    while True:
        clock.tick(30)
        screen.fill(BG_COLOR)
        
        # --- INPUT ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game.winner:
                if game.turn == 'WHITE':
                    mx, my = event.pos
                    if MARGIN_Y <= my <= MARGIN_Y + CELL_SIZE:
                        col = (mx - MARGIN_X) // CELL_SIZE
                        if 0 <= col < COLS:
                            if selected is None:
                                p = game.board[col]
                                if game.get_piece_owner(p) == 'WHITE': selected = col
                            else:
                                moves = game.get_valid_moves(selected)
                                if col in moves:
                                    game.make_move(selected, col)
                                    selected = None
                                    if not game.winner:
                                        pygame.time.set_timer(pygame.USEREVENT, 1000)
                                else:
                                    p = game.board[col]
                                    if game.get_piece_owner(p) == 'WHITE': selected = col
                                    else: selected = None

            if event.type == pygame.USEREVENT and not game.winner:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                game.ai_move()

            if event.type == pygame.KEYDOWN and game.winner:
                 if event.key == pygame.K_SPACE:
                     game = OneDChess()
                     selected = None

        # --- DRAWING ---
        
        # Board Background
        board_rect = (MARGIN_X - 10, MARGIN_Y - 10, COLS * CELL_SIZE + 20, CELL_SIZE + 20)
        pygame.draw.rect(screen, (80, 50, 20), board_rect) # Wood Frame
        pygame.draw.rect(screen, (60, 40, 15), board_rect, 4)

        for i in range(COLS):
            x = MARGIN_X + i * CELL_SIZE
            color = BOARD_WHITE if i % 2 == 0 else BOARD_BLACK
            
            # Cell
            pygame.draw.rect(screen, color, (x, MARGIN_Y, CELL_SIZE, CELL_SIZE))
            
            # Highlight
            if selected == i:
                s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                s.fill(SELECT_COL)
                screen.blit(s, (x, MARGIN_Y))
            
            if selected is not None and i in game.get_valid_moves(selected):
                s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                s.fill(HIGHLIGHT)
                screen.blit(s, (x, MARGIN_Y))
                # Small marker
                pygame.draw.circle(screen, (0, 180, 0), (x+CELL_SIZE//2, MARGIN_Y+CELL_SIZE//2), 6)

            # Piece
            if game.board[i] != EMPTY:
                draw_piece(screen, game.board[i], x, MARGIN_Y)

        # UI
        if game.winner:
            draw_text(screen, game.winner, WIDTH//2, 50, 3, (255, 215, 0), center=True)
            draw_text(screen, "SPACE TO RESTART", WIDTH//2, 250, 2, center=True)
        else:
            turn_txt = "YOUR TURN" if game.turn == 'WHITE' else "AI THINKING..."
            color = (100, 200, 255) if game.turn == 'WHITE' else (255, 100, 100)
            draw_text(screen, turn_txt, WIDTH//2, 50, 2, color, center=True)
            
            # Tutorial Legend
            draw_text(screen, "KING[1]   ROOK[SLIDE]   KNIGHT[JUMP]", WIDTH//2, 260, 1, (150, 150, 150), center=True)

        pygame.display.flip()

if __name__ == "__main__":
    main()
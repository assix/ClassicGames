import pygame
import sys
import copy
import random

# --- CONFIGURATION ---
WIDTH, HEIGHT = 800, 800
BOARD_SIZE = 800
SQUARE_SIZE = BOARD_SIZE // 8

# COLORS
WHITE_PIECE = (245, 245, 245)
BLACK_PIECE = (40, 40, 40)
PIECE_BORDER = (20, 20, 20)
WHITE_BORDER = (150, 150, 150)

LIGHT_SQUARE = (235, 236, 208)
DARK_SQUARE = (119, 149, 86)   
HIGHLIGHT = (186, 202, 68)     
MOVE_HINT = (50, 50, 50, 60)   
CHECK_RED = (255, 80, 80)      
OVERLAY_BG = (0, 0, 0, 180)    
TEXT_COL = (255, 255, 255)

# PIECE CONSTANTS
EMPTY = 0
W_PAWN = 1; W_KNIGHT = 2; W_BISHOP = 3; W_ROOK = 4; W_QUEEN = 5; W_KING = 6
B_PAWN = 7; B_KNIGHT = 8; B_BISHOP = 9; B_ROOK = 10; B_QUEEN = 11; B_KING = 12

# --- PIXEL FONT ENGINE (Crash-Proof) ---
PIXEL_FONT = {
    'A': [0x70, 0x88, 0x88, 0xF8, 0x88, 0x88, 0x88],
    'B': [0xF0, 0x88, 0x88, 0xF0, 0x88, 0x88, 0xF0],
    'C': [0x70, 0x88, 0x80, 0x80, 0x80, 0x88, 0x70],
    'D': [0xF0, 0x88, 0x88, 0x88, 0x88, 0x88, 0xF0],
    'E': [0xF8, 0x80, 0x80, 0xF0, 0x80, 0x80, 0xF8],
    'F': [0xF8, 0x80, 0x80, 0xF0, 0x80, 0x80, 0x80],
    'G': [0x78, 0x80, 0x80, 0x98, 0x88, 0x88, 0x70],
    'H': [0x88, 0x88, 0x88, 0xF8, 0x88, 0x88, 0x88],
    'I': [0x70, 0x20, 0x20, 0x20, 0x20, 0x20, 0x70],
    'J': [0x08, 0x08, 0x08, 0x08, 0x08, 0x88, 0x70],
    'K': [0x88, 0x90, 0xA0, 0xC0, 0xA0, 0x90, 0x88],
    'L': [0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0xF8],
    'M': [0x88, 0xD8, 0xA8, 0xA8, 0x88, 0x88, 0x88],
    'N': [0x88, 0xC8, 0xA8, 0x98, 0x88, 0x88, 0x88],
    'O': [0x70, 0x88, 0x88, 0x88, 0x88, 0x88, 0x70],
    'P': [0xF0, 0x88, 0x88, 0xF0, 0x80, 0x80, 0x80],
    'Q': [0x70, 0x88, 0x88, 0x88, 0xA8, 0x90, 0x68],
    'R': [0xF0, 0x88, 0x88, 0xF0, 0xA0, 0x90, 0x88],
    'S': [0x70, 0x88, 0x80, 0x70, 0x08, 0x88, 0x70],
    'T': [0xF8, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20],
    'U': [0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x70],
    'V': [0x88, 0x88, 0x88, 0x88, 0x88, 0x50, 0x20],
    'W': [0x88, 0x88, 0x88, 0xA8, 0xA8, 0xD8, 0x88],
    'X': [0x88, 0x88, 0x50, 0x20, 0x50, 0x88, 0x88],
    'Y': [0x88, 0x88, 0x50, 0x20, 0x20, 0x20, 0x20],
    'Z': [0xF8, 0x08, 0x10, 0x20, 0x40, 0x80, 0xF8],
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
    '/': [0x08, 0x10, 0x20, 0x40, 0x80, 0x00, 0x00],
    '|': [0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20]
}

def draw_text(surface, text, x, y, scale=2, color=TEXT_COL, center=False):
    text = str(text).upper()
    width = len(text) * 6 * scale
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

# --- CHESS LOGIC ---
class Board:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [
            [B_ROOK, B_KNIGHT, B_BISHOP, B_QUEEN, B_KING, B_BISHOP, B_KNIGHT, B_ROOK],
            [B_PAWN] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [W_PAWN] * 8,
            [W_ROOK, W_KNIGHT, W_BISHOP, W_QUEEN, W_KING, W_BISHOP, W_KNIGHT, W_ROOK]
        ]
        self.turn = 'white'
        self.castling_rights = [True, True, True, True]
        self.en_passant_target = None
        self.winner = None
        self.history = []

    def save_state(self):
        state = ([row[:] for row in self.board], self.turn, self.castling_rights[:], self.en_passant_target, self.winner)
        self.history.append(state)

    def undo(self):
        if len(self.history) >= 2:
            self.history.pop() # Pop AI
            prev = self.history.pop() # Pop Player
            self.restore_state(prev)
            return True
        elif len(self.history) == 1:
             prev = self.history.pop()
             self.restore_state(prev)
             return True
        return False

    def restore_state(self, state):
        self.board, self.turn, self.castling_rights, self.en_passant_target, self.winner = state
        self.board = [row[:] for row in self.board]
        self.castling_rights = self.castling_rights[:]

    def get_piece(self, r, c):
        if 0 <= r < 8 and 0 <= c < 8: return self.board[r][c]
        return None

    def is_white(self, piece): return 1 <= piece <= 6
    def is_black(self, piece): return 7 <= piece <= 12

    def get_valid_moves(self, piece, r, c, check_check=True):
        moves = []
        is_w = self.is_white(piece)
        
        def add(nr, nc):
            target = self.get_piece(nr, nc)
            if target is None: return False
            is_capture = False
            if target != EMPTY:
                if is_w and self.is_white(target): return False
                if not is_w and self.is_black(target): return False
                is_capture = True
            
            if check_check:
                if self.simulate_move(r, c, nr, nc): moves.append((nr, nc))
            else:
                moves.append((nr, nc))
            return not is_capture

        if piece in (W_PAWN, B_PAWN):
            d = -1 if is_w else 1
            start = 6 if is_w else 1
            if self.get_piece(r+d, c) == EMPTY:
                if not check_check or self.simulate_move(r, c, r+d, c): moves.append((r+d, c))
                if r == start and self.get_piece(r+d*2, c) == EMPTY:
                    if not check_check or self.simulate_move(r, c, r+d*2, c): moves.append((r+d*2, c))
            for dc in [-1, 1]:
                t = self.get_piece(r+d, c+dc)
                if t and t != EMPTY and ((is_w and self.is_black(t)) or (not is_w and self.is_white(t))):
                    if not check_check or self.simulate_move(r, c, r+d, c+dc): moves.append((r+d, c+dc))
                if self.en_passant_target == (r+d, c+dc):
                    if not check_check or self.simulate_move(r, c, r+d, c+dc): moves.append((r+d, c+dc))

        elif piece in (W_KNIGHT, B_KNIGHT):
            for dr, dc in [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]: add(r+dr, c+dc)

        elif piece in (W_BISHOP, B_BISHOP, W_ROOK, B_ROOK, W_QUEEN, B_QUEEN):
            dirs = []
            if piece not in (W_ROOK, B_ROOK): dirs.extend([(1,1), (1,-1), (-1,1), (-1,-1)])
            if piece not in (W_BISHOP, B_BISHOP): dirs.extend([(1,0), (-1,0), (0,1), (0,-1)])
            for dr, dc in dirs:
                for i in range(1, 8):
                    if not add(r+dr*i, c+dc*i): break

        elif piece in (W_KING, B_KING):
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr==0 and dc==0: continue
                    add(r+dr, c+dc)
            if check_check and not self.is_in_check(is_w):
                row = 7 if is_w else 0
                idx = 0 if is_w else 2
                if self.castling_rights[idx] and self.get_piece(row, 5)==EMPTY and self.get_piece(row, 6)==EMPTY:
                    moves.append((row, 6))
                if self.castling_rights[idx+1] and self.get_piece(row, 1)==EMPTY and self.get_piece(row, 2)==EMPTY and self.get_piece(row, 3)==EMPTY:
                    moves.append((row, 2))
        return moves

    def find_king(self, is_white):
        t = W_KING if is_white else B_KING
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == t: return r, c
        return None

    def is_in_check(self, is_white):
        kp = self.find_king(is_white)
        if not kp: return True
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p != EMPTY and ((is_white and self.is_black(p)) or (not is_white and self.is_white(p))):
                    if kp in self.get_valid_moves(p, r, c, False): return True
        return False

    def simulate_move(self, r1, c1, r2, c2):
        save_board = [row[:] for row in self.board]
        save_ep = self.en_passant_target
        self.move_piece_internal(r1, c1, r2, c2)
        safe = not self.is_in_check(self.is_white(save_board[r1][c1]))
        self.board = save_board
        self.en_passant_target = save_ep
        return safe

    def move_piece_internal(self, r1, c1, r2, c2):
        p = self.board[r1][c1]
        self.board[r2][c2] = p
        self.board[r1][c1] = EMPTY
        if (p in (W_PAWN, B_PAWN)) and (r2, c2) == self.en_passant_target: self.board[r1][c2] = EMPTY
        self.en_passant_target = None
        if (p in (W_PAWN, B_PAWN)) and abs(r2-r1) == 2: self.en_passant_target = ((r1+r2)//2, c1)
        if p == W_PAWN and r2 == 0: self.board[r2][c2] = W_QUEEN
        if p == B_PAWN and r2 == 7: self.board[r2][c2] = B_QUEEN
        if p == W_KING:
            self.castling_rights[0] = self.castling_rights[1] = False
            if c2-c1 == 2: self.board[7][5], self.board[7][7] = self.board[7][7], EMPTY
            elif c2-c1 == -2: self.board[7][3], self.board[7][0] = self.board[7][0], EMPTY
        if p == B_KING:
            self.castling_rights[2] = self.castling_rights[3] = False
            if c2-c1 == 2: self.board[0][5], self.board[0][7] = self.board[0][7], EMPTY
            elif c2-c1 == -2: self.board[0][3], self.board[0][0] = self.board[0][0], EMPTY
        if p == W_ROOK:
            if r1==7 and c1==0: self.castling_rights[1] = False
            if r1==7 and c1==7: self.castling_rights[0] = False
        if p == B_ROOK:
            if r1==0 and c1==0: self.castling_rights[3] = False
            if r1==0 and c1==7: self.castling_rights[2] = False

    def make_move(self, r1, c1, r2, c2):
        if self.simulate_move(r1, c1, r2, c2):
            self.save_state()
            self.move_piece_internal(r1, c1, r2, c2)
            self.turn = 'black' if self.turn == 'white' else 'white'
            has_moves = False
            is_w = (self.turn == 'white')
            for r in range(8):
                for c in range(8):
                    p = self.board[r][c]
                    if p!=EMPTY and ((is_w and self.is_white(p)) or (not is_w and self.is_black(p))):
                        if self.get_valid_moves(p, r, c): has_moves = True; break
            if not has_moves:
                self.winner = 'black' if self.is_in_check(is_w) else 'draw' if is_w else 'white'
                if not is_w and not self.is_in_check(False): self.winner = 'draw'
            return True
        return False

    def get_all_moves(self, is_white):
        moves = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p!=EMPTY and ((is_white and self.is_white(p)) or (not is_white and self.is_black(p))):
                    for m in self.get_valid_moves(p, r, c): moves.append(((r,c), m))
        return moves

# --- AI ---
class AI:
    def __init__(self):
        self.values = {EMPTY:0, W_PAWN:10, W_KNIGHT:30, W_BISHOP:30, W_ROOK:50, W_QUEEN:90, W_KING:900,
                       B_PAWN:-10, B_KNIGHT:-30, B_BISHOP:-30, B_ROOK:-50, B_QUEEN:-90, B_KING:-900}
    
    def evaluate(self, board): return sum(self.values.get(c, 0) for row in board.board for c in row)

    def get_best_move(self, board, depth=2):
        moves = board.get_all_moves(False)
        if not moves: return None
        best, best_move = 99999, random.choice(moves)
        for s, e in moves:
            tmp = copy.deepcopy(board)
            tmp.make_move(s[0], s[1], e[0], e[1])
            val = self.minimax(tmp, depth-1, -10000, 10000, True)
            if val < best: best, best_move = val, (s, e)
        return best_move

    def minimax(self, board, depth, alpha, beta, is_max):
        if depth == 0 or board.winner: return self.evaluate(board)
        moves = board.get_all_moves(is_max)
        if not moves: return self.evaluate(board)
        if is_max:
            val = -99999
            for s, e in moves:
                tmp = copy.deepcopy(board)
                tmp.make_move(s[0], s[1], e[0], e[1])
                val = max(val, self.minimax(tmp, depth-1, alpha, beta, False))
                alpha = max(alpha, val)
                if beta <= alpha: break
            return val
        else:
            val = 99999
            for s, e in moves:
                tmp = copy.deepcopy(board)
                tmp.make_move(s[0], s[1], e[0], e[1])
                val = min(val, self.minimax(tmp, depth-1, alpha, beta, True))
                beta = min(beta, val)
                if beta <= alpha: break
            return val

# --- GRAPHICS ---
def draw_piece(surface, piece, cx, cy, s):
    is_w = 1 <= piece <= 6
    fill = WHITE_PIECE if is_w else BLACK_PIECE
    border = PIECE_BORDER if is_w else WHITE_BORDER
    pt = piece if is_w else piece - 6
    def poly(pts):
        scaled = [(cx + x*s, cy + y*s) for x, y in pts]
        pygame.draw.polygon(surface, fill, scaled)
        pygame.draw.polygon(surface, border, scaled, 2)
    def ellipse(x, y, w, h):
        rect = pygame.Rect(cx + x*s, cy + y*s, w*s, h*s)
        pygame.draw.ellipse(surface, fill, rect)
        pygame.draw.ellipse(surface, border, rect, 2)

    if pt == 1: # Pawn
        ellipse(-0.15, -0.35, 0.3, 0.3)
        poly([(-0.15, 0.2), (0.15, 0.2), (0.05, -0.2), (-0.05, -0.2)])
        ellipse(-0.25, 0.2, 0.5, 0.25)
    elif pt == 2: # Knight
        poly([(-0.2, 0.4), (0.2, 0.4), (0.25, 0.2), (0.15, -0.1), (0.25, -0.25), (0.1, -0.4), (-0.15, -0.3), (-0.25, -0.1), (-0.2, 0.1)])
        poly([(0.05, -0.4), (0.15, -0.3), (0.12, -0.2)])
    elif pt == 3: # Bishop
        poly([(-0.15, 0.3), (0.15, 0.3), (0.2, 0), (0, -0.4), (-0.2, 0)])
        ellipse(-0.2, 0.25, 0.4, 0.15)
        ellipse(-0.05, -0.48, 0.1, 0.1)
        pygame.draw.line(surface, border, (cx-0.05*s, cy-0.2*s), (cx+0.05*s, cy-0.05*s), 2)
    elif pt == 4: # Rook
        poly([(-0.2, 0.35), (0.2, 0.35), (0.2, -0.2), (-0.2, -0.2)])
        ellipse(-0.25, 0.3, 0.5, 0.15)
        poly([(-0.25, -0.2), (0.25, -0.2), (0.25, -0.4), (-0.25, -0.4)])
        pygame.draw.rect(surface, fill, (cx-0.08*s, cy-0.42*s, 0.16*s, 0.1*s)) 
    elif pt == 5: # Queen
        poly([(-0.2, 0.4), (0.2, 0.4), (0.15, 0), (0.3, -0.3), (0.1, -0.15), (0, -0.4), (-0.1, -0.15), (-0.3, -0.3), (-0.15, 0)])
        circ_pts = [(-0.3,-0.3), (0,-0.4), (0.3,-0.3)]
        for px, py in circ_pts: ellipse(px-0.04, py-0.04, 0.08, 0.08)
    elif pt == 6: # King
        poly([(-0.2, 0.4), (0.2, 0.4), (0.2, -0.1), (-0.2, -0.1)])
        ellipse(-0.2, 0.3, 0.4, 0.15)
        pygame.draw.rect(surface, fill, (cx-0.05*s, cy-0.4*s, 0.1*s, 0.3*s))
        pygame.draw.rect(surface, border, (cx-0.05*s, cy-0.4*s, 0.1*s, 0.3*s), 2)
        pygame.draw.rect(surface, fill, (cx-0.12*s, cy-0.3*s, 0.24*s, 0.08*s))
        pygame.draw.rect(surface, border, (cx-0.12*s, cy-0.3*s, 0.24*s, 0.08*s), 2)

def draw_board(screen, board, selected, moves):
    for r in range(8):
        for c in range(8):
            col = LIGHT_SQUARE if (r+c)%2==0 else DARK_SQUARE
            if selected == (r,c): col = HIGHLIGHT
            p = board.board[r][c]
            if p in (W_KING, B_KING):
                if board.is_in_check(p==W_KING): col = CHECK_RED
            
            pygame.draw.rect(screen, col, (c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            # Coords via Pixel Text
            if c==0: draw_text(screen, str(8-r), 2, r*SQUARE_SIZE+2, 1, DARK_SQUARE if (r+c)%2==0 else LIGHT_SQUARE)
            if r==7: draw_text(screen, chr(97+c), c*SQUARE_SIZE+SQUARE_SIZE-10, HEIGHT-10, 1, DARK_SQUARE if (r+c)%2==0 else LIGHT_SQUARE)

            if (r,c) in moves:
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(s, MOVE_HINT, (SQUARE_SIZE//2, SQUARE_SIZE//2), 14)
                screen.blit(s, (c*SQUARE_SIZE, r*SQUARE_SIZE))

            if p != EMPTY:
                draw_piece(screen, p, c*SQUARE_SIZE + SQUARE_SIZE//2, r*SQUARE_SIZE + SQUARE_SIZE//2, SQUARE_SIZE)

def draw_game_over(screen, winner):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(OVERLAY_BG)
    screen.blit(overlay, (0,0))
    text = "DRAW" if winner == 'draw' else f"{winner} WINS"
    draw_text(screen, text, WIDTH//2, HEIGHT//2 - 20, 5, center=True)
    draw_text(screen, "PRESS R TO RESTART OR U TO UNDO", WIDTH//2, HEIGHT//2 + 50, 2, center=True)

# --- MAIN ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Pro - 'U' to Undo")
    clock = pygame.time.Clock()
    
    board = Board()
    ai = AI()
    selected = None
    moves = []
    
    while True:
        clock.tick(30)
        if not board.winner and board.turn == 'black':
            draw_board(screen, board, selected, moves)
            pygame.display.flip()
            move = ai.get_best_move(board)
            if move: board.make_move(move[0][0], move[0][1], move[1][0], move[1][1])
            else: board.winner = 'white' if not board.winner else board.winner

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: board.reset(); selected = None; moves = []
                if event.key == pygame.K_u:
                    if board.undo(): selected = None; moves = []; board.winner = None

            if event.type == pygame.MOUSEBUTTONDOWN and not board.winner and board.turn == 'white':
                c = event.pos[0] // SQUARE_SIZE
                r = event.pos[1] // SQUARE_SIZE
                if selected:
                    if (r,c) in moves:
                        board.make_move(selected[0], selected[1], r, c)
                        selected = None; moves = []
                    else:
                        p = board.get_piece(r, c)
                        if p and board.is_white(p): selected = (r,c); moves = board.get_valid_moves(p, r, c)
                        else: selected = None; moves = []
                else:
                    p = board.get_piece(r, c)
                    if p and board.is_white(p): selected = (r,c); moves = board.get_valid_moves(p, r, c)

        draw_board(screen, board, selected, moves)
        if board.winner: draw_game_over(screen, board.winner)
        pygame.display.flip()

if __name__ == "__main__":
    main()
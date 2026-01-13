import pygame
import random
import sys
import copy

# --- SETUP ---
pygame.init()
WIDTH, HEIGHT = 900, 700
SIDE_PANEL = 150
BOARD_WIDTH = WIDTH - SIDE_PANEL
HEIGHT_PAD = 50
PLAY_AREA_H = HEIGHT - HEIGHT_PAD * 2

# Colors
BROWN_DARK = (80, 40, 0)
BROWN_LIGHT = (140, 90, 40)
CREAM = (240, 230, 200)
RED_CHK = (200, 20, 20)
WHITE_CHK = (240, 240, 240)
BLACK = (0, 0, 0)
GREEN_FELT = (0, 80, 0)
HIGHLIGHT = (100, 255, 100)
BAR_COLOR = (40, 20, 0)

# Constants
WHITE = 1
RED = -1
EMPTY = 0

# --- PIXEL FONT ENGINE (5x7) ---
PIXEL_FONT_5x7 = {
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
    'V': [0x88, 0x88, 0x88, 0x88, 0x88, 0x50, 0x20], # Fixed V
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
}

def draw_pixel_char(surface, char, x, y, scale=2, color=BLACK):
    char = char.upper()
    if char not in PIXEL_FONT_5x7: char = ' '
    rows = PIXEL_FONT_5x7[char]
    for r_idx, row_val in enumerate(rows):
        for c_idx in range(5):
            if (row_val >> (7 - c_idx)) & 1:
                pygame.draw.rect(surface, color, (x + c_idx * scale, y + r_idx * scale, scale, scale))

def draw_pixel_string(surface, text, x, y, scale=2, color=BLACK):
    cursor_x = x
    for char in str(text).upper():
        draw_pixel_char(surface, char, cursor_x, y, scale, color)
        cursor_x += (6 * scale)

# --- BOARD LOGIC ---
class Board:
    def __init__(self):
        # 24 Points. Index 0 is White's Home, 23 is Red's Home
        # Format: [Color, Count]
        self.points = [[0, 0] for _ in range(24)]
        self.bar = {WHITE: 0, RED: 0}
        self.off = {WHITE: 0, RED: 0}
        self.setup_board()

    def setup_board(self):
        # Standard Setup
        self.points[0] = [WHITE, 2]   # 2 White on 1
        self.points[5] = [RED, 5]     # 5 Red on 6
        self.points[7] = [RED, 3]     # 3 Red on 8
        self.points[11] = [WHITE, 5]  # 5 White on 12
        self.points[12] = [RED, 5]    # 5 Red on 13
        self.points[16] = [WHITE, 3]  # 3 White on 17
        self.points[18] = [WHITE, 5]  # 5 White on 19
        self.points[23] = [RED, 2]    # 2 Red on 24

    def is_valid_move(self, start, end, color):
        if end < 0 or end > 23: return False
        dest_color, dest_count = self.points[end]
        if dest_count > 1 and dest_color != color:
            return False # Blocked
        return True

    def move_piece(self, start, end, color):
        # Handle Bar Move
        if start == 'BAR':
            self.bar[color] -= 1
        else:
            self.points[start][1] -= 1
            if self.points[start][1] == 0: self.points[start][0] = 0

        # Handle Bear Off
        if end == 'OFF':
            self.off[color] += 1
            return

        # Handle Destination
        dest_color, dest_count = self.points[end]
        
        # Hit Logic
        if dest_count == 1 and dest_color != color:
            self.points[end] = [color, 1]
            self.bar[dest_color] += 1 # Send opponent to bar
        elif dest_count == 0:
            self.points[end] = [color, 1]
        else:
            self.points[end][1] += 1

    def can_bear_off(self, color):
        if self.bar[color] > 0: return False
        
        # Check if all pieces are in home quadrant
        start, end = (0, 17) if color == WHITE else (6, 23)
        for i in range(start, end + 1):
            c, count = self.points[i]
            if c == color and count > 0:
                return False
        return True

    def get_valid_moves(self, dice, color):
        moves = [] # (start_idx, end_idx, die_used)
        unique_dice = set(dice)
        
        # 1. Must move from Bar if possible
        if self.bar[color] > 0:
            for die in unique_dice:
                target = -1
                if color == WHITE: target = -1 + die
                else: target = 24 - die 
                
                if 0 <= target <= 23:
                    c, count = self.points[target]
                    if count <= 1 or c == color:
                        moves.append(('BAR', target, die))
            return moves

        # 2. Regular Moves
        bear_off_allowed = self.can_bear_off(color)
        
        for i in range(24):
            c, count = self.points[i]
            if c != color or count == 0: continue
            
            for die in unique_dice:
                target = i + die if color == WHITE else i - die
                
                # Check Bearing Off
                if (color == WHITE and target > 23) or (color == RED and target < 0):
                    if bear_off_allowed:
                        if (color == WHITE and target == 24) or (color == RED and target == -1):
                            moves.append((i, 'OFF', die))
                        else:
                            # Allow if no pieces further away
                            furthest = True
                            if color == WHITE:
                                for back in range(18, i):
                                    if self.points[back][0] == WHITE and self.points[back][1] > 0: furthest = False
                            else:
                                for back in range(i + 1, 6):
                                    if self.points[back][0] == RED and self.points[back][1] > 0: furthest = False
                            
                            if furthest:
                                moves.append((i, 'OFF', die))

                # Normal Move
                elif 0 <= target <= 23:
                    t_c, t_count = self.points[target]
                    if t_count <= 1 or t_c == color:
                        moves.append((i, target, die))
                        
        return moves

# --- AI AGENT ---
class AI:
    def __init__(self, color):
        self.color = color

    def get_move(self, board, dice):
        moves = board.get_valid_moves(dice, self.color)
        if not moves: return None
        
        # Heuristic Scoring
        best_score = -9999
        best_move = None
        
        for move in moves:
            start, end, die = move
            score = 0
            
            # 1. Priority: Hit opponent
            if end != 'OFF' and end != 'BAR':
                c, count = board.points[end]
                if count == 1 and c != self.color:
                    score += 50
            
            # 2. Priority: Bear Off
            if end == 'OFF':
                score += 100
            
            # 3. Priority: Secure a point (make size 2)
            if end != 'OFF' and end != 'BAR':
                c, count = board.points[end]
                if c == self.color and count == 1:
                    score += 20
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move

# --- GRAPHICS ---
def draw_board(win, board, selected_idx, valid_targets):
    win.fill(BROWN_DARK)
    pygame.draw.rect(win, BROWN_LIGHT, (0, HEIGHT_PAD, BOARD_WIDTH, PLAY_AREA_H))
    
    # Draw Bar
    bar_x = BOARD_WIDTH // 2
    pygame.draw.rect(win, BAR_COLOR, (bar_x - 15, HEIGHT_PAD, 30, PLAY_AREA_H))
    
    # Draw Triangles
    tri_w = (BOARD_WIDTH - 30) // 12
    tri_h = PLAY_AREA_H // 2 - 20
    
    for i in range(24):
        is_top = 12 <= i <= 23
        if is_top:
            pos_idx = i - 12
        else:
            pos_idx = 11 - i 
        
        gap = 0
        if pos_idx >= 6: gap = 30
        
        x_base = pos_idx * tri_w + gap
        y_base = HEIGHT_PAD if is_top else HEIGHT - HEIGHT_PAD
        point_dir = 1 if is_top else -1
        
        color = CREAM if i % 2 == 0 else BROWN_DARK
        pts = [
            (x_base, y_base),
            (x_base + tri_w, y_base),
            (x_base + tri_w // 2, y_base + tri_h * point_dir)
        ]
        pygame.draw.polygon(win, color, pts)
        
        # Highlight Valid Target
        if i in valid_targets:
            pygame.draw.circle(win, HIGHLIGHT, (x_base + tri_w//2, y_base + tri_h//2 * point_dir), 10)
        
        # Highlight Selected
        if i == selected_idx:
            pygame.draw.rect(win, HIGHLIGHT, (x_base, y_base if is_top else y_base - 10, tri_w, 10))

        # Draw Checkers
        c, count = board.points[i]
        if count > 0:
            chk_color = WHITE_CHK if c == WHITE else RED_CHK
            cx = x_base + tri_w // 2
            cy_start = y_base + (25 * point_dir)
            
            limit = 5
            drawn = min(count, limit)
            for k in range(drawn):
                cy = cy_start + (k * 40 * point_dir)
                pygame.draw.circle(win, chk_color, (cx, cy), 18)
                pygame.draw.circle(win, BLACK, (cx, cy), 18, 1)
                
            if count > limit:
                draw_pixel_string(win, str(count), cx - 6, cy_start + ((limit-1)*40*point_dir) - 5, 2, BLACK)

    # Draw Bar Checkers
    if board.bar[WHITE] > 0:
        for k in range(board.bar[WHITE]):
            pygame.draw.circle(win, WHITE_CHK, (bar_x, HEIGHT//2 - 40 - k*10), 18)
    if board.bar[RED] > 0:
        for k in range(board.bar[RED]):
            pygame.draw.circle(win, RED_CHK, (bar_x, HEIGHT//2 + 40 + k*10), 18)
            
    # Draw Off Pieces
    draw_pixel_string(win, "OFF", WIDTH - 100, 50, 2, WHITE_CHK)
    draw_pixel_string(win, f"W:{board.off[WHITE]}", WIDTH - 120, 100, 2, WHITE_CHK)
    draw_pixel_string(win, f"R:{board.off[RED]}", WIDTH - 120, HEIGHT - 100, 2, RED_CHK)

def draw_dice(win, dice, turn):
    y = HEIGHT // 2
    x = WIDTH - 100
    color = WHITE_CHK if turn == WHITE else RED_CHK
    
    for i, d in enumerate(dice):
        pygame.draw.rect(win, color, (x, y - 40 + i*50, 40, 40), border_radius=5)
        draw_pixel_string(win, str(d), x + 12, y - 30 + i*50, 2, BLACK)

# --- GAME CONTROLLER ---
def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Backgammon vs AI")
    clock = pygame.time.Clock()
    
    board = Board()
    ai = AI(WHITE) 
    
    turn = RED 
    dice = []
    selected_idx = None
    valid_targets = []
    message = "SPACE TO ROLL"
    
    run = True
    while run:
        clock.tick(30)
        
        if turn == WHITE and dice:
            pygame.time.wait(500)
            move = ai.get_move(board, dice)
            if move:
                start, end, die = move
                board.move_piece(start, end, WHITE)
                dice.remove(die)
                if not dice:
                    turn = RED
                    message = "YOUR TURN"
            else:
                turn = RED
                dice = []
                message = "AI STUCK YOUR TURN"
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not dice:
                    d1, d2 = random.randint(1,6), random.randint(1,6)
                    dice = [d1, d2]
                    if d1 == d2: dice = [d1, d1, d1, d1]
                    message = "MOVE PIECES"
                    
                    if not board.get_valid_moves(dice, turn):
                        message = "NO MOVES"
                        dice = []
                        turn = -turn

            if event.type == pygame.MOUSEBUTTONDOWN and turn == RED:
                x, y = event.pos
                clicked_idx = None
                
                # Check Bar
                if WIDTH//2 - 15 <= x <= WIDTH//2 + 15:
                     if board.bar[RED] > 0: clicked_idx = 'BAR'

                # Check Points
                tri_w = (BOARD_WIDTH - 30) // 12
                if clicked_idx is None:
                    for i in range(24):
                        is_top = 12 <= i <= 23
                        pos_idx = i - 12 if is_top else 11 - i
                        gap = 30 if pos_idx >= 6 else 0
                        bx = pos_idx * tri_w + gap
                        by = HEIGHT_PAD if is_top else HEIGHT//2
                        
                        if bx <= x <= bx + tri_w:
                            if is_top and y <= HEIGHT//2: clicked_idx = i
                            elif not is_top and y > HEIGHT//2: clicked_idx = i

                if clicked_idx is not None:
                    valid_move = False
                    for t_idx, die in valid_targets:
                        if clicked_idx == t_idx or (t_idx == 'OFF' and x > BOARD_WIDTH):
                            board.move_piece(selected_idx, clicked_idx, RED)
                            dice.remove(die)
                            selected_idx = None
                            valid_targets = []
                            valid_move = True
                            if not dice:
                                turn = WHITE
                                message = "AI TURN"
                            break
                    
                    if not valid_move:
                        c = RED
                        count = 0
                        if clicked_idx == 'BAR': count = board.bar[RED]
                        else: c, count = board.points[clicked_idx]
                        
                        if c == RED and count > 0:
                            selected_idx = clicked_idx
                            moves = board.get_valid_moves(dice, RED)
                            valid_targets = []
                            for m_start, m_end, m_die in moves:
                                if m_start == selected_idx:
                                    valid_targets.append((m_end, m_die))
                
                if x > BOARD_WIDTH and selected_idx is not None:
                    for t_idx, die in valid_targets:
                        if t_idx == 'OFF':
                             board.move_piece(selected_idx, 'OFF', RED)
                             dice.remove(die)
                             selected_idx = None
                             valid_targets = []
                             if not dice: turn = WHITE

        draw_targets = [t[0] for t in valid_targets if t[0] != 'OFF']
        draw_board(win, board, selected_idx, draw_targets)
        draw_dice(win, dice, turn)
        draw_pixel_string(win, message, WIDTH//2 - len(message)*6, HEIGHT//2 - 5, 2, WHITE_CHK)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
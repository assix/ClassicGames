import pygame
import sys
import random

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1250, 900
BOARD_ROWS, BOARD_COLS = 10, 10
CELL_SIZE = 80
MARGIN_X = 50
MARGIN_Y = 50
SIDEBAR_X = MARGIN_X + (BOARD_COLS * CELL_SIZE) + 40

# COLORS
BG_COLOR = (15, 15, 20)
GRID_COLOR = (40, 40, 50)
WATER_COLOR = (0, 100, 200)
RED_COLOR = (180, 40, 40)   # AI
BLUE_COLOR = (40, 80, 180)  # Player
TEXT_COL = (255, 255, 255)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
SELECT_COLOR = (0, 255, 0)
COMBAT_BG = (0, 0, 0, 220)

# PIECE SETUP
PIECES_SETUP = {
    '10': {'name': 'Marshal', 'rank': 10, 'count': 1},
    '9': {'name': 'General', 'rank': 9, 'count': 1},
    '8': {'name': 'Colonel', 'rank': 8, 'count': 2},
    '7': {'name': 'Major', 'rank': 7, 'count': 3},
    '6': {'name': 'Captain', 'rank': 6, 'count': 4},
    '5': {'name': 'Lieut.', 'rank': 5, 'count': 4},
    '4': {'name': 'Sergeant', 'rank': 4, 'count': 4},
    '3': {'name': 'Miner', 'rank': 3, 'count': 5},
    '2': {'name': 'Scout', 'rank': 2, 'count': 8},
    'S': {'name': 'Spy', 'rank': 1, 'count': 1},
    'B': {'name': 'Bomb', 'rank': 11, 'count': 6},
    'F': {'name': 'Flag', 'rank': 0, 'count': 1},
}

# --- PIXEL FONT ENGINE ---
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
    '.': [0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x60],
    '/': [0x08, 0x10, 0x20, 0x40, 0x80, 0x00, 0x00],
    ':': [0x00, 0x60, 0x60, 0x00, 0x60, 0x60, 0x00]
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
class Piece:
    def __init__(self, key, owner):
        self.key = key
        self.owner = owner
        self.rank = PIECES_SETUP[key]['rank']
        self.name = PIECES_SETUP[key]['name']
        self.revealed = False
        self.moved = False

    def is_movable(self): return self.key not in ['F', 'B']

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.turn = 'BLUE'
        self.winner = None
        self.selected = None
        self.valid_moves = []
        self.captured_red_keys = []
        self.captured_blue_keys = []
        self.combat_active = False
        self.combat_attacker = None
        self.combat_defender = None
        self.combat_result = ""
        self.combat_timer = 0
        self.setup_pieces()

    def setup_pieces(self):
        pool = []
        for key, info in PIECES_SETUP.items():
            for _ in range(info['count']): pool.append(key)
        
        # AI (RED)
        ai_pool = pool[:]
        ai_grid = [[None]*10 for _ in range(4)]
        flag_col = random.randint(1, 8)
        ai_grid[0][flag_col] = 'F'
        ai_pool.remove('F')
        for r, c in [(0, flag_col-1), (0, flag_col+1), (1, flag_col)]:
            if 'B' in ai_pool:
                ai_grid[r][c] = 'B'; ai_pool.remove('B')
        random.shuffle(ai_pool)
        for r in range(4):
            for c in range(10):
                if ai_grid[r][c] is None: ai_grid[r][c] = ai_pool.pop()
        for r in range(4):
            for c in range(10): self.grid[r][c] = Piece(ai_grid[r][c], 'RED')

        # Player (BLUE)
        p_pool = pool[:]
        random.shuffle(p_pool)
        idx = 0
        for r in range(6, 10):
            for c in range(10):
                self.grid[r][c] = Piece(p_pool[idx], 'BLUE')
                idx += 1

    def is_water(self, r, c): return r in [4, 5] and c in [2, 3, 6, 7]

    def get_valid_moves(self, r, c):
        moves = []
        p = self.grid[r][c]
        if not p or not p.is_movable(): return []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        is_scout = (p.key == '2')
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while 0 <= nr < BOARD_ROWS and 0 <= nc < BOARD_COLS:
                if self.is_water(nr, nc): break
                target = self.grid[nr][nc]
                if target is None:
                    moves.append((nr, nc))
                    if not is_scout: break
                elif target.owner != p.owner:
                    moves.append((nr, nc))
                    break
                else: break
                if not is_scout: break
                nr += dr
                nc += dc
        return moves

    def move_piece(self, start, end):
        sr, sc = start
        er, ec = end
        attacker = self.grid[sr][sc]
        defender = self.grid[er][ec]
        attacker.moved = True
        
        if defender:
            survivor, res = self.resolve_combat(attacker, defender)
            if res == "WIN_COMBAT" or res == "DEFUSE":
                self.record_loss(defender)
                self.grid[er][ec] = attacker
                self.grid[sr][sc] = None
            elif res == "LOSE_COMBAT":
                self.record_loss(attacker)
                self.grid[sr][sc] = None
            elif res == "DRAW":
                self.record_loss(attacker); self.record_loss(defender)
                self.grid[sr][sc] = None; self.grid[er][ec] = None
            elif res == "WIN":
                self.winner = attacker.owner
                self.grid[er][ec] = attacker
                self.grid[sr][sc] = None
        else:
            self.grid[er][ec] = attacker
            self.grid[sr][sc] = None
        self.turn = 'RED' if self.turn == 'BLUE' else 'BLUE'

    def resolve_combat(self, attacker, defender):
        attacker.revealed = True
        defender.revealed = True
        self.combat_active = True
        self.combat_attacker = attacker
        self.combat_defender = defender
        self.combat_timer = 60
        if defender.key == 'F':
            self.combat_result = "FLAG CAPTURED!"
            return attacker, "WIN"
        if attacker.key == 'S' and defender.key == '10':
            self.combat_result = "SPY ASSASSINATES MARSHAL!"
            return attacker, "WIN_COMBAT"
        if attacker.key == '3' and defender.key == 'B':
            self.combat_result = "MINER DEFUSES BOMB!"
            return attacker, "DEFUSE"
        if attacker.rank > defender.rank:
            self.combat_result = f"{attacker.name} WINS"
            return attacker, "WIN_COMBAT"
        elif attacker.rank < defender.rank:
            self.combat_result = f"{defender.name} WINS"
            return defender, "LOSE_COMBAT"
        else:
            self.combat_result = "MUTUAL DESTRUCTION"
            return None, "DRAW"

    def record_loss(self, piece):
        if piece.owner == 'RED': self.captured_red_keys.append(piece.key)
        else: self.captured_blue_keys.append(piece.key)

# --- AI ---
class AI:
    def __init__(self, diff): self.diff = diff
    def get_move(self, board):
        moves = []
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                p = board.grid[r][c]
                if p and p.owner == 'RED':
                    valid = board.get_valid_moves(r, c)
                    for v in valid: moves.append(((r, c), v))
        if not moves: return None
        if self.diff >= 2:
            best_move = None
            best_score = -1000
            for start, end in moves:
                score = 0
                attacker = board.grid[start[0]][start[1]]
                defender = board.grid[end[0]][end[1]]
                if defender:
                    if defender.revealed:
                        if attacker.rank > defender.rank: score += defender.rank * 10
                        elif attacker.rank < defender.rank: score -= attacker.rank * 10
                    else:
                        if attacker.rank < 4: score += 5
                        elif attacker.rank > 8: score -= 5
                else:
                    if end[0] > start[0]: score += 1
                if score > best_score:
                    best_score = score
                    best_move = (start, end)
            return best_move
        return random.choice(moves)

# --- HIGH FIDELITY GRAPHICS ---
def draw_detailed_sprite(screen, key, x, y, size):
    cx, cy = x + size//2, y + size//2
    # Base styling
    
    # 1. FLAG (Golden Waving Flag)
    if key == 'F':
        pygame.draw.line(screen, (100, 50, 0), (cx-10, cy+15), (cx-10, cy-15), 3) # Pole
        pygame.draw.polygon(screen, GOLD, [(cx-10, cy-15), (cx+15, cy-5), (cx-10, cy+5)])
        pygame.draw.polygon(screen, (200, 160, 0), [(cx-10, cy-15), (cx+15, cy-5), (cx-10, cy+5)], 2)
        return

    # 2. BOMB (Classic Black Sphere with Fuse)
    if key == 'B':
        pygame.draw.circle(screen, (20, 20, 20), (cx, cy+5), size//3) # Body
        pygame.draw.circle(screen, (80, 80, 80), (cx-5, cy), 3) # Highlight
        pygame.draw.line(screen, (200, 200, 200), (cx, cy-8), (cx+5, cy-15), 2) # Fuse
        pygame.draw.circle(screen, (255, 50, 0), (cx+6, cy-16), 3) # Fire
        return

    # 3. SPY (Trench Coat / Hat Silhouette)
    if key == 'S':
        # Hat
        pygame.draw.ellipse(screen, (20, 20, 20), (cx-15, cy-10, 30, 10))
        pygame.draw.rect(screen, (20, 20, 20), (cx-8, cy-18, 16, 12))
        # Coat collar
        pygame.draw.polygon(screen, (50, 50, 50), [(cx, cy+5), (cx-10, cy+15), (cx+10, cy+15)])
        # Eyes
        pygame.draw.rect(screen, (255, 255, 255), (cx-5, cy-5, 10, 3))
        return

    # 4. MARSHAL (10) - Crossed Batons + Star
    if key == '10':
        pygame.draw.line(screen, GOLD, (cx-10, cy-10), (cx+10, cy+10), 4)
        pygame.draw.line(screen, GOLD, (cx+10, cy-10), (cx-10, cy+10), 4)
        pygame.draw.circle(screen, SILVER, (cx, cy), 6)
        return

    # 5. GENERAL (9) - 3 Stars
    if key == '9':
        for off in [-12, 0, 12]:
            pygame.draw.circle(screen, GOLD, (cx+off, cy), 4)
        return
        
    # 6. COLONEL (8) - Eagle
    if key == '8':
        pygame.draw.polygon(screen, SILVER, [(cx, cy-8), (cx-12, cy), (cx-5, cy+5), (cx+5, cy+5), (cx+12, cy)])
        pygame.draw.circle(screen, SILVER, (cx, cy-10), 3)
        return

    # 7. MAJOR (7) - Oak Leaf
    if key == '7':
        pygame.draw.polygon(screen, GOLD, [(cx, cy-12), (cx+8, cy), (cx, cy+12), (cx-8, cy)])
        pygame.draw.line(screen, (100, 80, 0), (cx, cy-12), (cx, cy+12), 1)
        return

    # 8. CAPTAIN (6) - 4 Bars
    if key == '6':
        for i in range(-9, 10, 6): pygame.draw.line(screen, SILVER, (cx-10, cy+i), (cx+10, cy+i), 3)
        return

    # 9. LIEUTENANT (5) - 3 Bars
    if key == '5':
        for i in range(-6, 7, 6): pygame.draw.line(screen, SILVER, (cx-10, cy+i), (cx+10, cy+i), 3)
        return

    # 10. SERGEANT (4) - Chevrons
    if key == '4':
        col = (200, 200, 200)
        for i in range(0, 15, 5):
            pygame.draw.lines(screen, col, False, [(cx-10, cy-8+i), (cx, cy-15+i), (cx+10, cy-8+i)], 3)
        return

    # 11. MINER (3) - Pickaxe
    if key == '3':
        pygame.draw.line(screen, (139, 69, 19), (cx, cy-10), (cx, cy+12), 3) # Handle
        pygame.draw.arc(screen, SILVER, (cx-12, cy-15, 24, 15), 0, 3.14, 3) # Head
        return

    # 12. SCOUT (2) - Binoculars
    if key == '2':
        pygame.draw.rect(screen, (30, 30, 30), (cx-12, cy-5, 10, 10))
        pygame.draw.rect(screen, (30, 30, 30), (cx+2, cy-5, 10, 10))
        pygame.draw.line(screen, (100, 100, 100), (cx-2, cy), (cx+2, cy), 2)
        # Lens reflection
        pygame.draw.circle(screen, (100, 200, 255), (cx-7, cy), 2)
        pygame.draw.circle(screen, (100, 200, 255), (cx+7, cy), 2)
        return

def draw_piece(screen, piece, x, y, size=CELL_SIZE):
    bg = BLUE_COLOR if piece.owner == 'BLUE' else RED_COLOR
    
    # Card Body
    pygame.draw.rect(screen, bg, (x+2, y+2, size-4, size-4), border_radius=6)
    pygame.draw.rect(screen, (220, 220, 220), (x+2, y+2, size-4, size-4), 2, border_radius=6)
    
    # If Hidden
    if piece.owner == 'RED' and not piece.revealed:
        # Pattern on back of card
        pygame.draw.line(screen, (150, 30, 30), (x+10, y+10), (x+size-10, y+size-10), 2)
        pygame.draw.line(screen, (150, 30, 30), (x+size-10, y+10), (x+10, y+size-10), 2)
        return

    # Draw High Res Icon
    draw_detailed_sprite(screen, piece.key, x, y, size)
    
    # Draw Name (Bottom)
    name_txt = piece.name[:6] if len(piece.name) > 6 else piece.name
    draw_text(screen, name_txt, x + size//2, y + size - 12, 1, center=True)
    
    # Draw Rank (Top Left)
    rank_txt = str(piece.rank) if piece.rank not in [0, 11] else piece.key
    col = GOLD if piece.key in ['10', '9', 'F'] else TEXT_COL
    draw_text(screen, rank_txt, x + 10, y + 8, 1, col, center=False)

def draw_sidebar(screen, board):
    # BG
    pygame.draw.rect(screen, (25, 25, 30), (SIDEBAR_X, 0, WIDTH-SIDEBAR_X, HEIGHT))
    pygame.draw.line(screen, (100,100,100), (SIDEBAR_X, 0), (SIDEBAR_X, HEIGHT), 2)
    
    # Header
    draw_text(screen, "UNIT STATUS", SIDEBAR_X + 160, 30, 2, center=True)
    draw_text(screen, "UNIT      | ENEMY | YOU", SIDEBAR_X + 160, 70, 1, (150, 150, 150), center=True)
    pygame.draw.line(screen, (50,50,50), (SIDEBAR_X+10, 85), (WIDTH-10, 85), 1)

    # List
    order = ['10','9','8','7','6','5','4','3','2','S','B','F']
    y = 110
    
    for key in order:
        info = PIECES_SETUP[key]
        
        # 1. Mini Piece Preview
        # Draw a small box to represent the piece color neutral
        pygame.draw.rect(screen, (60, 60, 70), (SIDEBAR_X+20, y-15, 30, 30), border_radius=4)
        draw_detailed_sprite(screen, key, SIDEBAR_X+20, y-15, 30)
        
        # 2. Name
        draw_text(screen, info['name'][:10], SIDEBAR_X + 60, y-5, 1, TEXT_COL)
        
        # 3. Stats (Captured / Total)
        total = info['count']
        red_loss = board.captured_red_keys.count(key)
        blue_loss = board.captured_blue_keys.count(key)
        
        # Enemy Stats
        e_txt = f"{red_loss}/{total}"
        col_e = (100, 100, 100) if red_loss == total else RED_COLOR
        draw_text(screen, e_txt, SIDEBAR_X + 180, y-5, 2, col_e)
        
        # You Stats
        y_txt = f"{blue_loss}/{total}"
        col_y = (100, 100, 100) if blue_loss == total else BLUE_COLOR
        draw_text(screen, y_txt, SIDEBAR_X + 260, y-5, 2, col_y)

        y += 55

def draw_combat_overlay(screen, board):
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    s.fill(COMBAT_BG)
    screen.blit(s, (0, 0))
    
    cx, cy = WIDTH//2, HEIGHT//2
    
    # Attacker
    att = board.combat_attacker
    draw_text(screen, "ATTACKER", cx - 200, cy - 180, 2, center=True)
    draw_piece(screen, att, cx - 275, cy - 140, 150) # Big version
    
    # Defender
    def_ = board.combat_defender
    draw_text(screen, "DEFENDER", cx + 200, cy - 180, 2, center=True)
    draw_piece(screen, def_, cx + 125, cy - 140, 150) # Big version
    
    draw_text(screen, "VS", cx, cy - 65, 5, (255, 0, 0), center=True)
    
    # Result
    res_col = SELECT_COLOR if "WINS" in board.combat_result or "DEFUSE" in board.combat_result else RED_COLOR
    draw_text(screen, board.combat_result, cx, cy + 120, 3, res_col, center=True)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Stratego Remastered")
    clock = pygame.time.Clock()
    
    difficulty = 2
    state = "MENU"
    board = None
    ai = None
    hint_mode = False
    
    while True:
        clock.tick(30)
        screen.fill(BG_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if state == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: difficulty = 1
                    if event.key == pygame.K_2: difficulty = 2
                    if event.key == pygame.K_3: difficulty = 3
                    if event.key == pygame.K_SPACE:
                        board = Board()
                        ai = AI(difficulty)
                        state = "GAME"

            elif state == "GAME":
                if board.combat_active: continue
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                    hint_mode = not hint_mode
                
                if event.type == pygame.MOUSEBUTTONDOWN and board.turn == 'BLUE':
                    mx, my = event.pos
                    if mx < SIDEBAR_X and my > MARGIN_Y:
                        c, r = (mx - MARGIN_X) // CELL_SIZE, (my - MARGIN_Y) // CELL_SIZE
                        if 0 <= c < BOARD_COLS and 0 <= r < BOARD_ROWS:
                            if hint_mode:
                                p = board.grid[r][c]
                                if p and p.owner == 'RED':
                                    p.revealed = True
                                    hint_mode = False
                            else:
                                if board.selected is None:
                                    p = board.grid[r][c]
                                    if p and p.owner == 'BLUE':
                                        board.selected = (r, c)
                                        board.valid_moves = board.get_valid_moves(r, c)
                                else:
                                    if (r, c) in board.valid_moves:
                                        board.move_piece(board.selected, (r, c))
                                        board.selected = None
                                        board.valid_moves = []
                                    else:
                                        p = board.grid[r][c]
                                        if p and p.owner == 'BLUE':
                                            board.selected = (r, c)
                                            board.valid_moves = board.get_valid_moves(r, c)
                                        else:
                                            board.selected = None
                                            board.valid_moves = []
            
            elif state == "GAMEOVER":
                 if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                     state = "MENU"

        # --- DRAWING ---
        if state == "MENU":
            draw_text(screen, "STRATEGO COMMANDER", WIDTH//2, 200, 4, center=True)
            draw_text(screen, f"DIFFICULTY: {difficulty}", WIDTH//2, 350, 3, (100,200,255), center=True)
            draw_text(screen, "PRESS SPACE TO DEPLOY", WIDTH//2, 500, 2, center=True)

        elif state == "GAME":
            draw_sidebar(screen, board)
            
            for r in range(BOARD_ROWS):
                for c in range(BOARD_COLS):
                    x = MARGIN_X + c * CELL_SIZE
                    y = MARGIN_Y + r * CELL_SIZE
                    col = WATER_COLOR if board.is_water(r, c) else GRID_COLOR
                    pygame.draw.rect(screen, col, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(screen, (0,0,0), (x, y, CELL_SIZE, CELL_SIZE), 1)
                    
                    if (r, c) in board.valid_moves:
                        s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                        s.fill((0, 255, 0, 50))
                        screen.blit(s, (x, y))
                    
                    p = board.grid[r][c]
                    if p: draw_piece(screen, p, x, y)
            
            if board.combat_active:
                draw_combat_overlay(screen, board)
                board.combat_timer -= 1
                if board.combat_timer <= 0:
                    board.combat_active = False
                    if board.winner: state = "GAMEOVER"
            else:
                txt = "SELECT ENEMY TO REVEAL" if hint_mode else "PRESS 'H' FOR SATELLITE SCAN"
                col = GOLD if hint_mode else (150, 150, 150)
                draw_text(screen, txt, MARGIN_X + 400, 10, 2, col, center=True)
                
                if board.turn == 'RED' and not board.winner:
                    move = ai.get_move(board)
                    if move:
                        board.move_piece(move[0], move[1])
                    else:
                        board.winner = 'BLUE'
                        state = "GAMEOVER"
        
        elif state == "GAMEOVER":
             draw_text(screen, "MISSION ACCOMPLISHED" if board.winner=='BLUE' else "MISSION FAILED", WIDTH//2, 300, 4, center=True)
             draw_text(screen, "PRESS SPACE", WIDTH//2, 500, 2, center=True)

        pygame.display.flip()

if __name__ == "__main__":
    main()
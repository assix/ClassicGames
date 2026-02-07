import pygame
import sys
import random
import copy
from collections import deque

# --- CONFIGURATION ---
WIDTH, HEIGHT = 600, 850
UI_HEIGHT = 250
GAME_HEIGHT = HEIGHT - UI_HEIGHT
FPS = 60

# --- COLORS ---
BG_COLOR = (15, 15, 20)
QUEEN_COLOR = (255, 255, 255)
X_COLOR = (200, 200, 210) 
ERROR_COLOR = (255, 50, 50)
TEXT_COLOR = (240, 240, 245)
GOLD = (255, 215, 0)
MODAL_BG = (20, 20, 30, 240)

REGION_COLORS = [
    (110, 80, 150), (60, 130, 80), (170, 90, 50), 
    (40, 110, 170), (160, 50, 50), (150, 150, 50),
    (50, 150, 140), (130, 130, 130), (80, 160, 220), (210, 90, 160)
]

class QueensGame:
    def __init__(self, size):
        self.size = size
        self.cell_size = WIDTH // size
        self.reset()

    def reset(self):
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.regions = [[-1 for _ in range(self.size)] for _ in range(self.size)]
        self.solution = []
        self.history = []
        self.undo_count = 0
        self.hint_count = 0
        self.won = False
        self.hint_mode = False
        self.show_help = False
        self.last_click_time = 0
        self.last_click_cell = None
        self.generate_level()

    def generate_level(self):
        """Generates level and runs a cleanup pass to ensure 100% connected regions."""
        # 1. Backtracking Solver
        def is_safe(board, r, c):
            for i in range(r):
                if board[i] == c or abs(i - r) <= 1 and abs(board[i] - c) <= 1:
                    return False
            return True

        def solve(board, r):
            if r == self.size: return True
            indices = list(range(self.size))
            random.shuffle(indices)
            for c in indices:
                if is_safe(board, r, c):
                    board[r] = c
                    if solve(board, r + 1): return True
            return False

        board_sol = [-1] * self.size
        solve(board_sol, 0)
        self.solution = [(r, board_sol[r]) for r in range(self.size)]

        # 2. Region Growth
        self.regions = [[-1 for _ in range(self.size)] for _ in range(self.size)]
        seeds = []
        for i, (qr, qc) in enumerate(self.solution):
            self.regions[qr][qc] = i
            seeds.append([qr, qc, i, 1]) # [r, c, id, size]

        # Beginner constraints: force sizes 1, 2, 3...
        if self.size == 6:
            max_sizes = {0: 1, 1: 2, 2: 3, 3: 10, 4: 10, 5: 10}
        else:
            max_sizes = {i: 100 for i in range(self.size)}

        filled = self.size
        while filled < self.size * self.size:
            random.shuffle(seeds)
            added = False
            for s in seeds:
                r, c, rid, size = s
                if size >= max_sizes.get(rid, 100): continue

                neighbors = [(r+1,c), (r-1,c), (0,c+1), (0,c-1), (r,c+1), (r,c-1)]
                random.shuffle(neighbors)
                for nr, nc in neighbors:
                    if 0 <= nr < self.size and 0 <= nc < self.size and self.regions[nr][nc] == -1:
                        self.regions[nr][nc] = rid
                        s[3] += 1 # incr size
                        seeds.append([nr, nc, rid, s[3]])
                        filled += 1
                        added = True
                        break
            
            # Fill holes if blocked
            if not added:
                for r in range(self.size):
                    for c in range(self.size):
                        if self.regions[r][c] == -1:
                            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                                if 0 <= r+dr < self.size and 0 <= c+dc < self.size:
                                    if self.regions[r+dr][c+dc] != -1:
                                        self.regions[r][c] = self.regions[r+dr][c+dc]
                                        filled += 1
                                        break
                break
        
        # 3. CRITICAL: Enforce Contiguity
        self.enforce_contiguity()

    def enforce_contiguity(self):
        """Merges isolated islands into their largest neighbors."""
        changed = True
        while changed:
            changed = False
            # Find all connected components for each region
            visited = set()
            components = [] # (region_id, [(r,c), ...])

            for r in range(self.size):
                for c in range(self.size):
                    if (r,c) not in visited:
                        rid = self.regions[r][c]
                        # Flood fill to find component
                        q = deque([(r,c)])
                        visited.add((r,c))
                        cells = [(r,c)]
                        while q:
                            curr_r, curr_c = q.popleft()
                            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                                nr, nc = curr_r+dr, curr_c+dc
                                if 0 <= nr < self.size and 0 <= nc < self.size:
                                    if (nr,nc) not in visited and self.regions[nr][nc] == rid:
                                        visited.add((nr,nc))
                                        cells.append((nr,nc))
                                        q.append((nr,nc))
                        components.append((rid, cells))
            
            # Group components by region ID
            region_groups = {}
            for rid, cells in components:
                if rid not in region_groups: region_groups[rid] = []
                region_groups[rid].append(cells)

            # Check for split regions
            for rid, groups in region_groups.items():
                if len(groups) > 1:
                    changed = True
                    # Sort by size, keep largest
                    groups.sort(key=len, reverse=True)
                    main_body = groups[0]
                    orphans = groups[1:]
                    
                    # Merge orphans into neighbor
                    for orphan_cells in orphans:
                        for or_r, or_c in orphan_cells:
                            # Find a neighbor that isn't me
                            found_neighbor = False
                            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                                nr, nc = or_r+dr, or_c+dc
                                if 0 <= nr < self.size and 0 <= nc < self.size:
                                    neighbor_id = self.regions[nr][nc]
                                    if neighbor_id != rid:
                                        self.regions[or_r][or_c] = neighbor_id
                                        found_neighbor = True
                                        break
                            # Fallback if surrounded by self (shouldn't happen in loop)
                            if not found_neighbor: 
                                # Just pick any valid neighbor from diagonals or fallback
                                pass

    def auto_mark_x(self, r, c):
        if self.grid[r][c] != 1: return
        self.save_state()
        rid = self.regions[r][c]
        for nr in range(self.size):
            for nc in range(self.size):
                if nr == r and nc == c: continue
                if nr == r or nc == c or (abs(nr-r) <= 1 and abs(nc-c) <= 1) or self.regions[nr][nc] == rid:
                    if self.grid[nr][nc] == 0: self.grid[nr][nc] = 2

    def save_state(self):
        self.history.append(copy.deepcopy(self.grid))
        if len(self.history) > 50: self.history.pop(0)

    def undo(self):
        if self.history:
            self.grid = self.history.pop()
            self.undo_count += 1
            self.won = False

    def provide_hint(self, manual_pos=None):
        self.save_state()
        self.hint_count += 1
        if manual_pos:
            r, c = manual_pos
            self.grid[r][c] = 1 if (r, c) in self.solution else 2
        else:
            missing = [p for p in self.solution if self.grid[p[0]][p[1]] != 1]
            if missing:
                r, c = random.choice(missing)
                self.grid[r][c] = 1
        self.check_win()

    def check_rules(self, r, c):
        if self.grid[r][c] != 1: return False
        for r2 in range(self.size):
            for c2 in range(self.size):
                if r == r2 and c == c2: continue
                if self.grid[r2][c2] == 1:
                    if r == r2 or c == c2 or (abs(r-r2) <= 1 and abs(c-c2) <= 1) or self.regions[r][c] == self.regions[r2][c2]:
                        return True
        return False

    def handle_click(self, pos, button):
        if self.show_help: self.show_help = False; return
        if self.won: 
            if pos[1] >= GAME_HEIGHT: self.handle_ui_click(pos, button)
            return
            
        x, y = pos
        if y >= GAME_HEIGHT: self.handle_ui_click(pos, button); return
        r, c = y // self.cell_size, x // self.cell_size
        
        mouse_pressed = pygame.mouse.get_pressed()
        is_chord = (button == 1 and mouse_pressed[2]) or (button == 3 and mouse_pressed[0])
        
        if is_chord:
            self.auto_mark_x(r, c)
            return

        now = pygame.time.get_ticks()
        if button == 1 and self.last_click_cell == (r, c) and now - self.last_click_time < 300:
            self.auto_mark_x(r, c); return

        self.last_click_time, self.last_click_cell = now, (r, c)

        if self.hint_mode and button == 3: self.provide_hint((r, c)); self.hint_mode = False; return
        
        self.save_state()
        if button == 1: self.grid[r][c] = 1 if self.grid[r][c] != 1 else 0
        elif button == 3: self.grid[r][c] = 2 if self.grid[r][c] != 2 else 0
        self.check_win()

    def handle_ui_click(self, pos, button):
        x, y = pos
        if 20 <= x <= 180 and GAME_HEIGHT + 20 <= y <= GAME_HEIGHT + 80: self.undo()
        if 210 <= x <= 390 and GAME_HEIGHT + 20 <= y <= GAME_HEIGHT + 80: self.show_help = True
        if 420 <= x <= 580 and GAME_HEIGHT + 20 <= y <= GAME_HEIGHT + 80:
            if button == 1: self.provide_hint()
            elif button == 3: self.hint_mode = True
        if 210 <= x <= 390 and GAME_HEIGHT + 100 <= y <= GAME_HEIGHT + 160:
            self.reset()

    def check_win(self):
        if sum(row.count(1) for row in self.grid) == self.size:
            if not any(self.check_rules(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == 1):
                self.won = True

    def draw_help(self, screen, font, small_font):
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill(MODAL_BG); screen.blit(s, (0,0))
        rect = pygame.Rect(50, 100, WIDTH-100, HEIGHT-350)
        pygame.draw.rect(screen, (30, 30, 45), rect, border_radius=15)
        pygame.draw.rect(screen, GOLD, rect, 2, border_radius=15)
        lines = ["QUEENS RULES", "", "1. One Queen per ROW.", "2. One Queen per COLUMN.", "3. One Queen per COLOR REGION.", "4. Queens cannot touch (even diagonally).", "", "CONTROLS:", "- Left Click: Place Queen", "- Right Click: Place X (Marker)", "- L+R Click (Chord): Auto-mark illegal cells", "- Right Click Hint: Reveal a specific cell", "", "Click anywhere to close."]
        for i, line in enumerate(lines):
            color = GOLD if i == 0 else TEXT_COLOR
            txt = small_font.render(line, True, color)
            screen.blit(txt, (70, 140 + i * 28))

    def draw(self, screen, font, small_font):
        screen.fill(BG_COLOR)
        for r in range(self.size):
            for c in range(self.size):
                color = REGION_COLORS[self.regions[r][c] % len(REGION_COLORS)]
                pygame.draw.rect(screen, color, (c*self.cell_size, r*self.cell_size, self.cell_size, self.cell_size))
                center = (c*self.cell_size + self.cell_size//2, r*self.cell_size + self.cell_size//2)
                if self.grid[r][c] == 1:
                    col = ERROR_COLOR if self.check_rules(r, c) else QUEEN_COLOR
                    scale = self.cell_size // 4
                    pts = [(center[0]-scale, center[1]+scale), (center[0]+scale, center[1]+scale), (center[0]+scale, center[1]-scale), (center[0]+scale//2, center[1]), (center[0], center[1]-scale*1.5), (center[0]-scale//2, center[1]), (center[0]-scale, center[1]-scale)]
                    pygame.draw.polygon(screen, col, pts)
                elif self.grid[r][c] == 2:
                    offset = self.cell_size // 4
                    pygame.draw.line(screen, X_COLOR, (c*self.cell_size+offset, r*self.cell_size+offset), (c*self.cell_size+self.cell_size-offset, r*self.cell_size+self.cell_size-offset), 6)
                    pygame.draw.line(screen, X_COLOR, (c*self.cell_size+self.cell_size-offset, r*self.cell_size+offset), (c*self.cell_size+offset, r*self.cell_size+self.cell_size-offset), 6)

        for r in range(self.size):
            for c in range(self.size):
                if r < self.size-1 and self.regions[r][c] != self.regions[r+1][c]:
                    pygame.draw.line(screen, BG_COLOR, (c*self.cell_size, (r+1)*self.cell_size), ((c+1)*self.cell_size, (r+1)*self.cell_size), 4)
                if c < self.size-1 and self.regions[r][c] != self.regions[r][c+1]:
                    pygame.draw.line(screen, BG_COLOR, ((c+1)*self.cell_size, r*self.cell_size), ((c+1)*self.cell_size, (r+1)*self.cell_size), 4)

        pygame.draw.rect(screen, (25, 25, 35), (0, GAME_HEIGHT, WIDTH, UI_HEIGHT))
        btn_data = [("UNDO", 20, self.undo_count), ("HELP", 210, None), ("HINT", 420, self.hint_count)]
        for label, x, count in btn_data:
            b_col = GOLD if (label == "HINT" and self.hint_mode) else (50, 50, 65)
            pygame.draw.rect(screen, b_col, (x, GAME_HEIGHT + 20, 160, 60), border_radius=10)
            t = font.render(label, True, BG_COLOR if (label=="HINT" and self.hint_mode) else TEXT_COLOR)
            screen.blit(t, (x + 80 - t.get_width()//2, GAME_HEIGHT + 35))
            if count is not None:
                c_txt = small_font.render(f"Used: {count}", True, X_COLOR)
                screen.blit(c_txt, (x + 80 - c_txt.get_width()//2, GAME_HEIGHT + 90))

        pygame.draw.rect(screen, (50, 100, 50), (210, GAME_HEIGHT + 100, 160, 60), border_radius=10)
        ng_txt = font.render("NEW GAME", True, TEXT_COLOR)
        screen.blit(ng_txt, (290 - ng_txt.get_width()//2, GAME_HEIGHT + 115))

        if self.won:
            w_txt = font.render("PUZZLE SOLVED!", True, GOLD)
            screen.blit(w_txt, (WIDTH//2 - w_txt.get_width()//2, GAME_HEIGHT + 180))
        if self.show_help: self.draw_help(screen, font, small_font)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Queens")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 22, bold=True)
    small_font = pygame.font.SysFont("Verdana", 16)
    selected_size = None
    while selected_size is None:
        screen.fill(BG_COLOR)
        title = font.render("CHOOSE DIFFICULTY", True, GOLD)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        btns = [("BEGINNER (6x6)", 6, 250), ("INTERMEDIATE (8x8)", 8, 350), ("EXPERT (10x10)", 10, 450)]
        m_pos, clicked = pygame.mouse.get_pos(), False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: clicked = True
        for label, size, y in btns:
            rect = pygame.Rect(WIDTH//2 - 150, y, 300, 60)
            c = (70, 70, 85) if rect.collidepoint(m_pos) else (40, 40, 55)
            pygame.draw.rect(screen, c, rect, border_radius=10)
            t = font.render(label, True, TEXT_COLOR)
            screen.blit(t, (WIDTH//2 - t.get_width()//2, y + 15))
            if clicked and rect.collidepoint(m_pos): selected_size = size
        pygame.display.flip()
        clock.tick(FPS)
    game = QueensGame(selected_size)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: game.handle_click(event.pos, event.button)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: main()
        game.draw(screen, font, small_font)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__": main()
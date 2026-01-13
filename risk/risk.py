import pygame
import random
import sys
import math

# --- SETUP ---
pygame.init()
WIDTH, HEIGHT = 1000, 700
BG_COLOR = (10, 10, 30)
OCEAN_COLOR = (20, 20, 50)
LINE_COLOR = (100, 100, 150)
HIGHLIGHT = (255, 255, 0)
TEXT_COLOR = (255, 255, 255)

# Player Colors
P1_COLOR = (50, 200, 50)   # Green (You)
P2_COLOR = (200, 50, 50)   # Red (AI)

PLAYER_COLORS = [P1_COLOR, P2_COLOR]
PLAYER_NAMES = ["YOU", "AI"]

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
    ':': [0x00, 0x60, 0x60, 0x00, 0x60, 0x60, 0x00],
}

def draw_pixel_char(surface, char, x, y, scale, color):
    char = char.upper()
    if char not in PIXEL_FONT_5x7: char = ' '
    rows = PIXEL_FONT_5x7[char]
    for r_idx, row_val in enumerate(rows):
        for c_idx in range(5):
            if (row_val >> (7 - c_idx)) & 1:
                pygame.draw.rect(surface, color, (x + c_idx * scale, y + r_idx * scale, scale, scale))

def draw_pixel_string(surface, text, x, y, scale, color):
    cursor_x = x
    for char in str(text).upper():
        draw_pixel_char(surface, char, cursor_x, y, scale, color)
        cursor_x += (6 * scale)

# --- MAP DATA ---
NODES = {
    'Alaska': (50, 100, 'NA'), 'NWest': (150, 100, 'NA'), 'Greenland': (300, 50, 'NA'),
    'Alberta': (120, 150, 'NA'), 'Ontario': (220, 160, 'NA'), 'E_US': (220, 230, 'NA'), 'W_US': (120, 220, 'NA'), 'Central': (150, 300, 'NA'),
    'Venezuela': (250, 350, 'SA'), 'Brazil': (320, 420, 'SA'), 'Peru': (240, 450, 'SA'), 'Argentina': (260, 550, 'SA'),
    'Iceland': (400, 80, 'EU'), 'UK': (400, 150, 'EU'), 'W_EU': (420, 220, 'EU'), 'N_EU': (480, 150, 'EU'), 'S_EU': (500, 240, 'EU'), 'Rus': (600, 150, 'EU'),
    'N_Afr': (450, 350, 'AF'), 'Egypt': (550, 360, 'AF'), 'E_Afr': (600, 450, 'AF'), 'C_Afr': (500, 450, 'AF'), 'S_Afr': (520, 580, 'AF'), 'Madagascar': (650, 550, 'AF'),
    'Ural': (680, 120, 'AS'), 'Siberia': (750, 100, 'AS'), 'Yakutsk': (850, 80, 'AS'), 'Kamchatka': (920, 100, 'AS'),
    'Irk': (800, 180, 'AS'), 'Mon': (800, 250, 'AS'), 'Japan': (920, 250, 'AS'),
    'Afghan': (650, 250, 'AS'), 'China': (780, 300, 'AS'), 'India': (720, 350, 'AS'), 'Middle_E': (620, 320, 'AS'), 'Siam': (820, 380, 'AS'),
    'Indo': (820, 480, 'AU'), 'W_Aus': (850, 580, 'AU'), 'E_Aus': (920, 550, 'AU'), 'NG': (920, 480, 'AU')
}

CONNECTIONS = [
    ('Alaska', 'NWest'), ('Alaska', 'Alberta'), ('Alaska', 'Kamchatka'),
    ('NWest', 'Greenland'), ('NWest', 'Alberta'), ('NWest', 'Ontario'),
    ('Greenland', 'Ontario'), ('Greenland', 'Iceland'),
    ('Alberta', 'Ontario'), ('Alberta', 'W_US'),
    ('Ontario', 'E_US'), ('Ontario', 'W_US'),
    ('W_US', 'E_US'), ('W_US', 'Central'), ('E_US', 'Central'),
    ('Central', 'Venezuela'), ('Venezuela', 'Brazil'), ('Venezuela', 'Peru'),
    ('Brazil', 'Peru'), ('Brazil', 'Argentina'), ('Brazil', 'N_Afr'),
    ('Peru', 'Argentina'), ('Iceland', 'UK'), ('Iceland', 'N_EU'),
    ('UK', 'W_EU'), ('UK', 'N_EU'), ('W_EU', 'N_EU'), ('W_EU', 'S_EU'), ('W_EU', 'N_Afr'),
    ('N_EU', 'S_EU'), ('N_EU', 'Rus'), ('S_EU', 'Rus'), ('S_EU', 'Middle_E'), ('S_EU', 'N_Afr'), ('S_EU', 'Egypt'),
    ('Rus', 'Ural'), ('Rus', 'Afghan'), ('Rus', 'Middle_E'),
    ('N_Afr', 'Egypt'), ('N_Afr', 'E_Afr'), ('N_Afr', 'C_Afr'),
    ('Egypt', 'Middle_E'), ('Egypt', 'E_Afr'), ('E_Afr', 'C_Afr'), ('E_Afr', 'S_Afr'), ('E_Afr', 'Madagascar'),
    ('C_Afr', 'S_Afr'), ('S_Afr', 'Madagascar'), ('Middle_E', 'Afghan'), ('Middle_E', 'India'),
    ('Ural', 'Siberia'), ('Ural', 'Afghan'), ('Ural', 'China'),
    ('Siberia', 'Yakutsk'), ('Siberia', 'Irk'), ('Siberia', 'Mon'), ('Siberia', 'China'),
    ('Yakutsk', 'Kamchatka'), ('Yakutsk', 'Irk'), ('Kamchatka', 'Irk'), ('Kamchatka', 'Japan'), ('Kamchatka', 'Mon'),
    ('Irk', 'Mon'), ('Mon', 'Japan'), ('Mon', 'China'), ('Japan', 'China'),
    ('Afghan', 'China'), ('Afghan', 'India'), ('China', 'India'), ('China', 'Siam'),
    ('India', 'Siam'), ('Siam', 'Indo'), ('Indo', 'W_Aus'), ('Indo', 'NG'),
    ('NG', 'E_Aus'), ('NG', 'W_Aus'), ('W_Aus', 'E_Aus')
]

# --- GAME LOGIC ---
class Territory:
    def __init__(self, name, x, y, continent):
        self.name = name
        self.x = x
        self.y = y
        self.continent = continent
        self.owner = -1
        self.armies = 0
        self.neighbors = []

    def draw(self, win, is_selected, is_neighbor, is_path_option):
        if self.owner == -1: col = (100, 100, 100)
        else: col = PLAYER_COLORS[self.owner]
        
        radius = 18
        if is_selected:
            pygame.draw.circle(win, HIGHLIGHT, (self.x, self.y), radius + 4, 2)
        elif is_neighbor and not is_path_option: # Only show attack targets red
             pygame.draw.circle(win, (255, 100, 100), (self.x, self.y), radius + 4, 1)
        elif is_path_option: # Show fortify targets blue
             pygame.draw.circle(win, (100, 100, 255), (self.x, self.y), radius + 4, 1)

        pygame.draw.circle(win, col, (self.x, self.y), radius)
        pygame.draw.circle(win, (255, 255, 255), (self.x, self.y), radius, 1)
        
        t_col = (0, 0, 0) if self.owner != -1 else (255, 255, 255)
        txt = str(self.armies)
        off = len(txt) * 3
        draw_pixel_string(win, txt, self.x - off, self.y - 4, 1, t_col)

class RiskGame:
    def __init__(self):
        self.territories = {}
        self.setup_map()
        self.turn = 0 # 0=Human, 1=AI
        self.phase = "DRAFT"
        self.draft_pool = 0
        self.selected_t = None
        self.target_t = None
        self.valid_fortify_targets = []
        self.message = "INITIALIZING"
        self.ai_timer = 0
        
        self.initial_distribution()
        self.start_turn()

    def setup_map(self):
        for name, data in NODES.items():
            self.territories[name] = Territory(name, data[0], data[1], data[2])
        for n1, n2 in CONNECTIONS:
            if n1 in self.territories and n2 in self.territories:
                self.territories[n1].neighbors.append(self.territories[n2])
                self.territories[n2].neighbors.append(self.territories[n1])

    def initial_distribution(self):
        keys = list(self.territories.keys())
        random.shuffle(keys)
        for i, k in enumerate(keys):
            self.territories[k].owner = i % 2
            self.territories[k].armies = 3
            
    def start_turn(self):
        self.phase = "DRAFT"
        self.selected_t = None
        self.target_t = None
        self.valid_fortify_targets = []
        
        owned = [t for t in self.territories.values() if t.owner == self.turn]
        if not owned: 
            self.message = "GAME OVER"
            return
            
        bonus = max(3, len(owned) // 3)
        self.draft_pool = bonus
        self.message = f"{PLAYER_NAMES[self.turn]} DRAFT: {self.draft_pool} ARMIES"
        self.ai_timer = 30 

    def update(self):
        if self.turn == 1: # AI Turn
            if self.ai_timer > 0:
                self.ai_timer -= 1
                return
            self.ai_timer = 20

            if self.phase == "DRAFT":
                candidates = [t for t in self.territories.values() if t.owner == 1]
                if candidates and self.draft_pool > 0:
                    target = random.choice(candidates)
                    target.armies += 1
                    self.draft_pool -= 1
                if self.draft_pool == 0:
                    self.next_phase()

            elif self.phase == "ATTACK":
                attacks = []
                for t in self.territories.values():
                    if t.owner == 1 and t.armies > 2:
                        for n in t.neighbors:
                            if n.owner == 0:
                                diff = t.armies - n.armies
                                if diff > 1:
                                    attacks.append((diff, t, n))
                
                attacks.sort(key=lambda x: x[0], reverse=True)
                
                if attacks:
                    _, att, dfd = attacks[0]
                    self.selected_t = att
                    self.target_t = dfd
                    self.resolve_battle()
                    if att.armies <= 2:
                         self.selected_t = None
                         self.target_t = None
                else:
                    self.next_phase()

            elif self.phase == "FORTIFY":
                # AI Logic: Find border territory that needs reinforcement
                # Simplistic: Just random move
                self.next_phase()

    def get_connected_territories(self, start_node):
        """BFS to find all connected territories owned by the same player"""
        connected = []
        queue = [start_node]
        visited = {start_node}
        
        while queue:
            current = queue.pop(0)
            if current != start_node:
                connected.append(current)
            
            for neighbor in current.neighbors:
                if neighbor.owner == start_node.owner and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return connected

    def handle_click(self, pos):
        if self.turn == 1: return 

        clicked = None
        for t in self.territories.values():
            dist = math.hypot(t.x - pos[0], t.y - pos[1])
            if dist < 20:
                clicked = t
                break
        
        if clicked:
            if self.phase == "DRAFT":
                if clicked.owner == self.turn and self.draft_pool > 0:
                    clicked.armies += 1
                    self.draft_pool -= 1
                    if self.draft_pool == 0:
                        self.message = "DRAFT DONE. NEXT PHASE >"

            elif self.phase == "ATTACK":
                if self.selected_t is None:
                    if clicked.owner == self.turn and clicked.armies > 1:
                        self.selected_t = clicked
                        self.message = "SELECT TARGET"
                else:
                    if clicked == self.selected_t:
                        self.selected_t = None
                        self.message = "ATTACK CANCELLED"
                    elif clicked in self.selected_t.neighbors and clicked.owner != self.turn:
                        self.target_t = clicked
                        self.resolve_battle()

            elif self.phase == "FORTIFY":
                if self.selected_t is None:
                    # Select Source
                    if clicked.owner == self.turn and clicked.armies > 1:
                        self.selected_t = clicked
                        # CALCULATE VALID PATHS
                        self.valid_fortify_targets = self.get_connected_territories(clicked)
                        if not self.valid_fortify_targets:
                            self.message = "NO CONNECTED DESTINATIONS"
                            self.selected_t = None
                        else:
                            self.message = "SELECT CONNECTED DESTINATION"
                else:
                    if clicked == self.selected_t:
                        self.selected_t = None
                        self.valid_fortify_targets = []
                        self.message = "FORTIFY CANCELLED"
                    elif clicked in self.valid_fortify_targets:
                        # Move 1 army
                        if self.selected_t.armies > 1:
                            self.selected_t.armies -= 1
                            clicked.armies += 1
                            self.message = "MOVED 1 ARMY"

    def resolve_battle(self):
        att = self.selected_t
        defs = self.target_t
        
        if att.armies <= 1: return

        att_dice_count = min(3, att.armies - 1)
        def_dice_count = min(2, defs.armies)
        
        att_roll = sorted([random.randint(1,6) for _ in range(att_dice_count)], reverse=True)
        def_roll = sorted([random.randint(1,6) for _ in range(def_dice_count)], reverse=True)
        
        msg = f"ROLL A:{att_roll} D:{def_roll} "
        
        comparisons = min(len(att_roll), len(def_roll))
        loss_att = 0
        loss_def = 0
        
        for i in range(comparisons):
            if att_roll[i] > def_roll[i]: loss_def += 1
            else: loss_att += 1
        
        att.armies -= loss_att
        defs.armies -= loss_def
        
        if defs.armies <= 0:
            defs.owner = att.owner
            move_in = att_dice_count
            att.armies -= move_in
            defs.armies = move_in
            msg += "CONQUERED!"
            self.selected_t = None
            self.target_t = None
        
        self.message = msg

    def next_phase(self):
        if self.phase == "DRAFT":
            if self.draft_pool == 0:
                self.phase = "ATTACK"
                self.message = "ATTACK PHASE"
            else:
                self.message = "PLACE ALL ARMIES FIRST"
        elif self.phase == "ATTACK":
            self.phase = "FORTIFY"
            self.selected_t = None
            self.target_t = None
            self.message = "FORTIFY PHASE"
        elif self.phase == "FORTIFY":
            self.phase = "DRAFT" # Reset phase display
            self.turn = (self.turn + 1) % 2
            self.start_turn()

    def draw(self, win):
        win.fill(BG_COLOR)
        
        for name, t in self.territories.items():
            for n in t.neighbors:
                pygame.draw.line(win, LINE_COLOR, (t.x, t.y), (n.x, n.y), 2)
        
        for t in self.territories.values():
            is_sel = (t == self.selected_t)
            is_neigh = (self.selected_t and t in self.selected_t.neighbors and self.phase == "ATTACK")
            is_path = (t in self.valid_fortify_targets and self.phase == "FORTIFY")
            
            t.draw(win, is_sel, is_neigh, is_path)
            
        pygame.draw.rect(win, (30, 30, 30), (0, HEIGHT-60, WIDTH, 60))
        
        btn_col = (100, 100, 100)
        pygame.draw.rect(win, btn_col, (WIDTH - 150, HEIGHT - 50, 130, 40))
        draw_pixel_string(win, "NEXT PHASE", WIDTH - 140, HEIGHT - 40, 2, (255, 255, 255))
        
        p_col = PLAYER_COLORS[self.turn]
        draw_pixel_string(win, self.message, 20, HEIGHT - 40, 2, p_col)
        
        # Scoreboard
        p1_score = len([t for t in self.territories.values() if t.owner == 0])
        p2_score = len([t for t in self.territories.values() if t.owner == 1])
        
        pygame.draw.rect(win, (0,0,0), (10, 10, 200, 70))
        pygame.draw.rect(win, (100,100,100), (10, 10, 200, 70), 2)
        
        draw_pixel_string(win, f"YOU:{p1_score}", 20, 20, 2, P1_COLOR)
        draw_pixel_string(win, f"AI :{p2_score}", 20, 50, 2, P2_COLOR)

# --- MAIN LOOP ---
def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Risk vs AI")
    clock = pygame.time.Clock()
    game = RiskGame()
    
    next_btn = pygame.Rect(WIDTH - 150, HEIGHT - 50, 130, 40)
    
    run = True
    while run:
        clock.tick(30)
        
        game.update()
        game.draw(win)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if next_btn.collidepoint(pos):
                    if game.turn == 0:
                        game.next_phase()
                else:
                    game.handle_click(pos)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
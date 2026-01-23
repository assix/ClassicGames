import pygame
import sys
import random
import math

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1000, 700
FPS = 60
BG_COLOR = (20, 20, 40)       # Dark Cavern Blue
UI_BG_COLOR = (40, 40, 45)
UI_HEIGHT = 100
GAME_HEIGHT = HEIGHT - UI_HEIGHT

LEM_WIDTH, LEM_HEIGHT = 16, 28
SPAWN_RATE = 50
TOTAL_LEMMINGS = 20
GRAVITY = 0.5
WALK_SPEED = 1.2

# --- COLORS ---
HAIR_COL = (0, 220, 50)     # Neon Green
SKIN_COL = (255, 210, 190)
ROBE_COL = (50, 100, 220)   # Royal Blue
DIRT_COL = (100, 80, 40)
GRASS_COL = (50, 150, 50)
GOLD = (255, 215, 0)
BUILD_COL = (130, 100, 50)

# --- JOBS ---
JOB_WALKER = 'Walker'
JOB_DIGGER = 'Digger'
JOB_BUILDER = 'Builder'
JOB_BLOCKER = 'Blocker'
JOB_BOMBER = 'Bomber'

jobs_list = [JOB_DIGGER, JOB_BUILDER, JOB_BLOCKER, JOB_BOMBER]
INITIAL_COUNTS = {JOB_DIGGER: 10, JOB_BUILDER: 20, JOB_BLOCKER: 5, JOB_BOMBER: 5}
job_counts = INITIAL_COUNTS.copy()
selected_job = None

# --- PARTICLE SYSTEM ---
class Particle:
    def __init__(self, x, y, color, vel_x, vel_y):
        self.x, self.y = x, y
        self.vx, self.vy = vel_x, vel_y
        self.color = color
        self.life = random.randint(20, 40)
        self.size = random.randint(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

particles = []

def spawn_particles(x, y, color, count=5):
    for _ in range(count):
        vx = random.uniform(-2, 2)
        vy = random.uniform(-3, -1)
        particles.append(Particle(x, y, color, vx, vy))

# --- PROCEDURAL GRAPHICS ---
def draw_lemming(surface, x, y, job, direction, frame, highlight=False):
    if highlight:
        pygame.draw.rect(surface, (255, 255, 255), (x-4, y-4, LEM_WIDTH+8, LEM_HEIGHT+8), 1)

    dm = direction
    cycle = (frame // 5) % 4
    
    # Feet
    if job == JOB_WALKER or job == JOB_BUILDER:
        off_l = math.sin(frame * 0.4) * 4
        off_r = math.sin(frame * 0.4 + math.pi) * 4
        pygame.draw.rect(surface, (200, 200, 200), (x+6+off_l, y+24, 4, 4))
        pygame.draw.rect(surface, (200, 200, 200), (x+6+off_r, y+24, 4, 4))
    elif job == JOB_DIGGER:
        shuffle = math.sin(frame * 0.8) * 2
        pygame.draw.rect(surface, (200, 200, 200), (x+4, y+24+shuffle, 4, 4))
        pygame.draw.rect(surface, (200, 200, 200), (x+10, y+24-shuffle, 4, 4))

    # Body
    pygame.draw.rect(surface, ROBE_COL, (x+2, y+10, 12, 14), border_radius=4)
    
    # Arms
    if job == JOB_BLOCKER:
        pygame.draw.rect(surface, ROBE_COL, (x-4, y+14, 24, 6))
        pygame.draw.rect(surface, SKIN_COL, (x-4, y+14, 4, 6))
        pygame.draw.rect(surface, SKIN_COL, (x+16, y+14, 4, 6))
    elif job == JOB_BUILDER:
        if cycle % 2 == 0:
            pygame.draw.rect(surface, ROBE_COL, (x + 8*dm + (4 if dm<0 else 0), y+12, 8, 4))
    
    # Head
    head_y_off = 2 if (job == JOB_DIGGER and cycle%2==0) else 0
    pygame.draw.circle(surface, SKIN_COL, (x+8, y+6+head_y_off), 7)
    eye_x = x+10 if direction == 1 else x+4
    pygame.draw.circle(surface, (0,0,0), (eye_x, y+6+head_y_off), 2)
    
    # Hair
    pygame.draw.ellipse(surface, HAIR_COL, (x+1, y-2+head_y_off, 14, 6))
    hair_sway = math.sin(frame*0.5)*3 if job == JOB_WALKER else 0
    py_x = x+2 if direction == 1 else x+12
    pygame.draw.circle(surface, HAIR_COL, (py_x - hair_sway, y+6+head_y_off), 3)

    if job == JOB_BOMBER:
        t = 5 - (frame // 60)
        draw_text_small(surface, str(t), x+8, y-10, (255, 0, 0))

# --- GAME LOGIC ---
class Lemming:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vx, self.vy = 0, 0
        self.job = JOB_WALKER
        self.direction = 1
        self.on_ground = False
        self.alive = True
        self.exited = False
        self.frame = random.randint(0, 100)
        self.build_steps = 0
        self.bomber_timer = 300 

    def rect(self): return pygame.Rect(self.x, self.y, LEM_WIDTH, LEM_HEIGHT)

    def update(self, terrain, lemmings):
        if not self.alive or self.exited: return
        self.frame += 1

        ground_y = int(self.y + LEM_HEIGHT + 1)
        center_x = int(self.x + LEM_WIDTH//2)
        
        is_solid = False
        if 0 <= center_x < WIDTH and 0 <= ground_y < GAME_HEIGHT:
            try:
                if terrain.get_at((center_x, ground_y))[3] > 0:
                    is_solid = True
            except IndexError: pass
        
        self.on_ground = is_solid

        if self.job == JOB_WALKER:
            if self.on_ground:
                self.vy = 0
                check_x = int(self.x + LEM_WIDTH + 2) if self.direction==1 else int(self.x - 2)
                check_y = int(self.y + LEM_HEIGHT - 8)
                
                hit_obstacle = False
                
                if 0 <= check_x < WIDTH and 0 <= check_y < GAME_HEIGHT:
                    try:
                        if terrain.get_at((check_x, check_y))[3] > 0:
                            # Climbing
                            climbed = False
                            for offset in range(1, 9):
                                if terrain.get_at((check_x, check_y - offset))[3] == 0:
                                    self.y -= offset
                                    climbed = True
                                    break
                            if not climbed: hit_obstacle = True
                    except IndexError: hit_obstacle = True

                my_rect = self.rect()
                for other in lemmings:
                    if other is not self and other.alive and other.job == JOB_BLOCKER:
                        if my_rect.colliderect(other.rect()):
                            if (self.direction == 1 and other.x > self.x) or \
                               (self.direction == -1 and other.x < self.x):
                                hit_obstacle = True

                if hit_obstacle:
                    self.direction *= -1
                else:
                    self.vx = WALK_SPEED * self.direction
            else:
                self.vx = 0
                self.vy += GRAVITY
        
        elif self.job == JOB_BLOCKER:
            self.vx = 0
            if not self.on_ground: self.vy += GRAVITY
            else: self.vy = 0

        elif self.job == JOB_DIGGER:
            self.vx = 0
            if self.on_ground:
                if self.frame % 5 == 0:
                    dig_rect = pygame.Rect(self.x, self.y+LEM_HEIGHT, LEM_WIDTH, 4)
                    pygame.draw.rect(terrain, (0,0,0,0), dig_rect)
                    self.y += 2
                    spawn_particles(self.x+LEM_WIDTH//2, self.y+LEM_HEIGHT, DIRT_COL, 3)
            else:
                self.job = JOB_WALKER
                self.vy += GRAVITY

        elif self.job == JOB_BUILDER:
            self.vx = 0
            if self.on_ground:
                if self.frame % 15 == 0:
                    if self.build_steps < 12:
                        bx = self.x + LEM_WIDTH if self.direction==1 else self.x - 8
                        by = self.y + LEM_HEIGHT - 6
                        pygame.draw.rect(terrain, BUILD_COL, (bx, by, 8, 6))
                        self.x += 8 * self.direction
                        self.y -= 6
                        self.build_steps += 1
                        spawn_particles(self.x, self.y+LEM_HEIGHT, (150,150,150), 2)
                    else:
                        self.job = JOB_WALKER
            else:
                self.vy += GRAVITY

        elif self.job == JOB_BOMBER:
            self.vx = 0
            self.bomber_timer -= 1
            if self.bomber_timer <= 0:
                self.alive = False
                cx, cy = self.x + LEM_WIDTH//2, self.y + LEM_HEIGHT//2
                pygame.draw.circle(terrain, (0,0,0,0), (int(cx), int(cy)), 30)
                spawn_particles(cx, cy, (255, 100, 50), 20)
                spawn_particles(cx, cy, (200, 200, 200), 20)

        self.x += self.vx
        self.y += self.vy
        if self.y > GAME_HEIGHT: self.alive = False

# --- TERRAIN GENERATION (PROCEDURAL) ---
def create_level():
    s = pygame.Surface((WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
    
    def fill_rect(rect):
        pygame.draw.rect(s, DIRT_COL, rect)
        pygame.draw.rect(s, GRASS_COL, (rect.left, rect.top, rect.width, 10))
    
    # 1. Start Platform (Fixed Top Left)
    fill_rect(pygame.Rect(50, 150, 250, 400))
    
    # 2. End Platform (Fixed Bottom Right)
    fill_rect(pygame.Rect(50, 550, 900, 50)) 
    
    # 3. Random Middle Platforms (2-3 Islands)
    num_islands = random.randint(2, 3)
    current_x = 320
    for _ in range(num_islands):
        w = random.randint(100, 200)
        h = 50
        y = random.randint(250, 450)
        
        # Ensure gap is jumpable (or buildable)
        gap = random.randint(20, 80)
        current_x += gap
        
        fill_rect(pygame.Rect(current_x, y, w, h))
        current_x += w

    # 4. Random Obstacles (Walls)
    num_walls = random.randint(1, 2)
    for _ in range(num_walls):
        wx = random.randint(350, 800)
        wy = random.randint(250, 450)
        wh = random.randint(80, 150)
        fill_rect(pygame.Rect(wx, wy, 40, wh))
    
    return s

def draw_text_small(surf, text, x, y, color=(255,255,255)):
    font = pygame.font.SysFont("Arial", 12, bold=True)
    img = font.render(text, True, color)
    surf.blit(img, (x, y))

def draw_ui(screen, font):
    pygame.draw.rect(screen, UI_BG_COLOR, (0, GAME_HEIGHT, WIDTH, UI_HEIGHT))
    pygame.draw.line(screen, (100,100,100), (0, GAME_HEIGHT), (WIDTH, GAME_HEIGHT), 3)

    bx = 50
    for job in jobs_list:
        cnt = job_counts[job]
        border_col = GOLD if job == selected_job else (100, 100, 100)
        bg_col = (60, 60, 70)
        
        rect = pygame.Rect(bx, GAME_HEIGHT + 15, 120, 70)
        pygame.draw.rect(screen, bg_col, rect, border_radius=8)
        pygame.draw.rect(screen, border_col, rect, 3, border_radius=8)
        
        txt = font.render(f"{job}", True, (255, 255, 255))
        screen.blit(txt, (bx + 10, GAME_HEIGHT + 25))
        
        cnt_col = (100, 255, 100) if cnt > 0 else (255, 100, 100)
        cnt_txt = font.render(f"x {cnt}", True, cnt_col)
        screen.blit(cnt_txt, (bx + 10, GAME_HEIGHT + 50))
        bx += 140

# --- MAIN ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lemmings HD - [R] New Map [SPACE] Pause")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 16, bold=True)
    
    terrain = create_level()
    lemmings = []
    spawn_timer = 0
    spawned_count = 0
    saved_count = 0
    
    spawn_pt = (100, 100)
    exit_rect = pygame.Rect(850, 480, 60, 70)
    
    global selected_job, job_counts
    selected_job = None
    paused = False

    def reset_game():
        nonlocal terrain, lemmings, spawn_timer, spawned_count, saved_count, paused
        terrain = create_level()
        lemmings = []
        spawn_timer = 0
        spawned_count = 0
        saved_count = 0
        paused = False
        for k, v in INITIAL_COUNTS.items():
            job_counts[k] = v

    running = True
    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: paused = not paused
                if event.key == pygame.K_r: reset_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
        
        # UI
        if click and mouse_pos[1] > GAME_HEIGHT:
            bx = 50
            for job in jobs_list:
                rect = pygame.Rect(bx, GAME_HEIGHT + 15, 120, 70)
                if rect.collidepoint(mouse_pos):
                    selected_job = job
                bx += 140

        if not paused:
            if spawned_count < TOTAL_LEMMINGS:
                spawn_timer += 1
                if spawn_timer > SPAWN_RATE:
                    lemmings.append(Lemming(*spawn_pt))
                    spawned_count += 1
                    spawn_timer = 0
            
            hover_lem = None
            closest_dist = 50
            for lem in lemmings:
                if not lem.alive or lem.exited: continue
                dist = math.hypot(lem.x+LEM_WIDTH//2 - mouse_pos[0], lem.y+LEM_HEIGHT//2 - mouse_pos[1])
                if dist < closest_dist:
                    closest_dist = dist
                    hover_lem = lem
            
            if click and hover_lem and mouse_pos[1] < GAME_HEIGHT and selected_job:
                if selected_job in job_counts and job_counts[selected_job] > 0:
                    hover_lem.job = selected_job
                    hover_lem.build_steps = 0
                    hover_lem.bomber_timer = 300
                    job_counts[selected_job] -= 1
            
            for lem in lemmings:
                lem.update(terrain, lemmings)
                if lem.alive and not lem.exited and lem.rect().colliderect(exit_rect):
                    lem.exited = True
                    saved_count += 1
            
            for p in particles[:]:
                p.update()
                if p.life <= 0: particles.remove(p)

        screen.fill(BG_COLOR)
        for _ in range(5):
            sx, sy = random.randint(0, WIDTH), random.randint(0, GAME_HEIGHT)
            screen.set_at((sx, sy), (200, 200, 255))

        screen.blit(terrain, (0, 0))
        pygame.draw.rect(screen, (50, 50, 50), (spawn_pt[0]-20, spawn_pt[1]-10, 40, 10))
        
        pygame.draw.rect(screen, (100, 50, 0), exit_rect)
        pygame.draw.rect(screen, (0, 0, 0), exit_rect.inflate(-10, -10))
        pygame.draw.circle(screen, (100, 200, 255), (exit_rect.centerx, exit_rect.bottom-10), 10 + random.randint(0, 4))

        for lem in lemmings:
            if lem.alive and not lem.exited:
                highlight = False
                if not paused and mouse_pos[1] < GAME_HEIGHT:
                    dist = math.hypot(lem.x+LEM_WIDTH//2 - mouse_pos[0], lem.y+LEM_HEIGHT//2 - mouse_pos[1])
                    if dist < 30: highlight = True
                draw_lemming(screen, lem.x, lem.y, lem.job, lem.direction, lem.frame, highlight)
        
        for p in particles: p.draw(screen)

        draw_ui(screen, font)
        
        stats_txt = f"SAVED: {saved_count} | LEFT: {TOTAL_LEMMINGS - spawned_count}"
        if paused: stats_txt += " | PAUSED"
        info = font.render(stats_txt, True, (255, 255, 255))
        screen.blit(info, (20, 20))
        
        if selected_job and not paused:
            tip = font.render(selected_job, True, GOLD)
            screen.blit(tip, (mouse_pos[0]+15, mouse_pos[1]))

        pygame.display.flip()

if __name__ == "__main__":
    main()
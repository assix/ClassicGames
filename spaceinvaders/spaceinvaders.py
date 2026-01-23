import pygame
import sys
import random

# --- CONFIGURATION ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# COLORS
BG_COLOR = (10, 10, 15)
PLAYER_COL = (50, 255, 50)
ALIEN_COLS = [(255, 50, 50), (255, 150, 50), (50, 150, 255)]
BULLET_COL = (255, 255, 255)
SHIELD_COL = (50, 255, 200)

# BITMAPS (1 = Pixel, 0 = Empty)
ALIEN_TYPES = [
    [ # Squid
        [0,0,0,1,1,0,0,0],
        [0,0,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,0],
        [1,1,0,1,1,0,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,0,1,1,0,1,0],
        [1,0,0,0,0,0,0,1],
        [0,1,0,0,0,0,1,0]
    ],
    [ # Crab
        [0,0,1,0,0,1,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,1,1,1,1,0,0],
        [0,1,1,0,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,0,1,1,1,1,0,1],
        [1,0,1,0,0,1,0,1],
        [0,0,0,1,1,0,0,0]
    ],
    [ # Octopus
        [0,0,0,1,1,0,0,0],
        [0,0,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,0],
        [1,1,0,1,1,0,1,1],
        [1,1,1,1,1,1,1,1],
        [0,0,1,0,0,1,0,0],
        [0,1,0,1,1,0,1,0],
        [1,0,1,0,0,1,0,1]
    ]
]

class Laser:
    def __init__(self, x, y, speed_y):
        self.rect = pygame.Rect(x, y, 4, 10)
        self.speed_y = speed_y
        self.dead = False

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y < 0 or self.rect.y > HEIGHT:
            self.dead = True

    def draw(self, screen):
        pygame.draw.rect(screen, BULLET_COL, self.rect)

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - 20, HEIGHT - 60, 40, 20)
        self.speed = 5
        self.cooldown = 0
    
    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        
        if self.cooldown > 0: self.cooldown -= 1

    def shoot(self):
        if self.cooldown == 0:
            self.cooldown = 30
            return Laser(self.rect.centerx - 2, self.rect.top, -10)
        return None

    def draw(self, screen):
        # Turret shape
        pygame.draw.rect(screen, PLAYER_COL, self.rect)
        pygame.draw.rect(screen, PLAYER_COL, (self.rect.centerx-5, self.rect.top-8, 10, 8))

class Alien:
    def __init__(self, x, y, type_idx):
        self.x = x
        self.y = y
        self.type_idx = type_idx
        self.width = 32
        self.height = 32
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def update(self, speed_x):
        self.x += speed_x
        self.rect.x = int(self.x)

    def draw(self, screen, tick):
        # Animate toggle every 30 frames
        frame = (tick // 30) % 2 
        bitmap = ALIEN_TYPES[self.type_idx]
        color = ALIEN_COLS[self.type_idx]
        
        scale = 4
        for r, row in enumerate(bitmap):
            for c, pix in enumerate(row):
                if pix:
                    # Simple animation: offset legs slightly based on frame
                    draw_r = r
                    if r > 5 and frame == 1: 
                        # Erase leg pixels in frame 1? 
                        # Simplified: Just draw bitmap as is for now, pixel art is static in this array
                        pass
                    
                    pygame.draw.rect(screen, color, (self.x + c*scale, self.y + r*scale, scale, scale))

class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = random.randint(20, 40)
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            alpha = min(255, self.life * 10)
            s = pygame.Surface((4,4), pygame.SRCALPHA)
            pygame.draw.rect(s, (*self.color, alpha), (0,0,4,4))
            screen.blit(s, (self.x, self.y))

class Game:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.player = Player()
        self.aliens = []
        self.bullets = []
        self.enemy_bullets = []
        self.particles = []
        self.alien_speed = 1
        self.alien_dir = 1
        self.game_over = False
        self.score = 0
        
        # Spawn Aliens
        start_y = 50
        for row in range(5):
            for col in range(10):
                # Row 0=Type 0, 1-2=Type 1, 3-4=Type 2
                t = 0 if row == 0 else (1 if row < 3 else 2)
                self.aliens.append(Alien(50 + col * 50, start_y + row * 40, t))

    def update(self):
        if self.game_over: return

        keys = pygame.key.get_pressed()
        self.player.update(keys)
        
        if keys[pygame.K_SPACE]:
            b = self.player.shoot()
            if b: self.bullets.append(b)

        # Alien Movement
        move_down = False
        for a in self.aliens:
            a.update(self.alien_speed * self.alien_dir)
            if a.rect.right >= WIDTH - 20 or a.rect.left <= 20:
                move_down = True
        
        if move_down:
            self.alien_dir *= -1
            for a in self.aliens:
                a.y += 20
                a.rect.y = int(a.y)
                if a.rect.bottom >= HEIGHT - 100:
                    self.game_over = True # Invasion success

        # Alien Shooting
        if random.random() < 0.02 and self.aliens:
            shooter = random.choice(self.aliens)
            self.enemy_bullets.append(Laser(shooter.rect.centerx, shooter.rect.bottom, 5))

        # Bullets Update
        for b in self.bullets[:]:
            b.update()
            if b.dead: self.bullets.remove(b)
            # Hit Alien?
            for a in self.aliens[:]:
                if b.rect.colliderect(a.rect):
                    self.aliens.remove(a)
                    if b in self.bullets: self.bullets.remove(b)
                    self.spawn_explosion(a.rect.centerx, a.rect.centery, ALIEN_COLS[a.type_idx])
                    self.score += (3 - a.type_idx) * 10
                    self.alien_speed += 0.05 # Speed up
                    break
                    
        for b in self.enemy_bullets[:]:
            b.update()
            if b.dead: self.enemy_bullets.remove(b)
            # Hit Player?
            if b.rect.colliderect(self.player.rect):
                self.game_over = True
                self.spawn_explosion(self.player.rect.centerx, self.player.rect.centery, PLAYER_COL)

        # Particles
        for p in self.particles[:]:
            p.update()
            if p.life <= 0: self.particles.remove(p)

        if not self.aliens:
            self.reset() # Next wave logic could go here

    def spawn_explosion(self, x, y, color):
        for _ in range(15):
            self.particles.append(Particle(x, y, color))

    def draw(self, screen, font):
        screen.fill(BG_COLOR)
        
        if not self.game_over:
            self.player.draw(screen)
            for a in self.aliens: a.draw(screen, pygame.time.get_ticks())
            for b in self.bullets: b.draw(screen)
            for b in self.enemy_bullets: pygame.draw.rect(screen, (255, 100, 100), b.rect)
        
        for p in self.particles: p.draw(screen)

        # UI
        sc_txt = font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        screen.blit(sc_txt, (20, 20))

        if self.game_over:
            go_txt = font.render("GAME OVER - SPACE TO RESTART", True, (255, 0, 0))
            screen.blit(go_txt, (WIDTH//2 - go_txt.get_width()//2, HEIGHT//2))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Courier", 20, bold=True)
    
    game = Game()
    
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and game.game_over:
                if event.key == pygame.K_SPACE: game.reset()

        game.update()
        game.draw(screen, font)
        pygame.display.flip()

if __name__ == "__main__":
    main()
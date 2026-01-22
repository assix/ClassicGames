import pygame
import sys
import math
import random

# --- CONFIGURATION ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# COLORS
BG_COLOR = (10, 10, 15)
VECTOR_COL = (220, 220, 255)
BULLET_COL = (255, 50, 50)
SHIP_COL = (100, 255, 200)

# --- VECTOR MATH ---
def rotate_point(point, angle, origin=(0, 0)):
    """Rotate a point around an origin."""
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

class GameObject:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.angle = 0 # Radians
        self.radius = radius
        self.dead = False

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Screen Wrap
        if self.x < -self.radius: self.x = WIDTH + self.radius
        if self.x > WIDTH + self.radius: self.x = -self.radius
        if self.y < -self.radius: self.y = HEIGHT + self.radius
        if self.y > HEIGHT + self.radius: self.y = -self.radius

    def draw(self, screen):
        # Draw Hitbox (Debug)
        # pygame.draw.circle(screen, (50, 50, 50), (int(self.x), int(self.y)), self.radius, 1)
        pass

    def collides(self, other):
        dist = math.hypot(self.x - other.x, self.y - other.y)
        return dist < (self.radius + other.radius)

class Ship(GameObject):
    def __init__(self):
        super().__init__(WIDTH//2, HEIGHT//2, 15)
        self.angle = -math.pi / 2 # Point Up
        self.thrusting = False
        self.friction = 0.99

    def update(self):
        # Physics
        if self.thrusting:
            force = 0.15
            self.vel_x += math.cos(self.angle) * force
            self.vel_y += math.sin(self.angle) * force
        
        self.vel_x *= self.friction
        self.vel_y *= self.friction
        
        super().update()

    def draw(self, screen):
        # Tip, Rear Left, Rear Right, Indent
        pts = [
            (self.x + 20, self.y),
            (self.x - 15, self.y - 12),
            (self.x - 10, self.y),
            (self.x - 15, self.y + 12)
        ]
        # Rotate points
        rot_pts = [rotate_point(p, self.angle, (self.x, self.y)) for p in pts]
        
        col = SHIP_COL if not self.dead else (100, 100, 100)
        pygame.draw.polygon(screen, col, rot_pts, 2)
        
        # Thruster Flame
        if self.thrusting and not self.dead:
            flame_pts = [
                (self.x - 10, self.y),
                (self.x - 25, self.y),
                (self.x - 10, self.y + 6),
                (self.x - 10, self.y - 6)
            ]
            rot_flame = [rotate_point(p, self.angle, (self.x, self.y)) for p in flame_pts]
            # Random flicker
            if random.random() > 0.3:
                pygame.draw.polygon(screen, (255, 100, 0), rot_flame, 2)

class Asteroid(GameObject):
    def __init__(self, x, y, size_idx=3):
        # size_idx: 3=Large, 2=Med, 1=Small
        radius = size_idx * 15
        super().__init__(x, y, radius)
        self.size_idx = size_idx
        
        # Random Movement
        speed = (4 - size_idx) * 1.5
        heading = random.uniform(0, math.pi * 2)
        self.vel_x = math.cos(heading) * speed
        self.vel_y = math.sin(heading) * speed
        
        # Procedural Shape (Jagged Polygon)
        self.points = []
        num_points = random.randint(7, 12)
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            # Random variance in radius to make it look "rocky"
            r = radius * random.uniform(0.7, 1.3)
            self.points.append((math.cos(angle) * r, math.sin(angle) * r))
        
        self.rot_speed = random.uniform(-0.05, 0.05)

    def update(self):
        super().update()
        self.angle += self.rot_speed

    def draw(self, screen):
        # Transform points
        world_pts = []
        for lx, ly in self.points:
            # Rotate local point
            rx = lx * math.cos(self.angle) - ly * math.sin(self.angle)
            ry = lx * math.sin(self.angle) + ly * math.cos(self.angle)
            world_pts.append((self.x + rx, self.y + ry))
        
        pygame.draw.polygon(screen, VECTOR_COL, world_pts, 2)

class Bullet(GameObject):
    def __init__(self, x, y, angle):
        super().__init__(x, y, 2)
        speed = 10
        self.vel_x = math.cos(angle) * speed
        self.vel_y = math.sin(angle) * speed
        self.timer = 50 # Frames to live

    def update(self):
        super().update()
        self.timer -= 1
        if self.timer <= 0: self.dead = True

    def draw(self, screen):
        pygame.draw.circle(screen, BULLET_COL, (int(self.x), int(self.y)), 3)

# --- PIXEL FONT ENGINE ---
# (Keeping your consistent font style)
PIXEL_FONT = {
    '0':[0x70,0x88,0x98,0xA8,0xC8,0x88,0x70], '1':[0x20,0x60,0x20,0x20,0x20,0x20,0x70],
    '2':[0x70,0x88,0x08,0x30,0x40,0x80,0xF8], '3':[0xF8,0x08,0x10,0x30,0x08,0x88,0x70],
    '4':[0x10,0x30,0x50,0x90,0xF8,0x10,0x10], '5':[0xF8,0x80,0xF0,0x08,0x08,0x88,0x70],
    '6':[0x30,0x40,0x80,0xF0,0x88,0x88,0x70], '7':[0xF8,0x08,0x10,0x20,0x40,0x40,0x40],
    '8':[0x70,0x88,0x88,0x70,0x88,0x88,0x70], '9':[0x70,0x88,0x88,0x78,0x08,0x88,0x70],
    'G':[0x78,0x80,0x80,0x98,0x88,0x88,0x70], 'A':[0x70,0x88,0x88,0xF8,0x88,0x88,0x88],
    'M':[0x88,0xD8,0xA8,0xA8,0x88,0x88,0x88], 'E':[0xF8,0x80,0x80,0xF0,0x80,0x80,0xF8],
    'O':[0x70,0x88,0x88,0x88,0x88,0x88,0x70], 'V':[0x88,0x88,0x88,0x88,0x88,0x50,0x20],
    'R':[0xF0,0x88,0x88,0xF0,0xA0,0x90,0x88], ' ':[0x00]*7
}
def draw_text(surface, text, x, y, scale=2, color=(255,255,255), center=False):
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

# --- MAIN ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Asteroids Vector")
    clock = pygame.time.Clock()
    
    ship = Ship()
    asteroids = []
    bullets = []
    score = 0
    game_over = False
    
    # Spawn initial rocks
    for _ in range(4):
        # Spawn away from center
        while True:
            x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
            if math.hypot(x-WIDTH//2, y-HEIGHT//2) > 150:
                asteroids.append(Asteroid(x, y, 3))
                break

    while True:
        clock.tick(FPS)
        screen.fill(BG_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE: main() # Restart
                else:
                    if event.key == pygame.K_SPACE: # Shoot
                        # Muzzle tip
                        tip_x = ship.x + math.cos(ship.angle) * 20
                        tip_y = ship.y + math.sin(ship.angle) * 20
                        bullets.append(Bullet(tip_x, tip_y, ship.angle))
                    
                    if event.key == pygame.K_LSHIFT: # Hyperspace
                        ship.x = random.randint(0, WIDTH)
                        ship.y = random.randint(0, HEIGHT)
                        ship.vel_x = 0; ship.vel_y = 0

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: ship.angle -= 0.08
            if keys[pygame.K_RIGHT]: ship.angle += 0.08
            ship.thrusting = keys[pygame.K_UP]
            
            ship.update()
        
        # Updates & Collisions
        for b in bullets[:]:
            b.update()
            if b.dead: bullets.remove(b)
            else: b.draw(screen)

        for a in asteroids[:]:
            a.update()
            a.draw(screen)
            
            # Ship Collision
            if not game_over and ship.collides(a):
                game_over = True
                ship.dead = True
            
            # Bullet Collision
            for b in bullets[:]:
                if a.collides(b):
                    b.dead = True # Remove bullet
                    
                    # Split logic
                    if a in asteroids:
                        asteroids.remove(a)
                        score += 50 * (4 - a.size_idx)
                        if a.size_idx > 1:
                            asteroids.append(Asteroid(a.x, a.y, a.size_idx - 1))
                            asteroids.append(Asteroid(a.x, a.y, a.size_idx - 1))
                        break # Break bullet loop
        
        # Wave Respawn
        if len(asteroids) == 0:
            score += 1000
            for _ in range(5 + (score // 2000)): # Harder waves
                x, y = 0, 0
                if random.choice([True, False]): x = random.randint(0, WIDTH)
                else: y = random.randint(0, HEIGHT)
                asteroids.append(Asteroid(x, y, 3))

        if not game_over:
            ship.draw(screen)
        else:
            draw_text(screen, "GAME OVER", WIDTH//2, HEIGHT//2 - 20, 4, (255, 50, 50), center=True)
            draw_text(screen, "SPACE TO RESTART", WIDTH//2, HEIGHT//2 + 40, 2, center=True)

        draw_text(screen, str(score), 40, 30, 3)
        pygame.display.flip()

if __name__ == "__main__":
    main()
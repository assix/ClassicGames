import pygame
import random
import sys

# --- SETUP ---
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CARD_W, CARD_H = 100, 140
BG_COLOR = (0, 80, 0)     # Casino Green
CARD_COLOR = (250, 250, 250)
BLACK = (0, 0, 0)
RED = (220, 20, 20)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
BUTTON_COLOR = (40, 40, 40)
BUTTON_HOVER = (70, 70, 70)

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# --- VECTOR GRAPHICS ENGINE (Suits) ---
def draw_diamond(surface, x, y, size, color):
    half_w, half_h = size // 2, size * 0.6 
    points = [(x, y - half_h), (x + half_w, y), (x, y + half_h), (x - half_w, y)]
    pygame.draw.polygon(surface, color, points)

def draw_heart(surface, x, y, size, color):
    radius = size // 3.5
    c1_x, c1_y = x - radius * 0.9, y - radius * 0.4
    c2_x, c2_y = x + radius * 0.9, y - radius * 0.4
    pygame.draw.circle(surface, color, (int(c1_x), int(c1_y)), int(radius))
    pygame.draw.circle(surface, color, (int(c2_x), int(c2_y)), int(radius))
    triangle_points = [(x - radius * 1.7, c1_y + radius*0.5), (x + radius * 1.7, c2_y + radius*0.5), (x, y + size // 2)]
    pygame.draw.polygon(surface, color, triangle_points)

def draw_spade(surface, x, y, size, color):
    radius = size // 3.5
    offset_y = y - size * 0.05
    c1_x, c1_y = x - radius * 0.9, offset_y + radius * 0.4
    c2_x, c2_y = x + radius * 0.9, offset_y + radius * 0.4
    triangle_points = [(x, offset_y - size // 2), (x + radius * 1.7, c2_y - radius*0.5), (x - radius * 1.7, c1_y - radius*0.5)]
    pygame.draw.polygon(surface, color, triangle_points)
    pygame.draw.circle(surface, color, (int(c1_x), int(c1_y)), int(radius))
    pygame.draw.circle(surface, color, (int(c2_x), int(c2_y)), int(radius))
    stem_w, stem_top = size // 5, offset_y + radius * 0.8
    pygame.draw.polygon(surface, color, [(x, stem_top), (x + stem_w, y + size//2), (x - stem_w, y + size//2)])

def draw_club(surface, x, y, size, color):
    radius = size // 3.6
    offset_y = y - size * 0.08
    pygame.draw.circle(surface, color, (x, int(offset_y - radius)), int(radius))
    pygame.draw.circle(surface, color, (int(x - radius*0.9), int(offset_y + radius*0.6)), int(radius))
    pygame.draw.circle(surface, color, (int(x + radius*0.9), int(offset_y + radius*0.6)), int(radius))
    pygame.draw.circle(surface, color, (x, int(offset_y)), int(radius*0.8))
    stem_w, stem_top = size // 5, offset_y + radius * 0.5
    pygame.draw.polygon(surface, color, [(x, stem_top), (x + stem_w, y + size//2), (x - stem_w, y + size//2)])

def draw_suit_icon(surface, suit, x, y, size, color):
    if suit == 'Hearts': draw_heart(surface, x, y, size, color)
    elif suit == 'Diamonds': draw_diamond(surface, x, y, size, color)
    elif suit == 'Clubs': draw_club(surface, x, y, size, color)
    elif suit == 'Spades': draw_spade(surface, x, y, size, color)

# --- HIGH RES 5x7 PIXEL FONT ---
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
    ' ': [0x00] * 7,
    '(': [0x10, 0x20, 0x40, 0x40, 0x40, 0x20, 0x10],
    ')': [0x40, 0x20, 0x10, 0x10, 0x10, 0x20, 0x40],
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
    for char in text.upper():
        draw_pixel_char(surface, char, cursor_x, y, scale, color)
        cursor_x += (6 * scale) # 5 width + 1 spacing

# --- GAME LOGIC ---
class Card:
    def __init__(self, rank, suit, hidden=False):
        self.rank = rank
        self.suit = suit
        self.hidden = hidden
        self.color = RED if suit in ['Hearts', 'Diamonds'] else BLACK
        
        if rank in ['J', 'Q', 'K']: self.val = 10
        elif rank == 'A': self.val = 11
        else: self.val = int(rank)

class Deck:
    def __init__(self):
        self.cards = [Card(r, s) for s in SUITS for r in RANKS]
        random.shuffle(self.cards)
    
    def draw(self):
        return self.cards.pop()

def calculate_score(hand):
    score = sum(c.val for c in hand)
    aces = sum(1 for c in hand if c.rank == 'A')
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

# --- DRAWING ---
def draw_card(surface, card, x, y):
    rect = pygame.Rect(x, y, CARD_W, CARD_H)
    pygame.draw.rect(surface, CARD_COLOR, rect, border_radius=8)
    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=8)

    if card.hidden:
        # Pattern Back
        inner = pygame.Rect(x+4, y+4, CARD_W-8, CARD_H-8)
        pygame.draw.rect(surface, (150, 50, 50), inner, border_radius=6)
        pygame.draw.line(surface, WHITE, (x+4, y+4), (x+CARD_W-4, y+CARD_H-4), 2)
        pygame.draw.line(surface, WHITE, (x+CARD_W-4, y+4), (x+4, y+CARD_H-4), 2)
    else:
        # Rank & Suit (Corner)
        draw_pixel_string(surface, card.rank, x+6, y+6, 2, card.color)
        draw_suit_icon(surface, card.suit, x+12, y+28, 12, card.color)
        
        # Center Suit
        draw_suit_icon(surface, card.suit, x+CARD_W//2, y+CARD_H//2, 30, card.color)
        
        # Bottom Right Rank
        draw_pixel_string(surface, card.rank, x+CARD_W-22, y+CARD_H-22, 2, card.color)

def draw_button(surface, text, x, y, w, h, hover=False):
    col = BUTTON_HOVER if hover else BUTTON_COLOR
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, col, rect, border_radius=6)
    pygame.draw.rect(surface, WHITE, rect, 2, border_radius=6)
    
    # Center text
    text_len = len(text)
    char_w = 6 * 2
    text_px_w = text_len * char_w
    
    draw_pixel_string(surface, text, x + (w-text_px_w)//2, y + 16, 2, WHITE)
    return rect

# --- MAIN LOOP ---
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Blackjack 21")
    clock = pygame.time.Clock()

    deck = Deck()
    player_hand = []
    dealer_hand = []
    
    # Game States: BETTING, PLAYING, DEALER_TURN, GAME_OVER
    state = "BETTING"
    outcome = ""
    
    # Buttons - INCREASED WIDTH FOR DEAL BUTTON
    btn_hit = pygame.Rect(SCREEN_WIDTH - 280, SCREEN_HEIGHT - 100, 120, 50)
    btn_stand = pygame.Rect(SCREEN_WIDTH - 140, SCREEN_HEIGHT - 100, 120, 50)
    btn_deal = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 25, 200, 50) # Width increased to 200

    # Function to trigger HIT action
    def action_hit():
        nonlocal state, outcome
        player_hand.append(deck.draw())
        if calculate_score(player_hand) > 21:
            state = "GAME_OVER"
            outcome = "BUST! YOU LOSE"

    # Function to trigger STAND action
    def action_stand():
        nonlocal state
        state = "DEALER_TURN"
        dealer_hand[0].hidden = False

    # Function to trigger DEAL action
    def action_deal():
        nonlocal state, deck, player_hand, dealer_hand, outcome
        deck = Deck()
        player_hand = [deck.draw(), deck.draw()]
        dealer_hand = [deck.draw(), deck.draw()]
        dealer_hand[0].hidden = True
        
        p_score = calculate_score(player_hand)
        if p_score == 21:
            dealer_hand[0].hidden = False
            d_score = calculate_score(dealer_hand)
            if d_score == 21:
                state = "GAME_OVER"; outcome = "PUSH"
            else:
                state = "GAME_OVER"; outcome = "BLACKJACK! WIN"
        else:
            state = "PLAYING"

    while True:
        mouse_pos = pygame.mouse.get_pos()
        hover_hit = btn_hit.collidepoint(mouse_pos)
        hover_stand = btn_stand.collidepoint(mouse_pos)
        hover_deal = btn_deal.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            # --- MOUSE CLICKS ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "BETTING":
                    if hover_deal: action_deal()
                
                elif state == "PLAYING":
                    if hover_hit: action_hit()
                    elif hover_stand: action_stand()
                
                elif state == "GAME_OVER":
                    if hover_deal: action_deal() # Re-use deal button pos for Play Again
            
            # --- KEYBOARD SHORTCUTS ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if state == "BETTING" or state == "GAME_OVER":
                        action_deal()
                
                if state == "PLAYING":
                    if event.key == pygame.K_h:
                        action_hit()
                    elif event.key == pygame.K_s:
                        action_stand()

        # Dealer Logic
        if state == "DEALER_TURN":
            pygame.display.flip()
            pygame.time.delay(600)
            d_score = calculate_score(dealer_hand)
            if d_score < 17:
                dealer_hand.append(deck.draw())
            else:
                # End Game
                p_score = calculate_score(player_hand)
                if d_score > 21:
                    outcome = "DEALER BUST! WIN"
                elif d_score > p_score:
                    outcome = "DEALER WINS"
                elif d_score < p_score:
                    outcome = "YOU WIN"
                else:
                    outcome = "PUSH"
                state = "GAME_OVER"

        # --- DRAWING ---
        screen.fill(BG_COLOR)
        
        # Dealer Area
        draw_pixel_string(screen, "DEALER", 50, 50, 2, WHITE)
        for i, card in enumerate(dealer_hand):
            draw_card(screen, card, 50 + i * (CARD_W + 10), 90)
            
        if state != "BETTING" and not dealer_hand[0].hidden:
            d_score = calculate_score(dealer_hand)
            draw_pixel_string(screen, str(d_score), 200, 50, 2, YELLOW)

        # Player Area
        draw_pixel_string(screen, "PLAYER", 50, 360, 2, WHITE)
        for i, card in enumerate(player_hand):
            draw_card(screen, card, 50 + i * (CARD_W + 10), 400)
            
        if state != "BETTING":
            p_score = calculate_score(player_hand)
            draw_pixel_string(screen, str(p_score), 200, 360, 2, YELLOW)

        # UI Controls
        if state == "BETTING":
            draw_button(screen, "DEAL (SPACE)", btn_deal.x, btn_deal.y, btn_deal.w, btn_deal.h, hover_deal)
        
        elif state == "PLAYING":
            draw_button(screen, "HIT (H)", btn_hit.x, btn_hit.y, btn_hit.w, btn_hit.h, hover_hit)
            draw_button(screen, "STAND (S)", btn_stand.x, btn_stand.y, btn_stand.w, btn_stand.h, hover_stand)
            
        elif state == "GAME_OVER":
            # Draw outcome with larger scale
            draw_pixel_string(screen, outcome, SCREEN_WIDTH//2 - (len(outcome)*9), SCREEN_HEIGHT//2 - 50, 3, YELLOW)
            draw_button(screen, "AGAIN (SPACE)", btn_deal.x, btn_deal.y, btn_deal.w, btn_deal.h, hover_deal)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()

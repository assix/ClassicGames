import pygame
import sys
import random
import math

# --- CONFIGURATION ---
COLUMN_COUNT = 7
ROW_COUNT = 6
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 5)

WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE # Extra row for header

# COLORS
BLUE = (0, 0, 255)
BLACK = (20, 20, 30)
RED = (255, 50, 50)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (255, 255, 255, 50) # Transparent highlight

# CONSTANTS
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4

# --- PIXEL FONT ENGINE (No System Dependencies) ---
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
    'V': [0x88, 0x88, 0x88, 0x88, 0x88, 0x50, 0x20],
    'W': [0x88, 0x88, 0x88, 0xA8, 0xA8, 0xD8, 0x88],
    'Y': [0x88, 0x88, 0x50, 0x20, 0x20, 0x20, 0x20],
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
    '!': [0x20, 0x20, 0x20, 0x20, 0x00, 0x20, 0x00],
}

def draw_text(surface, text, x, y, scale=3, color=WHITE, center=False):
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
class Board:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
        self.game_over = False
        self.winner = None
        self.turn = random.choice([PLAYER, AI])

    def drop_piece(self, row, col, piece):
        self.grid[row][col] = piece

    def is_valid_location(self, col):
        return self.grid[ROW_COUNT-1][col] == EMPTY

    def get_next_open_row(self, col):
        for r in range(ROW_COUNT):
            if self.grid[r][col] == EMPTY:
                return r
        return None

    def winning_move(self, piece):
        # Horizontal
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if self.grid[r][c] == piece and self.grid[r][c+1] == piece and self.grid[r][c+2] == piece and self.grid[r][c+3] == piece:
                    return True
        # Vertical
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if self.grid[r][c] == piece and self.grid[r+1][c] == piece and self.grid[r+2][c] == piece and self.grid[r+3][c] == piece:
                    return True
        # Pos Diag
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if self.grid[r][c] == piece and self.grid[r+1][c+1] == piece and self.grid[r+2][c+2] == piece and self.grid[r+3][c+3] == piece:
                    return True
        # Neg Diag
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if self.grid[r][c] == piece and self.grid[r-1][c+1] == piece and self.grid[r-2][c+2] == piece and self.grid[r-3][c+3] == piece:
                    return True
        return False

# --- AI ---
class AI:
    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

        if window.count(piece) == 4: score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1: score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2: score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1: score -= 4

        return score

    def score_position(self, board, piece):
        score = 0
        grid = board.grid
        
        # Center column preference
        center_array = [i[COLUMN_COUNT//2] for i in grid]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Horizontal
        for r in range(ROW_COUNT):
            row_array = grid[r]
            for c in range(COLUMN_COUNT-3):
                window = row_array[c:c+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Vertical
        for c in range(COLUMN_COUNT):
            col_array = [grid[r][c] for r in range(ROW_COUNT)]
            for r in range(ROW_COUNT-3):
                window = col_array[r:r+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Positive Diagonal
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [grid[r+i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        # Negative Diagonal
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [grid[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def is_terminal_node(self, board):
        return board.winning_move(PLAYER_PIECE) or board.winning_move(AI_PIECE) or len(self.get_valid_locations(board)) == 0

    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if board.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        
        if depth == 0 or is_terminal:
            if is_terminal:
                if board.winning_move(AI_PIECE): return (None, 100000000000000)
                elif board.winning_move(PLAYER_PIECE): return (None, -10000000000000)
                else: return (None, 0)
            else:
                return (None, self.score_position(board, AI_PIECE))

        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = board.get_next_open_row(col)
                temp_board = copy.deepcopy(board)
                temp_board.drop_piece(row, col, AI_PIECE)
                new_score = self.minimax(temp_board, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta: break
            return column, value
        else:
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = board.get_next_open_row(col)
                temp_board = copy.deepcopy(board)
                temp_board.drop_piece(row, col, PLAYER_PIECE)
                new_score = self.minimax(temp_board, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta: break
            return column, value

# --- RENDERING ---
def draw_board(screen, board):
    # Draw Background
    pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARE_SIZE))
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # Draw Blue Box (The Board structure)
            rect = (c*SQUARE_SIZE, (r+1)*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, BLUE, rect)
            
            # Draw Holes (Black if empty, Color if filled)
            circle_pos = (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int((r+1)*SQUARE_SIZE+SQUARE_SIZE/2))
            
            # Note: Pygame coordinates start top-left.
            # Our grid[0][0] is bottom-left conceptually for logic, but top-left in storage makes graphics easier.
            # Standard Connect 4 storage: grid[row][col] where row 0 is bottom.
            # To draw correctly we must invert row index.
            
            piece = board.grid[r][c] # Draw inverted? No, let's map logic to visual.
            # Visual Row 0 (Top) -> Logic Row 5. Visual Row 5 (Bottom) -> Logic Row 0.
            # Let's actually adjust the draw loop to match logic.
            
            logic_row = ROW_COUNT - 1 - r
            piece = board.grid[logic_row][c]
            
            if piece == EMPTY: pygame.draw.circle(screen, BLACK, circle_pos, RADIUS)
            elif piece == PLAYER_PIECE: pygame.draw.circle(screen, RED, circle_pos, RADIUS)
            elif piece == AI_PIECE: pygame.draw.circle(screen, YELLOW, circle_pos, RADIUS)

    # Highlight top bar piece
    if board.turn == PLAYER and not board.game_over:
        pos_x = pygame.mouse.get_pos()[0]
        # Snap to column
        col = int(math.floor(pos_x / SQUARE_SIZE))
        if 0 <= col < COLUMN_COUNT:
            cx = int(col * SQUARE_SIZE + SQUARE_SIZE/2)
            pygame.draw.circle(screen, RED, (cx, int(SQUARE_SIZE/2)), RADIUS)

def draw_game_over(screen, winner_text):
    pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARE_SIZE))
    draw_text(screen, winner_text, WIDTH//2, 25, 3, center=True)

# --- MAIN ---
import copy

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect Four AI")
    clock = pygame.time.Clock()
    
    board = Board()
    ai = AI()
    
    while True:
        clock.tick(30)
        
        # AI Turn
        if board.turn == AI and not board.game_over:
            draw_board(screen, board)
            pygame.display.flip()
            
            # Simple "Thinking" animation delay
            pygame.time.wait(500)
            
            col, minimax_score = ai.minimax(board, 5, -math.inf, math.inf, True)
            
            if board.is_valid_location(col):
                row = board.get_next_open_row(col)
                board.drop_piece(row, col, AI_PIECE)
                
                if board.winning_move(AI_PIECE):
                    board.game_over = True
                    board.winner = "AI WINS!"
                
                board.turn = PLAYER

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEMOTION:
                # Handled in draw_board for piece tracking
                pass 

            if event.type == pygame.MOUSEBUTTONDOWN and not board.game_over:
                if board.turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARE_SIZE))
                    
                    if board.is_valid_location(col):
                        row = board.get_next_open_row(col)
                        board.drop_piece(row, col, PLAYER_PIECE)
                        
                        if board.winning_move(PLAYER_PIECE):
                            board.game_over = True
                            board.winner = "YOU WIN!"
                        
                        board.turn = AI
            
            if event.type == pygame.MOUSEBUTTONDOWN and board.game_over:
                # Reset on click
                board = Board()

        draw_board(screen, board)
        
        if board.game_over:
            draw_game_over(screen, board.winner)
            
        pygame.display.flip()

if __name__ == "__main__":
    main()
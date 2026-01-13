import pygame
import sys
import copy

# --- SETUP ---
pygame.init()
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
RED = (200, 20, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CREAM = (245, 222, 179) 
WOOD = (100, 60, 30)    
BLUE = (0, 0, 255)      
GOLD = (255, 215, 0)    
GREY = (128, 128, 128)

# --- PIXEL FONT ENGINE (5x7) ---
PIXEL_FONT_5x7 = {
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
    'W': [0x88, 0x88, 0x88, 0xA8, 0xA8, 0xD8, 0x88],
    'Y': [0x88, 0x88, 0x50, 0x20, 0x20, 0x20, 0x20],
    ' ': [0x00] * 7,
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
        cursor_x += (6 * scale)

# --- GAME PIECE CLASS ---
class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - 10
        pygame.draw.circle(win, GREY, (self.x, self.y + 2), radius)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        pygame.draw.circle(win, GREY, (self.x, self.y), radius - 10, 2)
        if self.king:
            pygame.draw.circle(win, GOLD, (self.x, self.y), radius // 2, 5)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

# --- BOARD LOGIC ---
class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def draw_squares(self, win):
        win.fill(WOOD)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, CREAM, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        # AI heuristic: Score based on piece count and kings
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE: self.white_kings += 1
            else: self.red_kings += 1 

    def get_piece(self, row, col):
        return self.board[row][col]

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED: self.red_left -= 1
                else: self.white_left -= 1
    
    def winner(self):
        if self.red_left <= 0: return "AI WINS"
        elif self.white_left <= 0: return "RED WINS"
        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0: break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last: break
                elif skipped: moves[(r, left)] = last + skipped
                else: moves[(r, left)] = last
                if last:
                    if step == -1: row = max(r-3, -1)
                    else: row = min(r+3, ROWS)
                    moves.update(self._traverse_left(row, stop, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(row, stop, step, color, left+1, skipped=last))
                break
            elif current.color == color: break
            else: last = [current]
            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS: break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last: break
                elif skipped: moves[(r, right)] = last + skipped
                else: moves[(r, right)] = last
                if last:
                    if step == -1: row = max(r-3, -1)
                    else: row = min(r+3, ROWS)
                    moves.update(self._traverse_left(row, stop, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(row, stop, step, color, right+1, skipped=last))
                break
            elif current.color == color: break
            else: last = [current]
            right += 1
        return moves

# --- AI ALGORITHM (Minimax) ---
def minimax(board, depth, max_player, game):
    if depth == 0 or board.winner() != None:
        return board.evaluate(), board
    
    if max_player: # White (AI)
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(board, WHITE, game):
            evaluation = minimax(move, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    else: # Red (Human)
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(board, RED, game):
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move

def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board

def get_all_moves(board, color, game):
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = copy.deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    return moves

# --- MAIN GAME CONTROLLER ---
class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        
        # Turn Indicator
        txt = "RED (YOU)" if self.turn == RED else "AI THINKING"
        t_col = RED if self.turn == RED else WHITE
        draw_pixel_string(self.win, txt, 10, 10, 2, t_col)
        
        pygame.display.update()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Checkers vs AI")
    clock = pygame.time.Clock()
    game = Game(screen)

    run = True
    while run:
        clock.tick(60)

        # Check for AI Turn
        if game.turn == WHITE:
            # Simple AI Delay
            pygame.time.wait(100) 
            value, new_board = minimax(game.get_board(), 3, True, game)
            if new_board: # Make sure AI has a move
                game.ai_move(new_board)
            else:
                # No moves left for AI
                pass 

        winner = game.board.winner()
        if winner:
            screen.fill(WOOD)
            draw_pixel_string(screen, winner, 200, 350, 5, GOLD)
            draw_pixel_string(screen, "SPACE TO RESET", 220, 450, 3, WHITE)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game.reset()
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and game.turn == RED:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
# Python Classic Game Collection 🃏

A collection of classic games implemented in Python using **Pygame** (Tested across multiple platforms using python 3.12). 
These projects focus on procedural graphics (no external assets required) and smooth, non-blocking game loops.

## 📂 The Games

| Game | Description | Command to Play |
| :--- | :--- | :--- |
| **[Crazy 8s](./crazy8)** | The classic shedding card game. Match rank or suit. 8s are wild. | `python3 crazy8/crazy8.py` |
| **[UNO](./uno)** | The famous color-matching game with Action cards (Skip, Reverse, Draw 2/4). | `python3 uno/uno.py` |
| **[Solitaire](./solitaire)** | The famous Solitaire game featuring procedural vector graphics and zero external assets. | `python3 solitaire/solitaire.py` |
| **[BlackJack](./blackjack)** | The famous casino style Blackjack game with betting, split/stand logic. | `python3 blackjack/blackjack.py` |
| **[Brick Breaker](./BrickBreaker)** | Classic arcade game with dynamic physics, 5 lives, and randomized layouts. | `python3 BrickBreaker/main.py` |
| **[Checkers](./checkers)** | Classic checkers strategy board game featuring Minimax AI and move validation. | `python3 checkers/checkers.py` |
| **[Backgammon](./backgammon)** | Classic Backgammon strategy board game race. Features Heuristic AI and bearing off logic. | `python3 backgammon/backgammon.py` |
| **[Risk](./risk)** | Classic Risk strategy board game. Features Heuristic AI and bearing off logic. | `python3 risk/risk.py` |
| **[Go](./go)** | Classic strategy board game Go (9x9). Features Liberties, Ko rule, Territory scoring, and AI. | `python3 go/go.py` |
| **[Chess](./chess)** | Pro Chess with Vector Graphics, Minimax AI, and Undo feature. | `python3 chess/chess.py` |
| **[Tic Tac Toe](./tictactoe)** | Classic Tic-Tac-Toe with unbeatable Minimax AI. | `python3 tictactoe/tictactoe.py` |
| **[Connect Four](./connectfour)** | Classic Connect four strategy game. Connect 4 tokens to win against a smart Minimax AI. | `python3 connectfour/connectfour.py` |
| **[Sudoku](./sudoku)** | Infinite Sudoku generator. Features error highlighting and smart cell selection. | `python3 sudoku/sudoku.py` |
| **[Othello](./othello)**  | Classic Othello (Reversi) strategy game. Features Undo, Hint system, and positional AI. | `python3 othello/othello.py` |
| **[1D Chess](./1dchess)** | A unique 1D chess variant played on a single strip. Features King, Rook, and Knight mechanics. AI uses a Greedy Heuristic algorithm (King > Capture > Advance). | `python3 1dchess/1dchess.py` |
| **[Stratego](./stratego)** | Classic strategy game Stratego. Features a Greedy Heuristic AI that evaluates moves based on Rank Differential and Scout Probing logic. | `python3 stratego/stratego.py` |
| **[Minesweeper](./minesweeper)** | Classic logic puzzle. Features recursive flood-fill, first-click safety, and 'Chording' (double-click to clear neighbors). | `python3 minesweeper/minesweeper.py` |
| **[Snake](./snake)** | Neon-styled Snake game. Features smooth input buffering, dash mechanic (Shift), and local high score tracking. | `python3 snake/snake.py` |
| **[Asteroids](./asteroids)** | Vector physics shooter. Features procedural asteroid shapes, inertia mechanics, and splitting rocks. | `python3 asteroids/asteroids.py` |


*(More games coming soon...)*

## 🛠️ Setup

1. **Clone the repository:**
   `git clone https://github.com/assix/ClassicGames.git;
   cd ClassicGames`

2. **Install Dependencies:**
   You only need Pygame for all games in this collection.
   `pip3 install -r requirements.txt`

## 📜 License
MIT License - see [LICENSE](LICENSE) for details.

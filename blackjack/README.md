# Blackjack 21 (Python/Pygame) ♠️

A clean, casino-style implementation of **Blackjack** built entirely in Python.

Like other games in this collection, this project requires **zero external image assets**. All graphics—including the card suits, the card backs, and even the text font—are drawn programmatically using a custom vector graphics engine and a high-resolution pixel font system.

## ✨ Features

- **Procedural Graphics:** Suits (Hearts, Spades, etc.) are drawn using geometric primitives. No PNGs or JPEGs required.
- **Custom Pixel Font:** Uses a sharp 5x7 pixel font engine to render text, bypassing system font dependencies (fixing compatibility for macOS/Linux).
- **Full Game Loop:** Includes Betting, Player Turn (Hit/Stand), Dealer Turn (AI logic), and Win/Loss/Push detection.
- **Keyboard Support:** Play efficiently using keyboard shortcuts.

## 🛠️ Installation & Run

🛠️ Prerequisites

You need Python 3.x and the Pygame library installed.
On Ubuntu / Linux (Debian-based)

```bash sudo apt update sudo apt install python3-pip pip3 install pygame ```
On macOS / Windows

```bash pip install pygame ```
🚀 Installation & Usage

    Clone the repository: ```bash git clone https://github.com/assix/ClassicGames.git cd ClassicGames/blackjack ```

    Run the game: ```bash python3 blackjack.py ```

🕹️ How to Play

The goal is to beat the Dealer's hand without going over 21.
Controls
Action	Mouse	Keyboard
Deal / Replay	Click DEAL	SPACE
Hit	Click HIT	H
Stand	Click STAND	S
Rules Implemented

    Blackjack: Ace + 10-value card on the first deal pays out immediately (unless Dealer also has Blackjack).

    Dealer Rules: Dealer must Hit on 16 and Stand on 17.

    Push: If Player and Dealer have the same total, the bet is returned.

    Bust: If you exceed 21, you lose immediately.

🎨 Under the Hood

To ensure this game runs on any system (even those with broken font libraries), blackjack.py includes:

    Vector Suit Engine: Mathematical functions to draw the 4 suits using pygame.draw.polygon.

    5x7 Bitmapped Font: A dictionary containing binary maps for the entire alphabet (A-Z) and numbers, rendered pixel-by-pixel.

📄 License

MIT License - Free to use, modify, and distribute.

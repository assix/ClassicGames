# Othello (Reversi) ⚪⚫

A high-fidelity Python implementation of the classic strategy board game **Othello** (also known as Reversi). 

This version features a **smart Minimax AI** that understands positional strategy (like the value of corners), a hint system for learning, and "vector-style" procedural graphics that require no external assets.

## ✨ Features
* **🧠 Minimax AI:** Uses Alpha-Beta pruning and a positional weight matrix (prioritizing corners and stable edges) to play competitively.
* **💡 Hint System:** Press `H` to see the optimal move calculated by the AI (highlighted in Gold).
* **↩️ Undo System:** Press `U` to undo the last round (reverts both the AI's move and your last move).
* **🎨 Procedural Graphics:** All assets (board, pieces, text) are drawn via code using Pygame primitives and a custom pixel-font engine. No image files required.
* **🚦 Visual Guides:** Valid moves are highlighted with transparent markers to help beginners.

## 🎮 How to Play
1.  **Objective:** Trap the opponent's pieces between two of yours (horizontally, vertically, or diagonally) to flip them to your color.
2.  **Winning:** The game ends when the board is full or neither player can move. The player with the most pieces on the board wins.
3.  **Strategy:** * **Corners** are invulnerable; try to capture them.
    * Avoid placing pieces adjacent to corners early in the game, as this gives the AI access to the corner.

## ⌨️ Controls
| Key / Action | Function |
|---|---|
| **Left Click** | Place a piece (Black) |
| **H** | **Hint** (Show best move) |
| **U** | **Undo** last round |
| **Space** | Restart Game (when Game Over) |

## 🚀 Running the Game
**Requirements:** Python 3.x, Pygame

```bash
# 1. Install Pygame
pip3 install pygame

# 2. Run the game
python3 othello.py

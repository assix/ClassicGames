# Minesweeper 💣

A high-performance Python implementation of the classic logic puzzle. This version features a modern **"First-Click Safe"** guarantee, recursive flood-fill for instant clearing, and advanced **Chording mechanics** for speedrunning.

## ✨ Features
* **🛡️ First-Click Safety:** The map is generated *after* your first click, ensuring you never hit a mine on start.
* **🌊 Recursive Flood Fill:** Clicking an empty "0" cell instantly clears all connected empty territory.
* **🎹 Chording (Double Click):** Advanced mechanics for experienced players. Click both mouse buttons on a number to auto-clear neighbors.
* **🎨 Procedural GUI:** Features a custom "3D" button engine and pixel-font rendering written entirely in code.

## 🎮 How to Play
1.  **Objective:** Clear the board without detonating any mines.
2.  **Numbers:** A number represents how many mines are adjacent to that square (1-8).
3.  **Winning:** The game is won when all non-mine cells are revealed.

## ⌨️ Controls
| Action | Input | Description |
|---|---|---|
| **Reveal** | Left Click | Open a square. |
| **Flag** | Right Click | Mark a square as a potential mine. |
| **Chord** | Left + Right Click<br>(or Middle Click) | **If flags match number:** Reveals all surrounding squares.<br>**If flags don't match:** Highlights surrounding area (to help you visualize). |
| **Reset** | Click the Face 🙂 | Restart the game instantly. |

## 🚀 Running the Game
**Requirements:** Python 3.x, Pygame

```bash
# 1. Install Pygame
pip3 install pygame

# 2. Run the game
python3 minesweeper.py

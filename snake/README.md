# Snake 🐍

A retro-futuristic implementation of the classic arcade game. This version focuses on **responsive controls** and visual flair, moving away from the rigid grid-movement of older versions to feel smoother and more modern.

## ✨ Features
* **🕹️ Input Buffering:** The movement logic stores your next turn, preventing the frustration of dying because you pressed two keys too quickly (the "suicide turn" prevention).
* **✨ Neon Glow:** Procedural alpha-blending creates a retro CRT glow effect around the food and snake segments.
* **💨 Dash Mechanic:** Hold `SHIFT` to double the game speed—risking a crash for faster food collection.
* **🏆 Persistence:** Automatically saves your **High Score** to a local file (`snake_highscore.txt`) so your records survive between sessions.

## 🎮 How to Play
1.  **Objective:** Eat the glowing red food to grow longer.
2.  **Failure:** The game ends if you hit the walls or your own tail.
3.  **Strategy:** Use the Dash button on long straightaways to minimize travel time, but release it before turning corners.

## ⌨️ Controls
| Key | Action |
|---|---|
| **Arrow Keys** | Change Direction |
| **Shift (Hold)** | **Dash** (2x Speed) |
| **P** | Pause Game |
| **Space** | Restart (on Game Over) |

## 🚀 Running the Game
**Requirements:** Python 3.x, Pygame

```bash
# 1. Install Pygame
pip3 install pygame

# 2. Run the game
python3 snake.py

# Tetris 🧱

A high-fidelity, hardware-accelerated Python clone of the world's most popular puzzle game. This implementation features a custom **Procedural 3D Rendering Engine** that generates beveled, illuminated blocks in real-time without external assets.


## ✨ Key Features
* **Rendering:** Custom "2.5D" drawing engine with dynamic highlights, shadows, and alpha transparency.
* **Ghost Piece:** A transparent guide shows exactly where your block will land, reducing misdrops.
* **SRS-Style Mechanics:** Includes "Super Rotation System" basics, allowing wall kicks in standard situations.
* ** DAS (Delayed Auto Shift):** Professional-grade input handling. Holding a key moves the piece instantly once, waits, and then zooms across—vital for high-level play.
* **Next Queue:** Preview the upcoming tetromino to plan your strategy.

## 🎮 Controls
| Key | Action |
| :--- | :--- |
| **Arrow Left / Right** | Move Piece |
| **Arrow Up** | Rotate Clockwise |
| **Arrow Down** | Soft Drop (Fall Faster) |
| **Spacebar** | **Hard Drop** (Instant Lock) |

## 📊 Scoring System
| Action | Points |
| :--- | :--- |
| **Soft Drop** | 1 point per cell |
| **Single Line** | 100 x Level |
| **Double Line** | 300 x Level |
| **Triple Line** | 500 x Level |
| **Tetris (4 Lines)** | 800 x Level |

## 🛠️ Installation & Run
**Requirements:** Python 3.x, Pygame

```bash
# 1. Install Dependencies
pip3 install -r requirements.txt

# 2. Run the Game
python3 tetris.py
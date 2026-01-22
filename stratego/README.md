# Stratego Commander 🔴🔵

A high-fidelity, remastered implementation of the classic board game **Stratego**, featuring a "Turtle Defense" AI, vector-based military graphics, and a combat statistics dashboard.

## ✨ Features
* **🧠 Smart AI (The "Turtle" Strategy):**
    * **Setup:** The AI automatically places its Flag in the back row and surrounds it with Bombs to create a defensive "kill zone."
    * **Decision Making:** Uses a **Greedy Heuristic algorithm** that aggressively hunts low-rank pieces while protecting its Marshal and General. It calculates rank differentials to determine the safest attacks.
* **📊 Live Stats Dashboard:** A sidebar tracks every captured piece in real-time, showing exactly how many units of each rank the enemy has lost (essential for card counting).
* **🎨 Vector Military Graphics:** Procedural icons for every rank (e.g., Spy trench coats, Miner pickaxes, Marshal stars) drawn directly in code—no external image assets required.
* **⚔️ Combat Cutscenes:** When pieces collide, the action pauses to display a "Combat Card" overlay, revealing the identities and declaring the winner.
* **🛰️ Spy Satellite (Hint System):** A cheat mechanic that allows you to scan and reveal any hidden enemy piece.

## 🎮 How to Play
1.  **Objective:** Capture the enemy **Flag (F)** or eliminate all their movable pieces.
2.  **Movement:** Pieces move 1 square orthogonally. **Scouts (2)** can move any distance in a straight line.
3.  **Combat:** When you move onto an enemy square, ranks are compared:
    * **Higher Rank Wins** (10 beats 9, etc.).
    * **Tie:** Both pieces are removed.
    * **Exceptions:**
        * **Spy (S)** defeats the **Marshal (10)** if the Spy attacks first.
        * **Miner (3)** defuses (defeats) **Bombs (B)**.
4.  **Immovable:** Flags and Bombs cannot move.

## 🔢 Ranks & Units
| Rank | Name | Count | Special Ability |
|---|---|---|---|
| **F** | Flag | 1 | Game ends if captured. Cannot move. |
| **B** | Bomb | 6 | Defeats anything except Miners. Cannot move. |
| **S** | Spy | 1 | Defeats Marshal (10) if attacking. |
| **10** | Marshal | 1 | Highest strength. |
| **9** | General | 1 | |
| **8** | Colonel | 2 | |
| **7** | Major | 3 | |
| **6** | Captain | 4 | |
| **5** | Lieutenant | 4 | |
| **4** | Sergeant | 4 | |
| **3** | Miner | 5 | Defeats Bombs. |
| **2** | Scout | 8 | Moves unlimited distance. |

## ⌨️ Controls
| Key / Action | Function |
|---|---|
| **Left Click** | Select and Move pieces |
| **H** | **Hint Mode** (Toggle Spy Satellite) |
| **1 / 2 / 3** | Select Difficulty (Menu) |
| **Space** | Start Game / Return to Menu |

## 🚀 Running the Game
**Requirements:** Python 3.x, Pygame

```bash
# 1. Install Pygame
pip3 install pygame

# 2. Run the game
python3 stratego.py

# Queens Logic Puzzle 👑

A sophisticated logic puzzle game implemented in Python (Pygame). Inspired by the popular LinkedIn game and "Star Battle" puzzles, this project features **procedural level generation**, **graph theory algorithms**, and **Minesweeper-style smart controls**.

## 🎮 Game Overview
The goal is simple but deep: Place **$N$ Queens** on an **$N \times N$ grid** (where $N$ is 6, 8, or 10).

### The 4 Golden Rules:
1.  **One per Row:** Every row must have exactly one Queen.
2.  **One per Column:** Every column must have exactly one Queen.
3.  **One per Color:** Every colored region must have exactly one Queen.
4.  **No Touching:** Queens cannot touch each other, **not even diagonally**.

---

## ✨ Key Features

### 🧠 Procedural Level Generation
Unlike static puzzle games, this engine generates **infinite unique levels** on the fly.
* **Backtracking Solver:** Ensures every generated board has at least one valid solution.
* **Organic Region Growth:** Uses a randomized flood-fill algorithm to grow color regions from solution seeds.
* **Contiguity Enforcement:** A post-processing pass merges isolated "islands" to guarantee that every color region is a single, solid shape.

### 🎚️ Smart Difficulty Scaling
* **Beginner ($6 \times 6$):** Uses **Progressive Constraint Logic**. The board always contains a "Region of Size 1" (a forced move), which unlocks a "Region of Size 2", creating a learnable chain reaction.
* **Intermediate ($8 \times 8$):** Standard logic puzzle difficulty.
* **Expert ($10 \times 10$):** Large board with complex, sprawling regions requiring deep deduction.

### ⚡ Pro Controls (Minesweeper Style)
Designed for speed and ease of use.
* **Auto-Marking (Chording):** Holding **Left + Right Click** on a placed Queen instantly marks all illegal squares (row, col, diagonals, region) with an **X**.
* **Smart Undo:** Tracks your history so you can experiment without fear.
* **Intelligent Hints:**
    * **Left-Click Hint:** Auto-fills a random correct Queen.
    * **Right-Click Hint:** Allows *you* to select a specific cell to reveal.

---

## 🕹️ Controls

| Action | Input |
| :--- | :--- |
| **Place Queen** | \`Left Click\` |
| **Place Marker (X)** | \`Right Click\` |
| **Auto-Mark Illegal (Chord)** | \`Left + Right Click\` (or \`Double Click\`) on a Queen |
| **Undo Move** | Click **Undo** button |
| **Get Hint** | Click **Hint** button |
| **Targeted Hint** | \`Right Click\` Hint button $\to$ Click any grid cell |
| **New Level** | Click **New Game** |

---

## 🛠️ Installation & Run

1.  **Install Pygame** (if you haven't already):
    \`\`\`bash
    pip3 install pygame
    \`\`\`

2.  **Run the Game:**
    \`\`\`bash
    python3 queens.py
    \`\`\`

---

## 🧩 Algorithms Used

### 1. The Generator (Backtracking)
The game first solves the $N$-Queens problem (with the added constraint of no touching neighbors) to create a hidden "Solution Grid."

### 2. The Partitioning (Flood Fill)
It then uses the solution coordinates as "Seeds." It grows regions outward from these seeds. 
* *Constraint:* A region cannot consume a cell if it would make it impossible for another region to expand.

### 3. The Cleanup (Graph Theory)
After generation, the board is scanned for non-contiguous regions (split islands). A **Connected Components** algorithm identifies these fragments and merges them into the largest neighboring region, ensuring a clean, solvable visual puzzle.

---

## 📜 License
MIT License - Free to use and modify.

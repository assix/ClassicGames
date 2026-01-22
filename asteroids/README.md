# Asteroids Vector ☄️

A high-fidelity recreation of the 1979 arcade classic. Unlike grid-based games, this project features a custom **Vector Physics Engine**, simulating real momentum, inertia, and drift in a friction-less environment.


## ✨ Features
* **⚛️ Newtonian Physics:** The ship obeys the laws of inertia. You don't stop moving when you release the key; you must counter-thrust to slow down.
* **📐 Procedural Asteroids:** Rocks are generated as random jagged polygons (not circles). No two asteroids look exactly the same.
* **💥 Splitting Mechanics:** Large rocks split into medium ones, which split into small fast ones.
* **🌌 Hyperspace:** Press `SHIFT` to teleport to a random screen location—a risky maneuver to escape a collision.

## 🎮 How to Play
1.  **Objective:** Destroy all asteroids to advance to the next wave.
2.  **Movement:** Use your thruster carefully. It is easy to lose control if you accelerate too much.
3.  **Screen Wrapping:** Flying off one edge of the screen makes you reappear on the opposite side. This applies to bullets and asteroids as well.

## ⌨️ Controls
| Key | Action |
|---|---|
| **Up Arrow** | **Thrust** (Accelerate) |
| **Left / Right** | Rotate Ship |
| **Space** | **Fire** |
| **Shift** | **Hyperspace** (Random Teleport) |
| **Space** | Restart (on Game Over) |

## 🚀 Running the Game
**Requirements:** Python 3.x, Pygame

```bash
# 1. Install Pygame
pip3 install pygame

# 2. Run the game
python3 asteroids.py

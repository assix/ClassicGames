# Lemmings 🐹

Guide a stream of mindless minions to safety by assigning them specific skills to overcome obstacles in a destructible world.

## ✨ Features
* **⛏️ Destructible Terrain:** The level is fully malleable. Diggers carve real tunnels through the ground, and Builders create permanent bridges that other Lemmings can walk on.
* **🧠 Intelligent Pathfinding:** Lemmings automatically climb small steps (stairs) and turn around when hitting walls or Blockers.
* **🎨 Procedural Graphics:** No sprite sheets! Every Lemming is drawn using code, featuring animated legs, swaying hair, and distinct uniforms for each job.
* **💥 Particle System:** Digging creates dirt debris, building kicks up dust, and explosions... well, they explode.

## 🎮 How to Play
1.  **Objective:** Guide as many Lemmings as possible from the Trapdoor (top left) to the Exit Temple (bottom right).
2.  **Assigning Jobs:**
    * **Step 1:** Click a Job button at the bottom of the screen (e.g., *Digger*).
    * **Step 2:** Click a Lemming in the game world. A white box will appear around the Lemming you are targeting.
3.  **Controls:**
    * **Left Click:** Select Job / Assign Job.
    * **Space:** Pause / Resume.
    * **R:** Restart Level.

## 👷 Jobs & Skills
| Job | Description | Count |
|---|---|---|
| **Walker** | The default state. Walks forward, turns at walls, falls off cliffs. | N/A |
| **Digger** | Digs vertically down through terrain until he falls through. | 10 |
| **Builder** | Builds a 12-step staircase diagonally upwards. | 20 |
| **Blocker** | Stands still and acts as a solid wall, turning others around. | 5 |
| **Bomber** | Counts down (5s) and explodes, destroying terrain and himself. | 5 |

## 🚀 Running the Game
**Requirements:** Python 3.x, Pygame

```bash
# 1. Install Pygame
pip3 install pygame

# 2. Run the game
python3 lemmings/lemmings.py
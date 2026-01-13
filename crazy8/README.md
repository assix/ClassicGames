# Crazy 8s - Python/Pygame

A lightweight, GUI-based implementation of the classic card game **Crazy 8s**, built entirely in Python using the Pygame library.

This project features a custom game engine with **procedural graphics**—meaning no external image assets are required. The cards are drawn programmatically using geometric shapes and Unicode characters, making the game extremely portable and easy to run.

## 🎮 Features
- **Human vs. CPU:** Play against a basic AI opponent.
- **Procedural Rendering:** No \`assets/\` folder needed; just the single Python script.
- **Smooth Animations:** Optimized game loop running at 60 FPS (non-blocking AI).
- **Cross-Platform:** Runs on Linux (Ubuntu/Debian), macOS, and Windows.

## 🛠️ Prerequisites
You need **Python 3.x** and the **Pygame** library installed.

### On Ubuntu / Linux (Debian-based)
\`\`\`bash
sudo apt update
sudo apt install python3-pip
pip3 install pygame
\`\`\`

### On macOS / Windows
\`\`\`bash
pip install pygame
\`\`\`

## 🚀 Installation & Usage

1. **Clone the repository:**
   \`\`\`bash
   git clone https://github.com/assix/ClassicGames.git
   cd CardGames/crazy8-python
   \`\`\`

2. **Run the game:**
   \`\`\`bash
   python3 crazy8.py
   \`\`\`

## 🕹️ How to Play

### Rules
1. **Objective:** Be the first player to empty your hand.
2. **Matching:** You can play a card if it matches the **Rank** (e.g., 5 matches 5) or **Suit** (e.g., Hearts matches Hearts) of the top card on the discard pile.
3. **Crazy 8s:** Eights are wild! You can play an 8 on any card. The AI will automatically pick the best suit for itself when playing an 8.
4. **Drawing:** If you cannot play (or choose not to), click the **DRAW** deck to pick up a card.

### Controls
- **Left Click:** Select a card to play or click the deck to draw.

## 🤝 Contributing
Contributions are welcome! If you want to improve the AI, add sound effects, or polish the UI:

1. Fork the Project
2. Create your Feature Branch (\`git checkout -b feature/AmazingFeature\`)
3. Commit your Changes (\`git commit -m 'Add some AmazingFeature'\`)
4. Push to the Branch (\`git push origin feature/AmazingFeature\`)
5. Open a Pull Request

## 📄 License
Distributed under the MIT License. See \`LICENSE\` for more information.

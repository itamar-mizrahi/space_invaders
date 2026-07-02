# Space Invaders 🚀

A modern, action-packed clone of the classic Space Invaders arcade game, built entirely in Python using `pygame-ce`. 
This version features powerups, boss waves, increasing difficulty, and is playable directly in your web browser!

![Gameplay Snapshot](background.jpg) <!-- Optional: We can add an actual screenshot later -->

🎮 **[PLAY IT LIVE IN YOUR BROWSER HERE!](https://itamar-mizrahi.github.io/space_invaders/)** 🎮

## ✨ Features

* **Endless Waves:** The game gets progressively harder as you clear waves. Enemies move faster and shoot more often.
* **Boss Fights:** Every 5th wave is a Boss Wave! Face off against a massive alien ship with massive health and aggressive attacks.
* **Powerups system:** 
  * 🟢 **Double Shot:** Fires two parallel lasers.
  * 🟣 **Pierce Shot:** A powerful laser that goes straight through multiple enemies.
  * 🟡 **Spread Shot:** Fires three lasers in a cone shape.
  * 💖 **Extra Life:** Grants an additional life.
  * 🛡️ **Shield:** Protects your ship from the next hit.
* **High Score Tracking:** Your highest score is automatically saved locally in your browser/computer.
* **WebAssembly Support:** Deployed seamlessly to GitHub Pages using `pygbag`.

## ⌨️ Controls

* **Left / Right Arrows:** Move the spaceship
* **Spacebar:** Shoot lasers (Hold for continuous autofire)
* **P:** Pause / Resume the game
* **Escape:** Return to the main menu

## 🛠️ How to run locally (Windows / Mac / Linux)

If you prefer to run the game natively on your machine instead of the browser:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/itamar-mizrahi/space_invaders.git
   cd space_invaders
   ```

2. **Install the dependencies:**
   Make sure you have Python 3.9+ installed.
   ```bash
   pip install pygame-ce
   ```

3. **Run the game:**
   ```bash
   python main.py
   ```

## 🌐 Web Deployment (Pygbag)

This project uses [Pygbag](https://pygame-web.github.io/) to compile the Python code into WebAssembly (WASM), allowing it to run natively inside any modern web browser without installing Python.

The deployment is handled automatically via GitHub Actions whenever code is pushed to the `master` branch.

## 📄 Credits
Developed by Itamar Mizrahi. Built with Python and Pygame-CE.

# Collect the Coins

A tiny beginner-friendly game made with Python and Pygame. The goal is to collect yellow coins while avoiding the red enemy.

## Run the game

1. Install Python 3.
2. Open a terminal in this folder.
3. Install Pygame:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the game:

   ```bash
   python main.py
   ```

## Controls

- **WASD** or **arrow keys** — move
- **R** — restart after game over
- **Esc** — quit

## How the code is organized

Everything is in `main.py` to make the logic easy to follow:

- `Player` — handles movement and drawing the player.
- `Coin` — stores and draws a coin.
- `Enemy` — moves from side to side.
- `Game` — handles events, updates objects, checks collisions, draws the screen, and runs the main loop.

The game uses simple rectangles and circles, so no image or sound assets are needed.

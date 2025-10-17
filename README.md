# Lotería Display (Pygame)

## What this is
A simple Python app to show Lotería cards randomly **without repeats** until you reset.

## How to use
1. Install Python 3.8+.
2. Install Pygame:
   ```bash
   pip install pygame
   ```
3. Place your card images in a folder named `cards` next to `loteria.py`.
   - Supported: .png .jpg .jpeg .webp .bmp
4. Run the app:
   ```bash
   python3 loteria.py
   ```

## Controls
- Space / Right Arrow / Enter → Next card
- R → Reset deck (reshuffle & start over)
- S → Shuffle remaining
- F → Toggle fullscreen
- Esc / Q → Quit

## Tips
- Images are auto-scaled to fit while preserving aspect ratio.
- A counter shows how many cards have been shown (e.g., `12 / 54`).
- If you want a specific order, skip shuffling and draw in sequence.

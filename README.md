# 🔤 Alpha Smash

A toddler-safe full-screen typing game built with Python and Pygame.

Kids are prompted to spell familiar words one letter at a time. Correct keys fill in the word with big, colorful letters. Wrong keys float harmlessly across the screen. When a word is completed, a celebration animation plays with the word's emoji.

## Features

- **Big colorful letters** — easy for small eyes to see
- **Guided spelling** — pulsing indicator shows which letter to press next
- **Safe wrong keys** — mistyped letters appear as fun floating text, not errors
- **Word completion** — confetti + emoji celebration on each finished word
- **Toddler-proof** — full-screen, mouse hidden, window can't be closed normally
- **Adult exit** — type the numeric codeword shown in the corner to quit

## Requirements

- Python 3.8+
- Pygame 2.5+

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

The app launches in full-screen mode with the mouse cursor hidden.

## How to Exit

Look at the **bottom-right corner** of the screen for a line like:

> `exit: three eight two seven one`

Type those digits on your keyboard (e.g., `3`, `8`, `2`, `7`, `1`) to exit the app. The codeword is randomized each time the app starts.

## Word List

The game includes 90+ toddler-friendly words across categories: animals, food, household objects, nature, vehicles, and body parts. Each word has an associated emoji shown on completion.

## Configuration

Edit `config.py` to adjust:

- Font sizes, colors, and animation speeds
- Codeword length
- Wrong letter behavior (lifetime, max count)
- Celebration duration

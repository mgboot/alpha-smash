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
- **Multi-language** — switch between English, Spanish (Latin American), and German via flag buttons
- **Diacritic support** — special characters (ñ, ü, ö, etc.) display automatically when the base letter is typed
- **Text-to-Speech** — completed words are read aloud via Azure TTS (requires `az login`)

## Requirements

- Python 3.8+
- Pygame 2.5+
- Azure CLI (for Text-to-Speech, optional)

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

The app launches in full-screen mode with the mouse cursor hidden.

## Language Switching

Tap one of the three flag buttons in the **top-right corner** of the screen to switch languages:

- 🇺🇸 English
- 🇲🇽 Spanish (Latin American)
- 🇩🇪 German

The game always starts in English. Switching mid-word loads a new word in the selected language immediately.

For languages with special characters (ñ, á, ü, ö, etc.), simply type the base letter on the keyboard — the correct diacritic is displayed automatically.

## Text-to-Speech (Optional)

When a word is completed, it is read aloud using Azure Text-to-Speech. To enable:

1. Install the Azure CLI and run `az login`
2. Ensure you have an Azure Cognitive Services Speech resource

If Azure auth is unavailable, TTS is silently skipped and the game works normally.

## How to Exit

Look at the **bottom-right corner** of the screen for a line like:

> `exit: three eight two seven one`

Type those digits on your keyboard (e.g., `3`, `8`, `2`, `7`, `1`) to exit the app. The codeword is randomized each time the app starts and always displays in English.

## Word Lists

The game includes toddler-friendly words across categories (animals, food, objects, nature, vehicles, body parts) in three languages, each with an associated emoji.

## Configuration

Edit `config.py` to adjust:

- Font sizes, colors, and animation speeds
- Codeword length
- Wrong letter behavior (lifetime, max count)
- Celebration duration
- Flag button size and position

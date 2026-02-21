"""Configuration constants for Alpha Smash."""

import pygame

# Display
FULLSCREEN = True
FPS = 60

# Colors
BG_COLOR = (30, 30, 50)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
DARK_GRAY = (70, 70, 70)
MUTED_GRAY = (90, 90, 100)

# Bright letter colors (cycled per letter slot)
LETTER_COLORS = [
    (255, 87, 87),    # red
    (255, 189, 46),   # yellow
    (46, 213, 115),   # green
    (30, 144, 255),   # blue
    (190, 75, 219),   # purple
    (255, 140, 50),   # orange
    (0, 210, 211),    # teal
    (255, 105, 180),  # pink
]

SLOT_EMPTY_COLOR = (80, 80, 110)
NEXT_LETTER_COLOR = (255, 255, 100)
PROMPT_COLOR = (200, 200, 220)

# Font sizes
LETTER_FONT_SIZE = 150
PROMPT_FONT_SIZE = 48
EMOJI_FONT_SIZE = 120
CODEWORD_FONT_SIZE = 18
WRONG_LETTER_MIN_SIZE = 60
WRONG_LETTER_MAX_SIZE = 140

# Wrong letter floaters
WRONG_LETTER_LIFETIME = 2.5  # seconds
MAX_WRONG_LETTERS = 20

# Celebration
CELEBRATION_DURATION = 2.5  # seconds
CONFETTI_COUNT = 80

# Codeword
CODEWORD_LENGTH = 5

# Pulse animation
PULSE_SPEED = 3.0  # Hz
PULSE_SCALE_MIN = 0.95
PULSE_SCALE_MAX = 1.1

# Language
DEFAULT_LANGUAGE = "en"

# Flag buttons (top-right corner)
FLAG_SIZE = 50
FLAG_MARGIN = 15
FLAG_GAP = 10
FLAG_HIGHLIGHT_COLOR = (255, 255, 100)
FLAG_HIGHLIGHT_WIDTH = 3

# Flag emoji per language
FLAG_EMOJI = {
    "en": "🇺🇸",
    "es": "🇵🇷",
    "de": "🇩🇪",
}

# Azure Text-to-Speech
# Set this to your Azure Speech resource endpoint (or leave empty to disable TTS)
SPEECH_ENDPOINT = "https://dos-aoai-westus.cognitiveservices.azure.com/"

TTS_VOICES = {
    "en": "en-US-AvaNeural",
    "es": "es-US-PalomaNeural",
    "de": "de-DE-KatjaNeural",
}

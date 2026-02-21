"""Core game logic for Alpha Smash."""

import random
import time
from words import get_random_word, NUMBER_WORDS
from config import (
    CODEWORD_LENGTH, WRONG_LETTER_LIFETIME, MAX_WRONG_LETTERS,
    CELEBRATION_DURATION,
)


class WrongLetter:
    """A wrong letter floating on screen."""

    def __init__(self, char, x, y, size, color):
        self.char = char
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.born = time.time()
        self.lifetime = WRONG_LETTER_LIFETIME

    @property
    def age(self):
        return time.time() - self.born

    @property
    def alpha(self):
        """Opacity from 1.0 to 0.0 over lifetime."""
        return max(0.0, 1.0 - self.age / self.lifetime)

    @property
    def alive(self):
        return self.age < self.lifetime


class Game:
    """Manages the game state."""

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Current word
        self.current_word = ""
        self.current_emoji = ""
        self.letter_index = 0  # next letter to match

        # Wrong letters floating on screen
        self.wrong_letters = []

        # Codeword for exit
        self.codeword = self._generate_codeword()
        self.codeword_display = self._codeword_to_words(self.codeword)
        self.codeword_index = 0  # progress through codeword

        # Celebration state
        self.celebrating = False
        self.celebration_start = 0

        # Start first word
        self._next_word()

    def _generate_codeword(self):
        """Generate a random numeric codeword string."""
        return "".join(str(random.randint(0, 9)) for _ in range(CODEWORD_LENGTH))

    def _codeword_to_words(self, code):
        """Convert '12345' to 'one two three four five'."""
        return " ".join(NUMBER_WORDS[d] for d in code)

    def _next_word(self):
        """Load the next word."""
        word, emoji = get_random_word(exclude=self.current_word)
        self.current_word = word
        self.current_emoji = emoji
        self.letter_index = 0

    def handle_key(self, key_char):
        """Handle a keypress. Returns 'exit' if codeword completed, else None."""
        if self.celebrating:
            return None

        # Check codeword progress (digits only)
        if key_char.isdigit():
            if key_char == self.codeword[self.codeword_index]:
                self.codeword_index += 1
                if self.codeword_index >= len(self.codeword):
                    return "exit"
            else:
                self.codeword_index = 0
            # Digits don't participate in word spelling
            return None

        # Non-digit codeword progress resets on any non-digit key
        # (only digits are used for codeword, so we don't reset here)

        upper = key_char.upper()
        if not upper.isalpha():
            return None

        # Check if it matches the next expected letter
        if self.letter_index < len(self.current_word):
            if upper == self.current_word[self.letter_index]:
                self.letter_index += 1
                # Word complete?
                if self.letter_index >= len(self.current_word):
                    self.celebrating = True
                    self.celebration_start = time.time()
                return None

        # Wrong letter — add as floater
        self._add_wrong_letter(upper)
        return None

    def _add_wrong_letter(self, char):
        """Add a wrong letter at a random position."""
        import random as rnd
        from config import (
            WRONG_LETTER_MIN_SIZE, WRONG_LETTER_MAX_SIZE, LETTER_COLORS,
        )

        margin = 100
        x = rnd.randint(margin, self.screen_width - margin)
        y = rnd.randint(margin, self.screen_height - margin)
        size = rnd.randint(WRONG_LETTER_MIN_SIZE, WRONG_LETTER_MAX_SIZE)
        color = rnd.choice(LETTER_COLORS)

        self.wrong_letters.append(WrongLetter(char, x, y, size, color))

        # Cap the number of floaters
        if len(self.wrong_letters) > MAX_WRONG_LETTERS:
            self.wrong_letters.pop(0)

    def update(self):
        """Update game state each frame."""
        # Remove dead wrong letters
        self.wrong_letters = [wl for wl in self.wrong_letters if wl.alive]

        # Check celebration timer
        if self.celebrating:
            elapsed = time.time() - self.celebration_start
            if elapsed >= CELEBRATION_DURATION:
                self.celebrating = False
                self.wrong_letters.clear()
                self._next_word()

    @property
    def filled_letters(self):
        """Return list of (char, is_filled) for each letter in current word."""
        result = []
        for i, ch in enumerate(self.current_word):
            result.append((ch, i < self.letter_index))
        return result

    @property
    def next_letter(self):
        """The next letter the player needs to press."""
        if self.letter_index < len(self.current_word):
            return self.current_word[self.letter_index]
        return None

    @property
    def celebration_progress(self):
        """0.0 to 1.0 progress through celebration."""
        if not self.celebrating:
            return 0.0
        return min(1.0, (time.time() - self.celebration_start) / CELEBRATION_DURATION)

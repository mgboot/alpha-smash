"""Rendering for Alpha Smash — all drawing logic."""

import math
import time
import random
import pygame
from config import (
    BG_COLOR, WHITE, MUTED_GRAY, SLOT_EMPTY_COLOR, NEXT_LETTER_COLOR,
    LETTER_COLORS, PROMPT_COLOR,
    LETTER_FONT_SIZE, PROMPT_FONT_SIZE, EMOJI_FONT_SIZE, CODEWORD_FONT_SIZE,
    PULSE_SPEED, PULSE_SCALE_MIN, PULSE_SCALE_MAX,
    CONFETTI_COUNT,
)


class ConfettiParticle:
    """A single confetti particle for celebrations."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-10, -2)
        self.gravity = 0.15
        self.color = random.choice(LETTER_COLORS)
        self.size = random.randint(6, 14)
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-5, 5)

    def update(self):
        self.x += self.vx
        self.vy += self.gravity
        self.y += self.vy
        self.rotation += self.rot_speed

    def draw(self, surface):
        rect = pygame.Rect(0, 0, self.size, self.size // 2)
        rect.center = (int(self.x), int(self.y))
        pygame.draw.rect(surface, self.color, rect)


class Renderer:
    """Handles all drawing to the screen."""

    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        # Fonts
        self.letter_font = pygame.font.SysFont("Arial", LETTER_FONT_SIZE, bold=True)
        self.prompt_font = pygame.font.SysFont("Arial", PROMPT_FONT_SIZE, bold=True)
        self.codeword_font = pygame.font.SysFont("Arial", CODEWORD_FONT_SIZE)
        self.emoji_font = pygame.font.SysFont("Segoe UI Emoji", EMOJI_FONT_SIZE)
        self.wrong_fonts = {}  # cache by size

        # Confetti particles
        self.confetti = []
        self._confetti_spawned = False

    def _get_wrong_font(self, size):
        if size not in self.wrong_fonts:
            self.wrong_fonts[size] = pygame.font.SysFont("Arial", size, bold=True)
        return self.wrong_fonts[size]

    def render(self, game):
        """Main render method — draws everything."""
        self.screen.fill(BG_COLOR)

        if game.celebrating:
            self._draw_celebration(game)
        else:
            self._confetti_spawned = False
            self.confetti.clear()
            self._draw_wrong_letters(game)
            self._draw_word(game)
            self._draw_prompt(game)

        self._draw_codeword(game)
        pygame.display.flip()

    def _draw_word(self, game):
        """Draw the target word with filled/empty letter slots."""
        letters = game.filled_letters
        n = len(letters)
        spacing = LETTER_FONT_SIZE + 20
        total_width = n * spacing - 20
        start_x = (self.width - total_width) // 2
        y = self.height // 2 - LETTER_FONT_SIZE // 2

        now = time.time()

        for i, (char, filled) in enumerate(letters):
            x = start_x + i * spacing
            color_idx = i % len(LETTER_COLORS)

            if filled:
                color = LETTER_COLORS[color_idx]
                text = self.letter_font.render(char, True, color)
                rect = text.get_rect(center=(x + spacing // 2, y + LETTER_FONT_SIZE // 2))
                self.screen.blit(text, rect)
            elif i == game.letter_index:
                # Pulsing underscore for next expected letter
                pulse = math.sin(now * PULSE_SPEED * 2 * math.pi) * 0.5 + 0.5
                scale = PULSE_SCALE_MIN + pulse * (PULSE_SCALE_MAX - PULSE_SCALE_MIN)
                size = int(LETTER_FONT_SIZE * scale)
                font = pygame.font.SysFont("Arial", size, bold=True)
                text = font.render("_", True, NEXT_LETTER_COLOR)
                rect = text.get_rect(center=(x + spacing // 2, y + LETTER_FONT_SIZE // 2 + 10))
                self.screen.blit(text, rect)
            else:
                # Empty slot
                text = self.letter_font.render("_", True, SLOT_EMPTY_COLOR)
                rect = text.get_rect(center=(x + spacing // 2, y + LETTER_FONT_SIZE // 2 + 10))
                self.screen.blit(text, rect)

    def _draw_prompt(self, game):
        """Draw 'Press: X' prompt above the word."""
        if game.next_letter:
            prompt_text = f"Press:  {game.next_letter}"
            text = self.prompt_font.render(prompt_text, True, PROMPT_COLOR)
            rect = text.get_rect(center=(self.width // 2, self.height // 2 - LETTER_FONT_SIZE - 40))
            self.screen.blit(text, rect)

    def _draw_wrong_letters(self, game):
        """Draw floating wrong letters with fade-out."""
        for wl in game.wrong_letters:
            alpha = wl.alpha
            if alpha <= 0:
                continue
            font = self._get_wrong_font(wl.size)
            color = (
                int(wl.color[0] * alpha),
                int(wl.color[1] * alpha),
                int(wl.color[2] * alpha),
            )
            text = font.render(wl.char, True, color)
            rect = text.get_rect(center=(wl.x, wl.y))
            self.screen.blit(text, rect)

    def _draw_celebration(self, game):
        """Draw celebration screen with emoji and confetti."""
        progress = game.celebration_progress

        # Spawn confetti once
        if not self._confetti_spawned:
            self._confetti_spawned = True
            for _ in range(CONFETTI_COUNT):
                x = random.randint(0, self.width)
                y = random.randint(self.height // 3, self.height * 2 // 3)
                self.confetti.append(ConfettiParticle(x, y))

        # Update and draw confetti
        for p in self.confetti:
            p.update()
            p.draw(self.screen)

        # Draw completed word in big letters
        word = game.current_word
        n = len(word)
        spacing = LETTER_FONT_SIZE + 20
        total_width = n * spacing - 20
        start_x = (self.width - total_width) // 2
        y = self.height // 2 - LETTER_FONT_SIZE // 2 - 40

        for i, char in enumerate(word):
            color = LETTER_COLORS[i % len(LETTER_COLORS)]
            text = self.letter_font.render(char, True, color)
            rect = text.get_rect(center=(start_x + i * spacing + spacing // 2,
                                         y + LETTER_FONT_SIZE // 2))
            self.screen.blit(text, rect)

        # Draw emoji below the word
        emoji_surface = self.emoji_font.render(game.current_emoji, True, WHITE)
        emoji_rect = emoji_surface.get_rect(center=(self.width // 2,
                                                     y + LETTER_FONT_SIZE + 80))
        self.screen.blit(emoji_surface, emoji_rect)

        # Draw "Great job!" text
        great = self.prompt_font.render("Great job!", True, NEXT_LETTER_COLOR)
        great_rect = great.get_rect(center=(self.width // 2, y - 60))
        self.screen.blit(great, great_rect)

    def _draw_codeword(self, game):
        """Draw the exit codeword hint in the bottom-right corner."""
        text = self.codeword_font.render(
            f"exit: {game.codeword_display}", True, MUTED_GRAY
        )
        rect = text.get_rect(bottomright=(self.width - 15, self.height - 10))
        self.screen.blit(text, rect)

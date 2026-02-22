"""Alpha Smash — A toddler-safe typing game.

Run: python main.py
Exit: type the numeric codeword shown in the bottom-right corner.
"""

import os
import sys
import pygame
from config import FPS, FULLSCREEN
from game import Game
from renderer import Renderer


def _load_dotenv():
    """Load .env file from the project root if it exists."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.isfile(env_path):
        return
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def main():
    _load_dotenv()
    pygame.init()

    # Set up full-screen display
    if FULLSCREEN:
        info = pygame.display.Info()
        screen = pygame.display.set_mode(
            (info.current_w, info.current_h), pygame.FULLSCREEN
        )
    else:
        screen = pygame.display.set_mode((1280, 720))

    pygame.display.set_caption("Alpha Smash")
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()
    game = Game(screen.get_width(), screen.get_height())
    renderer = Renderer(screen)

    running = True
    while running:
        for event in pygame.event.get():
            # Handle touch events for flag buttons
            if event.type == pygame.FINGERDOWN:
                tx = int(event.x * screen.get_width())
                ty = int(event.y * screen.get_height())
                lang = renderer.hit_test_flags(tx, ty)
                if lang:
                    game.switch_language(lang)
                continue

            # Allow mouse clicks only on flag buttons (for touchscreen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                lang = renderer.hit_test_flags(event.pos[0], event.pos[1])
                if lang:
                    game.switch_language(lang)
                continue

            # Ignore other mouse events
            if event.type in (
                pygame.MOUSEMOTION,
                pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL,
            ):
                continue

            if event.type == pygame.QUIT:
                # Prevent window close — only codeword exits
                continue

            if event.type == pygame.KEYDOWN:
                # Get the typed character
                char = event.unicode
                if char:
                    result = game.handle_key(char)
                    if result == "exit":
                        running = False

        game.update()
        renderer.render(game)
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()

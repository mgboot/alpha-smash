"""Alpha Smash — A toddler-safe typing game.

Run: python main.py
Exit: type the numeric codeword shown in the bottom-right corner.
"""

import sys
import pygame
from config import FPS, FULLSCREEN
from game import Game
from renderer import Renderer


def main():
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
            # Ignore mouse events entirely
            if event.type in (
                pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN,
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

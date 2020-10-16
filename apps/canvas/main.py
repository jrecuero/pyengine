import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from engine import Log, Color
from _game_handler import GameHandler
from _game_scene import GameScene
from _settings import FPS, WIDTH, HEIGHT


def main():
    Log.Main("Canvas App").State("init").call()
    pygame.init()
    pygame.display.set_caption("Canvas App")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    ghandler = GameHandler(screen, clock)
    gscene = GameScene(screen)
    ghandler.add_scene(gscene)
    ghandler.hscene.active(gscene)
    while True:
        clock.tick(FPS)

        # -> handle events
        ghandler.event_handler()
        # <-

        # -> update objects
        ghandler.update()
        # <-

        # -> render objects
        screen.fill(Color.RED)
        ghandler.render()
        # <-

    Log.Main("Canvas App").State("end").call()


if __name__ == "__main__":
    main()

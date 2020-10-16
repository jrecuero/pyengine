import os
# import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
# from pyengine import Scene, GRect, GHandler, Color, Log, Grid, Layer, GTimed
# from pyengine import Move
from pyengine import Log, Color
from _game_scene import GameScene
from _game_handler import GameHandler


def main():
    Log.Main("Workspace App").State("Init").call()
    pygame.init()
    pygame.display.set_caption("Workspace App")
    screen = pygame.display.set_mode((900, 900))
    clock = pygame.time.Clock()
    ghandler = GameHandler(screen, clock)
    gscene = GameScene(screen)
    ghandler.add_scene(gscene)
    ghandler.hscene.active(gscene)
    while True:
        clock.tick(30)
        ghandler.event_handler()

        # -> update objects
        ghandler.update()
        # <-

        # -> render objects
        screen.fill(Color.WHITE)
        ghandler.render()
        # pygame.display.flip()
        # <-
    Log.Main("Workspace App").State("End").call()


if __name__ == "__main__":
    main()

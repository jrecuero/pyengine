import os
# import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
# from pyengine import Scene, GRect, GHandler, Color, Log, Grid, Layer, GTimed
# from pyengine import Move
from pyengine import Log, Color, GTextBox
from _game_scene import GameScene
from _game_handler import GameHandler


def main():
    Log.Main("Gritty App").State("Init").call()
    pygame.init()
    pygame.display.set_caption("GRITTY")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    ghandler = GameHandler(screen, clock)
    gscene = GameScene(screen)
    glog = GTextBox("Log Activity", 32, 320 + 64, 320, 192, logger=True)
    glog.messages = "Log Activity"
    gscene.add_gobject(glog)
    ghandler.add_scene(gscene)
    ghandler.hscene.active(gscene)
    while True:
        clock.tick(30)
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit(0)
        ghandler.event_handler()

        # -> update objects
        ghandler.update()
        # <-

        # -> render objects
        screen.fill(Color.WHITE)
        ghandler.render()
        # pygame.display.flip()
        # <-
    Log.Main("Gritty App").State("End").call()


if __name__ == "__main__":
    main()

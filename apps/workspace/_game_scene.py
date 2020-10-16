import sys
import pygame
from pyengine import Scene
# from pyengine import Log
from _game_board import GameBoard


class GameScene(Scene):

    def __init__(self, surface, **kwargs):
        super(GameScene, self).__init__("Game Workspace Scene", surface, **kwargs)
        self.board = GameBoard(20, 20, 0, 0, 32, 32, 640, 640)
        self.add_gobject(self.board)

    def handle_keyboard_event(self, event, **kwargs):
        """handle_keyboard_event should process the keyboard event given.
        """
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_x]:
            sys.exit(0)

        super(GameScene, self).handle_keyboard_event(event, **kwargs)

    def update(self, **kwargs):
        """update calls update method for all scene graphical objects.
        """
        super(GameScene, self).update(**kwargs)

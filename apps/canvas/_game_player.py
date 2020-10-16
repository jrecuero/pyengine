# import sys
import pygame
from engine import GImage
from _game_gobjects import GameBullet
from _settings import BULLET_LAYER


class GamePlayer(GImage):
    """GamePlayer class implements the game player image for the game.
    """

    def __init__(self, image, x, y, **kwargs):
        """__init__ initializes GamePlayer instance.

        Args:
            image (Image): GamePlayer instance image to be used.
            x (int): GamePlayer instance initial X-axis position.
            y (int): GamePlayer instance initial Y-axis position.
            **kwargs (dict): GamePlayer dictionary with custom arguments.
        """
        super(GamePlayer, self).__init__("Canvas Player", image, x, y, **kwargs)
        self.vx = 0
        self.vy = 0
        self.speed = 5

    def update(self, surface, **kwargs):
        """update method update the GamePlayer instance.

        Args:
            surface (Surface): Surface where instance will be displayed
            **kwargs (dict): custom instance arguments.

        Returns:
            None: no return
        """
        self.x += self.vx
        self.y += self.vy
        result, _ = self.gparent.can_move_to(self)
        if not result:
            self.x -= self.vx
            self.y -= self.vy

    def handle_keyboard_event(self, event, **kwargs):
        """handle_keyboard_event should process the keyboard event given.

        Args:
            surface (Surface): Surface where instance will be displayed
            **kwargs (dict): custom instance arguments.

        Returns:
            None: no return
        """
        key_pressed = pygame.key.get_pressed()
        # if key_pressed[pygame.K_x]:
        #    sys.exit(0)
        if key_pressed[pygame.K_LEFT]:
            self.vx = -self.speed
            self.vy = 0
        if key_pressed[pygame.K_RIGHT]:
            self.vx = self.speed
            self.vy = 0
        if key_pressed[pygame.K_UP]:
            self.vy = -self.speed
            self.vx = 0
        if key_pressed[pygame.K_DOWN]:
            self.vy = self.speed
            self.vx = 0
        if key_pressed[pygame.K_SPACE]:
            bullet = GameBullet(self.x + self.dx / 2, self.y + self.dy / 10, 2)
            bullet.owner = self
            self.gparent.add_gobject(bullet, BULLET_LAYER)

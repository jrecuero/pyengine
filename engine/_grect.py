import pygame
from ._gobject import GObject


class GRect(GObject):
    """GRect implements a graphical object that is rendered as a rectangle.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GRect, self).__init__(name, x, y, dx, dy, **kwargs)
        pygame.draw.rect(self.image, self.color, (0, 0, self.dx, self.dy), self.outline)

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | ({self.x}, {self.y}) ({self.dx}, {self.dy})"

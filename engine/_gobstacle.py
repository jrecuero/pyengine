import pygame
from ._gobject import GObject
from ._loggar import Log


class GObstacle(GObject):
    """GObstacle class contains all information related with a graphical
    obstacle, that should trigger a collision with any other solid graphical
    object.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GObstacle, self).__init__(name, x, y, dx, dy, **kwargs)
        pygame.draw.rect(self.image, self.color, (0, 0, self.dx, self.dy), self.outline)

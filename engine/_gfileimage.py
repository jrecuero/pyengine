import pygame
from ._gobject import GObject


class GFileImage(GObject):
    """GFileImage implements a graphical object that is rendered as an image from
    an filename.
    """

    def __init__(self, name, filename, x, y, **kwargs):
        image = pygame.image.load(filename)
        rect = image.get_rect()
        super(GFileImage, self).__init__(name, x, y, rect.width, rect.height, **kwargs)
        self.filename = filename
        self.image = image
        self.rect = rect

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | {self.filename} ({self.x}, {self.y})"

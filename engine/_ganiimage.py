import pygame
from ._gobject import GObject
from ._loggar import Log


class GAniImage(GObject):
    """GAniImage implements a graphical object that is rendered as an animated
    image from an image.
    """

    def __init__(self, name, sprite_sheet, x, y, dx, dy, start=0, end=0, **kwargs):
        super(GAniImage, self).__init__(name, x, y, dx, dy, **kwargs)
        self.sprite_sheet = sprite_sheet
        self.start_at = start
        self.end_at = end
        self.index = self.start_at
        self.colorkey = kwargs.get("colorkey", -1)
        self.image = self.sprite_sheet.image_at(pygame.Rect(self.index * dx, 0, dx, dy), colorkey=self.colorkey)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.repeated_frames = 0
        self.repeat_frames = kwargs.get("repeat_frames", 5)
        if end >= self.sprite_sheet.frames:
            raise Exception("End frame {end} greater than sprite sheet max frames {self.sprite_sheet.frames}")

    def set_new_frames(self, start, end):
        """set_new_frames sets new start_at and end_at frames for the animation.
        """
        if end >= self.sprite_sheet.frames:
            raise Exception("End frame {end} greater than sprite sheet max frames {self.sprite_sheet.frames}")
        self.start_at = start
        self.end_at = end
        self.index = start

    def update(self, surface, **kwargs):
        """update updates animated image.
        """
        Log.GAniImage(self.name).Update(f"{surface}").call()
        if self.repeated_frames == self.repeat_frames:
            self.repeated_frames = 0
            self.index = self.start_at if self.index == self.end_at else self.index + 1
            self.image = self.sprite_sheet.image_at(pygame.Rect(self.index * self.dx, 0, self.dx, self.dy), colorkey=self.colorkey)
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
        else:
            self.repeated_frames += 1

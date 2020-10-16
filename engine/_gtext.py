import pygame
from ._color import Color
from ._gobject import GObject


class GText(GObject):
    def __init__(self, name, x, y, message, **kwargs):
        self._message = message
        self.font_name = kwargs.get("font_name", "Courier")
        self.font_size = kwargs.get("font_size", 18)
        self.font_bold = kwargs.get("font_bold", False)
        self.font_italic = kwargs.get("font_italic", False)
        self.font = pygame.font.SysFont(self.font_name, self.font_size, bold=self.font_bold, italic=self.font_italic)
        self.color = kwargs.get("color", Color.BLACK)
        self.background_color = kwargs.get("bcolor", Color.WHITE)
        self.gtext = self.font.render(self._message, True, self.color)
        rect = self.gtext.get_rect()
        super(GText, self).__init__(name, x, y, rect.w, rect.h, **kwargs)
        self.image.fill(self.background_color)
        self.image.blit(self.gtext, (0, 0, self.dx, self.dy))

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | ({self.x}, {self.y}) {self.message}"

    @property
    def message(self):
        """message property returns the string to be displayed by the graphical
        text object.
        """
        return self._message

    @message.setter
    def message(self, val):
        """message setters sets the string to be displayed, it cleans any
        previous text from the surface and update surface instance.
        """
        self._message = val
        self.gtext = self.font.render(self._message, True, self.color)
        self.rect = self.gtext.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self._dx = self.rect.w
        self._dy = self.rect.h
        self.image.fill((255, 255, 255, 0))
        self.image.fill(self.background_color)
        self.image.blit(self.gtext, (0, 0, self.dx, self.dy))

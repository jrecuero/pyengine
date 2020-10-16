import pygame
from ._color import Color
from ._gobject import GObject


class GTextBox(GObject):

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GTextBox, self).__init__(name, x, y, dx, dy, **kwargs)
        pygame.draw.rect(self.image, self.color, (0, 0, self.dx, self.dy), 1)
        self.font_name = kwargs.get("font_name", "Courier")
        self.font_size = kwargs.get("font_size", 12)
        self.font_bold = kwargs.get("font_bold", False)
        self.font_italic = kwargs.get("font_italic", False)
        self.font = pygame.font.SysFont(self.font_name, self.font_size, bold=self.font_bold, italic=self.font_italic)
        self.color = kwargs.get("color", Color.BLACK)
        self.background_color = kwargs.get("bcolor", Color.WHITE)
        self._messages = []

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | ({self.x}, {self.y}) ({self.dx}, {self.dy}) {self.messages}"

    @property
    def messages(self):
        """messages property returns list of strings to be displayed by the graphical
        text box object.
        """
        return self._messages

    @messages.setter
    def messages(self, val):
        """messages setters sets a new string to be displayed, it cleans any
        previous text from the surface and update surface instance.
        """
        self.image.fill((255, 255, 255, 0))
        self.image.fill(self.background_color)
        pygame.draw.rect(self.image, self.color, (0, 0, self.dx, self.dy), 1)
        self._messages.append(f"{val}")
        inc_x, inc_y = self.font_size / 2, self.font_size / 2
        scroll_len = (self.dy // self.font_size) - 1
        for msg in self._messages[-scroll_len:]:
            gtext = self.font.render(msg, True, self.color)
            rect = gtext.get_rect()
            rect.x, rect.y = self.x + inc_x, self.y + inc_y
            self.image.blit(gtext, (inc_x, inc_y, rect.w, rect.h))
            inc_y += self.font_size

import pygame
from ._gobject import GObject, Color
from ._loggar import Log


class GMenu(GObject):
    """GMenu implementsa graphical menu entity.
    """

    VERTICAL = 1
    HORIZONTAL = 2

    def __init__(self, name, text, x, y, **kwargs):
        self.text = text
        self.sprite_group = pygame.sprite.LayeredUpdates()
        self.menu_items = []
        self.width = kwargs.get("width", None)
        self.height = kwargs.get("height", None)
        self.shortcut = kwargs.get("shortcut", None)
        self.orientation = kwargs.get("orientation", GMenu.HORIZONTAL)
        self.callback = kwargs.get("callback", None)
        self.font_name = kwargs.get("font_name", "Courier")
        self.font_size = kwargs.get("font_size", 18)
        self.font_bold = kwargs.get("font_bold", False)
        self.font_italic = kwargs.get("font_italic", False)
        self.color = kwargs.get("color", Color.BLACK)
        self.background_color = kwargs.get("bcolor", Color.WHITE)
        self.font = pygame.font.SysFont(self.font_name, self.font_size, bold=self.font_bold, italic=self.font_italic)
        self.highlighted_index = 0
        if self.text:
            self.gtext = self.font.render(self.text, True, self.color)
            rect = self.gtext.get_rect()
            super(GMenu, self).__init__(name, x, y, rect.w, rect.h, **kwargs)
            self.image.fill(self.background_color)
            self.image.blit(self.gtext, (0, 0, self.dx, self.dy))
            self._next_item_x = self.x + 1 + int(self.gtext.get_rect().w * 1.5) if self.orientation == GMenu.HORIZONTAL else self.x + 1
            self._next_item_y = self.y + 1 + self.gtext.get_rect().h if self.orientation == GMenu.VERTICAL else self.y + 1
        else:
            super(GMenu, self).__init__(name, x, y, 0, 0, **kwargs)
            self.gtext = None
            self._next_item_x = self.x + 1
            self._next_item_y = self.y + 1
        Log.Menu(self.name).Create().call()

    @property
    def highlighted(self):
        return self._highlighted

    @highlighted.setter
    def highlighted(self, val):
        self._highlighted = val
        color = self.color if not val else self.background_color
        background_color = self.background_color if not val else self.color
        self.gtext = self.font.render(self.text, True, color)
        self.rect = self.gtext.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self._dx = self.rect.w
        self._dy = self.rect.h
        self.image.fill(background_color)
        self.image.blit(self.gtext, (0, 0, self.dx, self.dy))

    def add_menu_item(self, text, **kwargs):
        """add_menu_item adds a new menu item entry.
        """
        # menu_item.x = self.x
        # menu_item.y = self.y
        # menu_item.dx = self.dx
        # menu_item.dy = self.dy
        menu_item = GMenu(text, text, self._next_item_x, self._next_item_y, **kwargs)
        if self.orientation == GMenu.HORIZONTAL:
            self._next_item_x += int(menu_item.gtext.get_rect().w * 1.5)
        elif self.orientation == GMenu.VERTICAL:
            self._next_item_y += menu_item.gtext.get_rect().h
        menu_item.highlighted = (self.highlighted_index == len(self.sprite_group))
        self.sprite_group.add(menu_item)
        self.menu_items.append(menu_item)
        return menu_item

    def highlight_next(self):
        """highlight_next highlights the next menu item.
        """
        if self.highlighted_index < len(self.menu_items) - 1:
            self.menu_items[self.highlighted_index].highlighted = False
            self.highlighted_index += 1
            self.menu_items[self.highlighted_index].highlighted = True

    def highlight_prev(self):
        """highlight_prev highlights the previous menu item.
        """
        if self.highlighted_index > 0:
            self.menu_items[self.highlighted_index].highlighted = False
            self.highlighted_index -= 1
            self.menu_items[self.highlighted_index].highlighted = True

    def select(self, **kwargs):
        Log.Menu(self.name).Select(str(kwargs)).call()
        if self.callback:
            return self.callback(**kwargs)
        return None

    def select_highlighted(self, **kwargs):
        return self.menu_items[self.highlighted_index].select(**kwargs)

    def get_highlighted(self):
        return self.menu_items[self.highlighted_index].name

    def render(self, surface, **kwargs):
        """render should draws the instance on the given surface.
        """
        # Render all menu items children
        # Log.Menu(self.name).Render(f"{self.enable}, {self.grayout}, {self.selected}").call()
        if self.enable and self.visible:
            if self.width and self.height:
                pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), True)
            self.sprite_group.draw(surface)

            if not self.grayout and self.selected:
                for mi in self.sprite_group:
                    mi.render(surface, **kwargs)

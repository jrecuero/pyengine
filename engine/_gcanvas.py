import pygame
from ._color import Color
from ._gobject import GDummy
from ._notify import Notify


class GCanvas(GDummy):
    """GCanvas class identifies a graphic canvas containing sprites to be
    displayed
    """

    def __init__(self, name, x, y, dx, dy, nlayers, **kwargs):
        """__init__ method initializes a GCanvas instance.

        Args:
            name (type): Description of parameter `name`.
            x (int): canvas X-axis position.
            y (int): canvas Y-axis position.
            dx (int): sanvas width.
            dy (int): canvas height.
            nlayers (int): canvas number of layers.
            **kwargs (dict): canvas custom arguments.
        """
        super(GCanvas, self).__init__(name, x, y, dx, dy, **kwargs)
        self.number_layers = nlayers
        self.glayers = [pygame.sprite.LayeredUpdates() for _ in range(nlayers)]
        self.collision_glayers = [True for _ in range(nlayers)]
        self.image = pygame.Surface((self.dx, self.dy), pygame.SRCALPHA)
        self.running = True

    def __str__(self):
        """__str__ method display GCanvas instance as a string.

        Returns:
            str: string with Canvas instance information.
        """
        return f"[{self.gid}] : {self.__class__.__name__} ({self.x}, {self.y}) ({self.dx. self.dy})"

    def add_gobject(self, gobject, layer):
        """add_gobject addsa graphical object to the canvas.

        Args:
            gobject (Object): graphical object instance to be added to the canvas.
            layer (int): layer where object should be added to the canvas.

        Returns:
            bool: True if graphical object was added, False else.
        """
        if 0 <= layer < self.number_layers:
            self.glayers[layer].add(gobject)
            gobject.gparent = self
            return True
        return False

    def del_gobject(self, gobject):
        """del_gobject deletes a graphical object from the canvas.

        Args:
            gobject (Object): Object instance to be deleted.

        Returns:
            bool: True if object was found and deleted, False else.
        """
        for layer in self.glayers:
            if gobject in layer:
                layer.remove(gobject)
                Notify.notify(gobject, "DELETED")
                return True
        return False

    def can_move_to(self, gobject, x=None, y=None):
        """can_move_to checks if the given object can move the given x-y delta.
        It returns a boolean with the movement result (True move allowed,
        False, not) and a cell instance if there is a collision.

        Args:
            gobject (Object): GObject instance that want to move.
            x (int): GObject instance final X-axis position.
            y (int): GObject instance final Y-axis position.

        Returns:
            bool, Object: Movement result.
                - Movement allowed: True, None
                - Movement not allowed (out of bounds): False, None
                - Movement not allowed (collision): False, collision-cell
        """
        x = x if x is not None else gobject.x
        y = y if y is not None else gobject.y
        xplus = x + gobject.dx
        yplus = y + gobject.dy
        if 0 <= x and xplus < self.dx and 0 <= y and yplus < self.dy:
            for layer, check_collision in enumerate(self.collision_glayers):
                if not check_collision:
                    continue
                for instance in self.glayers[layer].sprites():
                    if instance == gobject or instance in gobject.owner:
                        continue
                    if instance.rect.colliderect(gobject.rect):
                        return False, instance
            return True, None
        return False, None

    def handle_keyboard_event(self, event, **kwargs):
        """handle_keyboard_event should process the keyboard event given.

        Args:
            event (Event): event to be processed.
            **kwargs (dict): dictionary with custom arguments.

        Returns:
            None: no value.
        """
        if self.running:
            for layer in self.glayers:
                for sprite in layer.sprites():
                    sprite.handle_keyboard_event(event, **kwargs)

    def handle_mouse_event(self, event, **kwargs):
        """handle_mouse_event should process the mouse event given.
        Mouse events are passed to the active scene to be handle.

        Args:
            event (Event): event to be processed.
            **kwargs (dict): dictionary with custom arguments.

        Returns:
            None: no value.
        """
        if self.running:
            for layer in self.glayers:
                for sprite in layer.sprites():
                    sprite.handle_mouse_event(event, **kwargs)

    def handle_custom_event(self, event, **kwargs):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.

        Args:
            event (Event): event to be processed.
            **kwargs (dict): dictionary with custom arguments.

        Returns:
            None: no value.
        """
        if self.running:
            for layer in self.glayers:
                for sprite in layer.sprites():
                    sprite.handle_custom_event(event, **kwargs)

    def update(self, surface, **kwargs):
        if self.running:
            for layer in self.glayers:
                for sprite in layer.sprites():
                    sprite.update(surface, **kwargs)

    def render(self, surface, **kwargs):
        """render method draws canvas instance in the given surface.

        Args:
            surface (Surface): pygame Surface where canvas will be drew.
            **kwargs (dict): render custom arguments

        Returns:
            None: no return value.

        """
        self.image.fill(Color.WHITE)
        for layer in self.glayers:
            layer.draw(self.image)
        surface.blit(self.image, (self.x, self.y))

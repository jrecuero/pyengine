import pygame

# from ._loggar import Log
from ._gid import Gid, new_gid
from ._move import Move
from ._color import Color
from ._layer import Layer


def update_attributes(instance, name, x, y, dx, dy, **kwargs):
    instance.name = name
    instance._x = x
    instance._y = y
    instance._dx = dx
    instance._dy = dy
    instance._layer = kwargs.get("layer", Layer.GROUND)
    instance.pushed = kwargs.get("pushed", None)
    instance.enable = kwargs.get("enable", True)
    instance.grayout = kwargs.get("grayout", False)
    instance._highlighted = kwargs.get("highlighted", False)
    instance.selected = kwargs.get("selected", False)
    instance.visible = kwargs.get("visible", 1)
    instance.solid = kwargs.get("solid", True)
    instance.color = kwargs.get("color", Color.BLACK)
    instance.outline = kwargs.get("outline", 0)
    instance.catch_keyboard = kwargs.get("keyboard", False)
    instance.content = kwargs.get("content", None)
    instance.logger = kwargs.get("logger", False)
    instance._cell = None
    instance._gparent = None
    instance._owners = set()
    if kwargs.get("owner", None):
        instance.owner = kwargs.get("owner")
    return instance


class GDummy(Gid):

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GDummy, self).__init__()
        update_attributes(self, name, x, y, dx, dy, **kwargs)

    @property
    def x(self):
        """x property returns the graphical object position in the X-axis.
        """
        return self._x

    @x.setter
    def x(self, val):
        """x setter sets the graphical object position in the X-axis and sync
        that with the rectangle that contains the object.
        """
        self._x = int(val)

    @property
    def y(self):
        """y property returns the graphical object position in the y-axis.
        """
        return self._y

    @y.setter
    def y(self, val):
        """y setter sets the graphical object position in the Y-axis and sync
        that with the rectangle that contains the object.
        """
        self._y = int(val)

    @property
    def dx(self):
        """dx property returns the graphical object width or X-axis size.
        """
        return self._dx

    @dx.setter
    def dx(self, val):
        """dx setter sets the graphical object width or X-axis size.
        """
        self._dx = int(val)

    @property
    def dy(self):
        """dy property returns the graphical object height or Y-axis size.
        """
        return self._dy

    @dy.setter
    def dy(self, val):
        """dy setter sets the graphical object heigh or Y-axis size.
        """
        self._dy = int(val)

    @property
    def highlighted(self):
        """highlighted property returns the graphical object _highlighted attribute.
        """
        return self._highlighted

    @highlighted.setter
    def highlighted(self, val):
        """highlighted setter set the graphical object _highlighted attribute.
        """
        self._highlighted = val

    @property
    def parent(self):
        """parent property returns _gparent which represents the graphica parent
        instance.

        Returns:
            Object: parent instance.
        """
        return self._gparent

    @parent.setter
    def parent(self, val):
        """parent property setter sets _gparent attribute with the given value,
        which represents the graphical parent instance.

        Args:
            val (Object): instance to set as parent.
        """
        self._gparent = val

    @property
    def owner(self):
        """owner property returns all owners

        Returns:
            Set: set structure with all owners.
        """
        return self._owners

    @owner.setter
    def owner(self, val):
        """owner property setter sets a new owner.

        Args:
            val (Object): new owner instance.
        """
        self._owners.add(val)


class GObject(pygame.sprite.Sprite):
    """GObject contains all information related with any object to be
    placed or used by the GHandler.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GObject, self).__init__()
        self.__gid = new_gid()
        self.image = pygame.Surface((dx, dy), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move = kwargs.get("move", Move())
        update_attributes(self, name, x, y, dx, dy, **kwargs)

    @property
    def gid(self):
        """gid property returns the graphical id.
        """
        return self.__gid

    @property
    def x(self):
        """x property returns the graphical object position in the X-axis.
        """
        return self._x

    @x.setter
    def x(self, val):
        """x setter sets the graphical object position in the X-axis and sync
        that with the rectangle that contains the object.
        """
        self._x = int(val)
        self.rect.x = self._x

    @property
    def y(self):
        """y property returns the graphical object position in the y-axis.
        """
        return self._y

    @y.setter
    def y(self, val):
        """y setter sets the graphical object position in the Y-axis and sync
        that with the rectangle that contains the object.
        """
        self._y = int(val)
        self.rect.y = self._y

    @property
    def dx(self):
        """dx property returns the graphical object width or X-axis size.
        """
        return self._dx

    @dx.setter
    def dx(self, val):
        """dx setter sets the graphical object width or X-axis size.
        """
        self._dx = int(val)
        self.image = pygame.transform.scale(self.image, (self._dx, self._dy))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    @property
    def dy(self):
        """dy property returns the graphical object height or Y-axis size.
        """
        return self._dy

    @dy.setter
    def dy(self, val):
        """dy setter sets the graphical object heigh or Y-axis size.
        """
        self._dy = int(val)
        self.image = pygame.transform.scale(self.image, (self._dx, self._dy))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    @property
    def highlighted(self):
        """highlighted property returns the graphical object _highlighted attribute.
        """
        return self._highlighted

    @highlighted.setter
    def highlighted(self, val):
        """highlighted setter set the graphical object _highlighted attribute.
        """
        self._highlighted = val

    @property
    def parent(self):
        """parent property returns _gparent attribute, which represents there
        graphical parent instance.

        Returns:
            Object: parent instance.
        """
        return self._gparent

    @parent.setter
    def parent(self, val):
        """parent property setter sets _gparent attribute with the given value,
        which represnts the graphical parent instance.

        Args:
            val (Object): instance to set as parent.
        """
        self._gparent = val

    @property
    def owner(self):
        """owner property returns all owners

        Returns:
            Set: set structure with all owners.
        """
        return self._owners

    @owner.setter
    def owner(self, val):
        """owner property setter sets a new owner.

        Args:
            val (Object): new owner instance.
        """
        self._owners.add(val)

    # @property
    # def layer(self):
    #     """layer property returns the graphical object _layer attribute.
    #     """
    #     return self._layer

    # @layer.setter
    # def layer(self, val):
    #     """layer setter set the graphical object _layer attribute.
    #     """
    #     self._layer = val

    def dxdy(self, dx=None, dy=None):
        """dxdy allows to set the graphical object width and height at the
        same time, X-axis and Y-axis dimensions.
        """
        self._dx = int(dx) if dx is not None else self._dx
        self._dy = int(dy) if dy is not None else self._dy
        self.image = pygame.transform.scale(self.image, (self._dx, self._dy))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | {self.x} {self.y} {self.dx} {self.dy}"

    def reverse(self):
        """reverse inverts movement with the same speed value.
        """
        return self.move.reverse()

    def bounce_x(self):
        """bounce_x bounces against an X-plane, it means y-component will
        be reversed.
        """
        return self.move.bounce_x()

    def bounce_y(self):
        """bounce_y bounces against an Y-plane, it means x-component will
        be reversed.
        """
        return self.move.bounce_y()

    def move_inc(self, inc_x, inc_y, dry=False):
        """move_inc moves the grafical object by the given x and y components.
        """
        if dry:
            return (self.x + inc_x, self.y + inc_y)
        self.x += inc_x
        self.y += inc_y
        return (self.x, self.y)

    def move_to(self, x, y):
        """move_to moves the grafical object to the given position.
        """
        self.x = x
        self.y = y

    def scale(self, dx, dy):
        """scale transfor the graphical object based on given x and y
        percentages.
        """
        self.dxdy(dx, dy)

    def start_tick(self):
        """start_tick should set all elements ready for a new tick.
        """
        pass

    def end_tick(self):
        """end_tick shoudl set all elements ready for the end of a tick. Any
        structure to be clean up can be done at this point.
        """
        pass

    def move_it(self, dx, dy, dry=False):
        """move_it moves a shape the given X and Y offsets. Grid position
        and graphical position are stored and move delta is stored. It moreover
        updates gridx and gridy attributes if update flag is True.
        """
        return self.move_inc(dx, dy, dry)

    def handle_keyboard_event(self, event, **kwargs):
        """handle_keyboard_event should process the keyboard event given.
        """
        # Log.GObject(self.name).KeyboardEvent(event.key).call()
        # if self.catch_keyboard:
        #     if pygame.key.get_pressed()[pygame.K_SPACE]:
        #         Log.GObject(self.name).KeyboardEvent(event.key).Shoot().call()
        return True

    def handle_custom_event(self, event, **kwargs):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        return True

    def handle_mouse_event(self, event, **kwargs):
        """handle_mouse_event should process the mouse event given.
        Mouse events are passed to the active scene to be handle.
        """
        pass

    def out_of_bounds_x_response(self):
        """out_of_bounds_x_response takes action when the graphical object is
        out of bound at the X-axis.
        Return True if objects is lost out of bound or False if object should
        be in bounds.
        """
        self.bounce_x()
        return False

    def out_of_bounds_y_response(self):
        """out_of_bounds_x_response takes action when the graphical object is
        out of bound at the X-axis.
        Return True if objects is lost out of bound or False if object should
        be in bounds.
        """
        self.bounce_y()
        return False

    def collide_with(self, other):
        """collide_with processes a collision with other object.
        """
        pass

    def mouse_over(self, mouse_pos):
        """mouse_over is called when mouse is over the graphical object.
        """
        print(f"mouse {mouse_pos} is over me {self}")

    def update(self, surface, **kwargs):
        """update updates x and y compoments based on the move attribute
        x and y components.
        """
        # update object based on the move attribute.
        if self.move:
            self.move_inc(self.move.x, self.move.y)
        if kwargs.get("dirty"):
            for owner in self.owner:
                owner.notify(self, "UPDATED")

    def render(self, surface, **kwargs):
        """render should draws the instance on the given surface.
        """
        pass

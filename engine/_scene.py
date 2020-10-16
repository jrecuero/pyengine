import pygame
# from ._loggar import Log
from ._gid import Gid
from ._gevent import GEvent
from ._loggar import Log


class Scene(Gid):
    """Scene class identifies a pyplay scene. A scene can contain multiple
    elements like boards, objects, ...
    Scene will handle all those instances, calling proper update and render
    for each of them.
    """

    def __init__(self, name, surface, **kwargs):
        super(Scene, self).__init__()
        self.name = name
        self.surface = surface
        self.sprites = pygame.sprite.LayeredUpdates()
        self.gobjects = []
        self.timers = []
        self.enable = kwargs.get("enable", True)
        self.visible = kwargs.get("visible", True)

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name}"

    def add_gobject(self, gobject):
        """add_gobject adds a graphical object to the scene.
        """
        if isinstance(gobject, pygame.sprite.Sprite):
            if gobject in self.sprites:
                raise Exception(f"object {object} already present in sprite list")
            self.sprites.add(gobject)
        else:
            if gobject in self.gobjects:
                raise Exception(f"object {object} already present in gobject list")
            self.gobjects.append(gobject)

    def del_gobject(self, gobject):
        """del_object deletes a graphical object from the scene.
        """
        if gobject in self.sprites:
            self.sprites.remove(gobject)
        if gobject in self.gobjects:
            self.gobjects.remove(gobject)

    def open(self, **kwargs):
        """open is called when transitioning into the scene.
        """
        pass

    def close(self, **kwargs):
        """close is called when transitioning out of the scene.
        """
        pass

    def start_tick(self):
        """start_tick should set all elements ready for a new tick.
        """
        for gobj in self.sprites:
            gobj.start_tick()
        for gobj in self.gobjects:
            gobj.start_tick()

    def end_tick(self):
        """end_tick shoudl set all elements ready for the end of a tick. Any
        structure to be clean up can be done at this point.
        """
        for gobj in self.sprites:
            gobj.end_tick()
        for gobj in self.gobjects:
            gobj.end_tick()

    def handle_keyboard_event(self, event, **kwargs):
        """handle_keyboard_event should process the keyboard event given.
        """
        # Log.Scene(self.name).KeyboardEvent(event.key).call()
        for gobj in self.sprites:
            gobj.handle_keyboard_event(event, **kwargs)
        for gobj in self.gobjects:
            gobj.handle_keyboard_event(event, **kwargs)

    def handle_mouse_event(self, event, **kwargs):
        """handle_mouse_event should process the mouse event given.
        Mouse events are passed to the active scene to be handle.
        """
        for gobj in self.sprites:
            gobj.handle_mouse_event(event, **kwargs)
        for gobj in self.gobjects:
            gobj.handle_mouse_event(event, **kwargs)

    def handle_custom_event(self, event, **kwargs):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        logger_event_message = None
        if GEvent.check_destination(event, GEvent.SCENE) and event.type == GEvent.ENGINE:
            if event.subtype == GEvent.LOGGER:
                Log.Grid(self.name).Event(event).call()
                logger_event_message = event.payload
        for gobj in self.gobjects:
            if gobj.logger and logger_event_message:
                gobj.messages = logger_event_message
            gobj.handle_custom_event(event, **kwargs)
        for gobj in self.sprites:
            if gobj.logger and logger_event_message:
                gobj.messages = logger_event_message
            gobj.handle_custom_event(event, **kwargs)

    def update(self, **kwargs):
        """update calls update method for all scene graphical objects.
        """
        for gobj in self.sprites:
            gobj.update(self.surface, **kwargs)
        for gobj in self.gobjects:
            gobj.update(self.surface, **kwargs)

    def render(self, **kwargs):
        """render calls render method for all scene graphical objects.
        """
        self.sprites.draw(self.surface)

        for gobj in self.gobjects:
            gobj.render(self.surface, **kwargs)

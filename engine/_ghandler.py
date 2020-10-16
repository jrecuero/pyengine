import sys
import pygame
from ._hscene import SceneHandler
from ._loggar import Log


class GHandler:
    """GHandler controls all scenes in the app. Any scene has to be
    registered to the game handler, as any other global instance that is
    scene independent.
    GHandler will be in charge to call update and render methods for
    all those instances (scenes and any other app global instance).
    """

    EBUCKET = "event-bucket"

    def __init__(self, name, surface, clock, **kwargs):
        Log.GHandler(f"{name}").Stage("init").call()
        self.name = name
        self.surface = surface
        self.hscene = SceneHandler()
        self.gobjects = []
        self.timers = []
        self.clock = clock
        self.running = True
        self.event_bucket = []

    def add_gobject(self, gobject):
        """add_gobject adds a graphical object to the game handler.
        """
        self.gobjects.append(gobject)
        return gobject

    def del_gobject(self, gobject):
        """del_gobject deletes a graphical object from the game handler.
        """
        if gobject in self.gobjects:
            self.gobjects.remove(gobject)
        return gobject

    def add_scene(self, scene):
        """add_scene adds an scene to the game handler.
        """
        self.hscene.add(scene)
        return scene

    def del_scene(self, scene):
        """del_scene deletes an scene from the game handler.
        """
        self.hscene.delete(scene)
        return scene

    def start_tick(self):
        """start_tick should set all elements ready for a new tick.
        """
        self.hscene.start_tick()

    def end_tick(self):
        """end_tick shoudl set all elements ready for the end of a tick. Any
        structure to be clean up can be done at this point.
        """
        self.hscene.end_tick()

    def start_match(self):
        """start_match proceeds to start a match and it will call all
        objects involved in the match like skills, ...
        """
        pass

    def end_match(self):
        """end_match proceeds to end a match and it will call all objects
        that were involved in the match like skills.
        """
        pass

    def start(self, **kwargs):
        """start starts the game handler.
        """
        pass

    def stop(self, **kwargs):
        """stop stops the game handler.
        """
        pass

    def reset(self, **kwargs):
        """reset resets and reinitializes the game handler.
        """
        pass

    def handle_custom_event(self, event, **kwargs):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        self.hscene.handle_custom_event(event, **kwargs)

    def handle_keyboard_event(self, event, **kwargs):
        """handle_keyboard_event should process the keyboard event given.
        Keyboard events are passed to the active scene to be handle.
        """
        self.hscene.handle_keyboard_event(event, **kwargs)

    def handle_mouse_event(self, event, **kwargs):
        """handle_mouse_event should process the mouse event given.
        Mouse events are passed to the active scene to be handle.
        """
        self.hscene.handle_mouse_event(event, **kwargs)

    def event_handler(self, events=None, keyboards=None, buttons=None, **kwargs):
        """event_handler provides a common and basic event handler to be added
        to the application.
        """
        events = events if events else pygame.event.get()
        keyboards = keyboards if keyboards else [pygame.KEYDOWN, pygame.KEYUP]
        buttons = buttons if buttons else [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]
        kwargs[GHandler.EBUCKET] = self.event_bucket
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type in keyboards:
                self.handle_keyboard_event(event, **kwargs)
            elif event.type in buttons:
                self.handle_mouse_event(event, **kwargs)
            elif event.type >= pygame.USEREVENT:
                self.handle_custom_event(event, **kwargs)

    def update(self, **kwargs):
        """update calls update method for all scenes and  graphical objects.
        """
        # call only the active scene.
        # Log.GHandler(f"{self.name}").Update(kwargs).Clock(self.clock).call()
        kwargs[GHandler.EBUCKET] = self.event_bucket
        self.hscene.update(**kwargs)
        for gobj in self.gobjects:
            gobj.update(self.surface, **kwargs)

    def render(self, **kwargs):
        """render calls render method for all scenes and graphical objects.

        Kwargs:
            flip (bool): call pygame to flip surface.
        """
        # call only the active scene.
        kwargs[GHandler.EBUCKET] = self.event_bucket
        self.hscene.render(**kwargs)
        for gobj in self.gobjects:
            gobj.render(self.surface, **kwargs)

        # By default flip surface calling pygame.
        if kwargs.get("flip", True):
            pygame.display.flip()

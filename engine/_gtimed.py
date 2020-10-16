import sys
import pygame
from ._gevent import GEvent
from ._gobject import GObject
from ._loggar import Log


class GTimed(GObject):
    """GTimed contains all information with any graphical object that requires
    a timer in order to work.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GTimed, self).__init__(name, x, y, dx, dy, **kwargs)
        pygame.draw.rect(self.image, self.color, (0, 0, self.dx, self.dy), self.outline)
        self.timed_tick = 0
        self.timed_tick_counter = 0
        self.timed_threshold = kwargs.get("timed_threshold", 100)
        self.timed_counter = kwargs.get("timed_counter", 0)
        self.timed_event_type = kwargs.get("timed_event_type", GEvent.CALLBACK)
        self.timed_event_subtype = kwargs.get("timed_event_subtype", GEvent.MOVE_TO)
        self.timed_event_destination = kwargs.get("timed_destination", GEvent.BOARD)

    def timed_callback(self, dx, dy):
        """timed_callback is the function to be executed every time timer expires.
        """
        def _timed_callback():
            # self.move_it(dx, dy)
            if self.timed_tick_counter == 3:
                GEvent.new_event(
                    self.timed_event_type,
                    GEvent.DELETE,
                    self,
                    self.timed_event_destination,
                    {
                        "callback": None,
                        "validation": None,
                    })
        return _timed_callback

    def update(self, surface, **kwargs):
        """update updates object.
        """
        super(GTimed, self).update(surface, **kwargs)
        if self.timed_counter == 0 or self.timed_counter > self.timed_tick_counter:
            if self.timed_tick == sys.maxsize:
                self.timed_tick = 0
            if self.timed_tick_counter == sys.maxsize:
                self.timed_tick_counter = 0
            self.timed_tick += 1
            if self.timed_tick % self.timed_threshold == 0:
                self.timed_tick_counter += 1
                Log.Update(self.name).Counter(self.timed_tick).call()
                GEvent.new_event(
                    self.timed_event_type,
                    self.timed_event_subtype,
                    self,
                    self.timed_event_destination,
                    {
                        "callback": self.timed_callback(self.dx, self.dy),
                        "validation": lambda: (self.dx, self.dy)
                    })

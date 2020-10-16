from pyengine import GHandler


class GameHandler(GHandler):

    def __init__(self, surface, clock, **kwargs):
        super(GameHandler, self).__init__("Gritty", surface, clock, **kwargs)

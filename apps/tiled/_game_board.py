# import sys
# import pygame
from pyengine import Grid
# from pyengine import Log


class GameBoard(Grid):

    def __init__(self, rows, cols, grid_origin_x, grid_origin_y, cell_width, cell_height, camera_width, camera_height, **kwargs):
        super(GameBoard, self).__init__("Game Board", rows, cols, grid_origin_x, grid_origin_y, cell_width, cell_height, camera_width, camera_height, **kwargs)
        self.player_turn = True
        self.off_player_counter = 0

    def handle_keyboard_event(self, event, **kwargs):
        """handle_keyboard_event should process the keyboard event given.
        """
        if self.player_turn:
            super(GameBoard, self).handle_keyboard_event(event, **kwargs)

    def handle_custom_event(self, event, **kwargs):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        super(GameBoard, self).handle_custom_event(event, **kwargs)

    def update(self, surface, **kwargs):
        """update provides any functionality to be done every tick.
        """
        super(GameBoard, self).update(surface, **kwargs)
        # event_bucket = kwargs["event-bucket"]
        # bucket = []
        # while len(event_bucket):
        #     event = event_bucket.pop(0)
        #     # Log.Scene(self.name).EventUpdateBucket(event).call()
        #     if event.type == GEvent.ENGINE and event.subtype == GEvent.DELETE and event.destination == GEvent.BOARD:
        #         self.del_gobject(event.source)
        #         event.destination = GEvent.SCENE
        #         bucket.append(event)
        # event_bucket.extend(bucket)

# import sys
# import pygame
from pyengine import Grid, GEvent
from pyengine import Log


class GameBoard(Grid):

    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

    def __init__(self, rows, cols, g_x, g_y, g_dx, g_dy, **kwargs):
        super(GameBoard, self).__init__("Game Board", rows, cols, g_x, g_y, g_dx, g_dy, **kwargs)
        self.player_turn = True
        self.off_player_counter = 0

    def move_player_to(self, direction):
        """move_player_to moves the player to the given direction.
        """
        if self.catch_keyboard_gobject and self.player_turn:
            if direction == GameBoard.LEFT:
                ok, collision = self.move_it_gobject(self.catch_keyboard_gobject, -self.g_cell_size.x, 0)
            elif direction == GameBoard.RIGHT:
                ok, collision = self.move_it_gobject(self.catch_keyboard_gobject, self.g_cell_size.x, 0)
            elif direction == GameBoard.UP:
                ok, collision = self.move_it_gobject(self.catch_keyboard_gobject, 0, -self.g_cell_size.y)
            elif direction == GameBoard.DOWN:
                ok, collision = self.move_it_gobject(self.catch_keyboard_gobject, 0, self.g_cell_size.y)
            else:
                return False, None
            if ok:
                self.player_turn = False
                Log.Board(self.name).EndPlayerTurn().call()
            return ok, collision
        return True, None

    def move_player_left(self):
        """move_player_left moves the player to the left.
        """
        return self.move_player_to(GameBoard.LEFT)
        # if self.catch_keyboard_gobject and self.player_turn:
        #     ok, collision = self.move_it_gobject(self.catch_keyboard_gobject, -self.g_cell_size.x, 0)
        #     if ok:
        #         self.player_turn = False
        #         Log.Board(self.name).EndPlayerTurn().call()
        #     return ok, collision
        # return True, None

    def move_player_right(self):
        """move_player_right moves the player to the right.
        """
        return self.move_player_to(GameBoard.RIGHT)
        # if self.catch_keyboard_gobject and self.player_turn:
        #     ok, collision = self.move_it_gobject(self.catch_keyboard_gobject, self.g_cell_size.x, 0)
        #     if ok:
        #         self.player_turn = False
        #         Log.Board(self.name).EndPlayerTurn().call()
        #     return ok, collision
        # return True, None

    def move_player_up(self):
        """move_player_up moves the player to the up.
        """
        return self.move_player_to(GameBoard.UP)
        # if self.catch_keyboard_gobject and self.player_turn:
        #     ok, collision = self.move_it_gobject(self.catch_keyboard_gobject, 0, -self.g_cell_size.y)
        #     if ok:
        #         self.player_turn = False
        #         Log.Board(self.name).EndPlayerTurn().call()
        #     return ok, collision
        # return True, None

    def move_player_down(self):
        """move_player_down moves the player to the down.
        """
        return self.move_player_to(GameBoard.DOWN)
        # if self.catch_keyboard_gobject and self.player_turn:
        #     ok, collision = self.move_it_gobject(self.catch_keyboard_gobject, 0, self.g_cell_size.y)
        #     if ok:
        #         self.player_turn = False
        #         Log.Board(self.name).EndPlayerTurn().call()
        #     return ok, collision
        # return True, None

    def handle_keyboard_event(self, event, **kwargs):
        """handle_keyboard_event should process the keyboard event given.
        """
        # if self.running:
        #     key_pressed = pygame.key.get_pressed()
        #     if key_pressed[pygame.K_x]:
        #         sys.exit(0)
        #     if self.catch_keyboard_gobject and self.player_turn:
        #         key_pressed = pygame.key.get_pressed()
        #         Log.Grid(self.name).KeyboardEvent(event).GObject(self.catch_keyboard_gobject.name).call()
        #         if key_pressed[pygame.K_LEFT]:
        #             self.move_it_gobject(self.catch_keyboard_gobject, -self.g_cell_size.x, 0)
        #         if key_pressed[pygame.K_RIGHT]:
        #             self.move_it_gobject(self.catch_keyboard_gobject, self.g_cell_size.x, 0)
        #         if key_pressed[pygame.K_UP]:
        #             self.move_it_gobject(self.catch_keyboard_gobject, 0, -self.g_cell_size.y)
        #         if key_pressed[pygame.K_DOWN]:
        #             self.move_it_gobject(self.catch_keyboard_gobject, 0, self.g_cell_size.y)
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
        if not self.player_turn:
            self.off_player_counter += 1
            if self.off_player_counter >= 2:
                self.off_player_counter = 0
                self.player_turn = True
                Log.Board(self.name).StartPlayerTurn().call()
        super(GameBoard, self).update(surface, **kwargs)
        event_bucket = kwargs["event-bucket"]
        bucket = []
        while len(event_bucket):
            event = event_bucket.pop(0)
            # Log.Scene(self.name).EventUpdateBucket(event).call()
            if event.type == GEvent.ENGINE and event.subtype == GEvent.DELETE and event.destination == GEvent.BOARD:
                self.del_gobject(event.source)
                event.destination = GEvent.SCENE
                bucket.append(event)
        event_bucket.extend(bucket)

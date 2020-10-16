from ._loggar import Log
from ._cell import Cell
from ._layer import Layer
from ._gobject import GDummy
from ._grect import GRect
from ._gobstacle import GObstacle
from ._color import Color
from ._gevent import GEvent
import pygame
from pygame.math import Vector2


class Grid(GDummy):
    """Class Grid identifies a grid containing a group of ordered cells to be
    displayed at fixed positions/
    """

    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

    def __init__(self, name, rows, cols, grid_origin_x, grid_origin_y, cell_width, cell_height, camera_height, camera_width, **kwargs):
        self.rows = rows
        self.cols = cols
        self.g_cell_size = pygame.Rect(0, 0, cell_width, cell_height)
        self.g_origin = Vector2(grid_origin_x, grid_origin_y)
        self.g_size = pygame.Rect(0, 0, cols * self.g_cell_size.width, rows * self.g_cell_size.height)
        super(Grid, self).__init__(name, self.g_origin.x, self.g_origin.y, self.g_size.width, self.g_size.height, **kwargs)
        self.db = [[Cell(i, j) for j in range(self.cols)] for i in range(self.rows)]
        self.catch_keyboard_gobject = None
        self.camera = pygame.Rect(0, 0, camera_width, camera_height)
        self.player = None
        self.player_position = None
        self.camera_follow = None
        self.gobjects = pygame.sprite.LayeredUpdates()
        self.tile_map = None
        self.running = True
        self.render_grid = kwargs.get("render_grid", True)
        self.image = pygame.Surface((self.g_size.width, self.g_size.height), pygame.SRCALPHA)

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__} ({self.x}, {self.y}) ({self.dx}, {self.dy})"

    def cell(self, row, col):
        """cell returns the grid cell at the given coordinates.
        """
        return self.db[row][col]

    def g_cell(self, row, col):
        """g_cell returns the pixel location for the cell at the given
        coordinates.
        """
        return Vector2(col * self.g_cell_size.width, row * self.g_cell_size.height)

    def g_to_cell(self, x, y):
        """g_to_cell translates graphical x-y coordinates to grid row/col values.
        """
        col = x / self.g_cell_size.width
        row = y / self.g_cell_size.height
        return int(row), int(col)

    def g_cell_rect(self, row, col):
        """g_cell_rect returns a rectangle with for the given cell.
        """
        origin = self.g_cell(row, col)
        return pygame.Rect(origin.x, origin.y, self.g_cell_size.width, self.g_cell_size.height)

    def _points_in_line(self, start, length, delta):
        """_points_in_line returns all points contained in a line of lenght,
        at an start and with an increment of delta.
        """
        result = []
        while start < length:
            result.append(start)
            start += delta
        return result

    def g_cells_in_rect(self, rect):
        """g_cells_in_rect returns all graphical cell contained in a graphical
        rectangle.
        """
        cells = []
        xs = self._points_in_line(rect.x, rect.x + rect.width, self.g_cell_size.width)
        ys = self._points_in_line(rect.y, rect.y + rect.height, self.g_cell_size.height)
        for yy in ys:
            for xx in xs:
                cells.append((yy, xx))
        return cells

    def cells_in_rect(self, rect):
        """cells_in_rect returns all cells contained in a graphical rectangle.
        """
        return [self.g_to_cell(x, y) for (x, y) in self.g_cells_in_rect(rect)]

    def grid_rect(self):
        """grid_rect returns a rectangle for the while grid.
        """
        return pygame.Rect(self.g_origin.x, self.g_origin.y, self.g_size.width, self.g_size.height)

    def in_bounds(self, row, col):
        """in_bounds returns in the given location is inside the grid or not.
        """
        return (0 <= row < self.rows) and (0 <= col < self.cols)

    def add_gobject_to_cell(self, gobject):
        """add_gobject_to_cell add a graphical object to the cell related with the
        gobject position.
        """
        row, col = self.g_to_cell(gobject.x, gobject.y)
        Log.Grid(self.name).AddGObjToCell(gobject.name).Cell(f"{row}, {col}").XY(f"{gobject.x}, {gobject.y}").call()
        cell = self.cell(row, col)
        cell.add_gobject(gobject)

    def del_gobject_from_cell(self, gobject):
        """del_gobject_from_cell removes the graphical object from the cell related
        with the gobject position.
        """
        cell = gobject._cell
        if cell:
            cell.del_gobject(gobject)
            Log.Grid(self.name).DelGObjFromCell(gobject.name).Cell(f"{cell.row}, {cell.col}").XY(f"{gobject.x}, {gobject.y}").call()

    def add_gobject(self, gobject, relative=False, player=False):
        """add_gobject adds a graphical object to the grid.
        """
        if gobject.catch_keyboard and self.catch_keyboard_gobject:
            raise Exception(f"Already configured catch keyboard gobject: {self.catch_keyboard_gobject}")
        # self.gobjects.add(gobject, layer=gobject.layer)
        self.gobjects.add(gobject)
        if player:
            self.player = gobject
            if self.player_position:
                gobject.x = self.player_position.x
                gobject.y = self.player_position.y
        if gobject.catch_keyboard:
            self.catch_keyboard_gobject = gobject

        # if relative:
        #     gobject.x += self.g_origin.x
        #     gobject.y += self.g_origin.y
        self.add_gobject_to_cell(gobject)

    def add_tilemap(self, tile_map, relative=True):
        """add_tilemap adds a TileMap object to the grid.
        """
        self.tile_map = tile_map
        for tobj in tile_map.objects:
            Log.Grid(self.name).Obstacle(tobj.name).At(f"{tobj.x}, {tobj.y}").Size(f"{tobj.width}. {tobj.height}").call()
            if tobj.type == "obstacle":
                g_cells = self.g_cells_in_rect(tobj)
                # Log.Grid(self.name).Cells(g_cells).call()
                for y, x in [(x1, y1) for (x1, y1) in g_cells if x1 < self.g_size.width and y1 < self.g_size.height]:
                    self.add_gobject(GObstacle(tobj.name, x, y, self.g_cell_size.width, self.g_cell_size.height, layer=Layer.TOP))
            elif tobj.type == "treasure":
                self.add_gobject(GRect(tobj.name, tobj.x, tobj.y, self.g_cell_size.width, self.g_cell_size.height, layer=Layer.TOP, color=Color.RED))
            elif tobj.type == "player" and tobj.name == "start-position":
                # self.add_gobject(GRect(tobj.name, tobj.x, tobj.y, self.g_cell_size.width, self.g_cell_size.height, layer=Layer.TOP, color=Color.BLUE))
                self.player_position = pygame.math.Vector2(tobj.x, tobj.y)
                if self.player:
                    self.player.x = tobj.x
                    self.player.y = tobj.y

    def del_gobject(self, gobject):
        """del_gobject deletes a graphical object from the grid.
        """
        self.gobjects.remove(gobject)
        if gobject._cell:
            self.del_gobject_from_cell(gobject)

    def camera_follow_gobject(self, gobject):
        """camera_follow_gobject sets the attribute camera_follow with the given object.
        """
        self.camera_follow = gobject

    def start_tick(self):
        """start_tick should set all elements ready for a new tick.
        """
        for gobj in [o for _, go in self.gobjects.items() for o in go]:
            gobj.start_tick()

    def end_tick(self):
        """end_tick shoudl set all elements ready for the end of a tick. Any
        structure to be clean up can be done at this point.
        """
        for gobj in [o for _, go in self.gobjects.items() for o in go]:
            gobj.end_tick()

    def can_move_to(self, gobject, move_shift_x=None, move_shift_y=None):
        """can_move_to checks if the given object can move the given x-y delta.
        It returns a boolean with the movement result (True move allowed,
        False, not) and a cell instance if there is a collision.
        - Movement allowed: True, None
        - Movement not allowed (out of bounds): False, None
        - Movement not allowed (collision): False, collision-cell
        """
        move_shift_x, move_shift_y = int(move_shift_x), int(move_shift_y)
        new_x, new_y = gobject.move_it(move_shift_x, move_shift_y, dry=True)
        row, col = self.g_to_cell(new_x, new_y)
        if (0 <= row < self.rows) and (0 <= col < self.cols):
            if not self.cell(row, col).collision(gobject):
                return True, None
            return False, self.cell(row, col)
        return False, None

    def move_it_gobject(self, gobject, move_shift_x, move_shift_y):
        """move_it_gobject moves the given object the given x-y delta.
        It returns a boolean with the movement result (True move allowed,
        False, not) and a cell instance if there is a collision.
        - Movement allowed: True, None
        - Movement not allowed (out of bounds): False, None
        - Movement not allowed (collision): False, collision-cell
        """
        move_shift_x, move_shift_y = int(move_shift_x), int(move_shift_y)
        new_x, new_y = gobject.move_it(move_shift_x, move_shift_y, dry=True)
        row, col = self.g_to_cell(new_x, new_y)
        if (0 <= row < self.rows) and (0 <= col < self.cols):
            if not self.cell(row, col).collision(gobject):
                self.del_gobject_from_cell(gobject)
                gobject.move_it(move_shift_x, move_shift_y)
                self.add_gobject_to_cell(gobject)
                return True, None
            return False, self.cell(row, col)
        return False, None

    def move_gobject_to(self, direction):
        """move_gobject_to moves the gobject to the given direction.
        """
        if self.catch_keyboard_gobject:
            if direction == Grid.LEFT:
                ok, collision = self.move_it_gobject(self.catch_keyboard_gobject, -self.g_cell_size.width, 0)
            elif direction == Grid.RIGHT:
                ok, collision = self.move_it_gobject(self.catch_keyboard_gobject, self.g_cell_size.width, 0)
            elif direction == Grid.UP:
                ok, collision = self.move_it_gobject(self.catch_keyboard_gobject, 0, -self.g_cell_size.height)
            elif direction == Grid.DOWN:
                ok, collision = self.move_it_gobject(self.catch_keyboard_gobject, 0, self.g_cell_size.height)
            else:
                return False, None
            return ok, collision
        return True, None

    def move_gobject_left(self):
        """move_gobject_left moves the gobject to the left.
        """
        return self.move_gobject_to(Grid.LEFT)

    def move_gobject_right(self):
        """move_gobject_right moves the gobject to the right.
        """
        return self.move_gobject_to(Grid.RIGHT)

    def move_gobject_up(self):
        """move_gobject_up moves the gobject to the up.
        """
        return self.move_gobject_to(Grid.UP)

    def move_gobject_down(self):
        """move_gobject_down moves the gobject to the down.
        """
        return self.move_gobject_to(Grid.DOWN)

    def handle_keyboard_event(self, event, **kwargs):
        """handle_keyboard_event should process the keyboard event given.
        """
        # Log.Grid(self.name).KeyboardEvent(event.key).call()
        if self.running:
            for gobj in self.gobjects:
                gobj.handle_keyboard_event(event, **kwargs)

    def handle_mouse_event(self, event, **kwargs):
        """handle_mouse_event should process the mouse event given.
        Mouse events are passed to the active scene to be handle.
        """
        for gobj in self.gobjects:
            gobj.handle_mouse_event(event, **kwargs)

    def handle_custom_event(self, event, **kwargs):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        if event.destination == GEvent.BOARD and event.type == GEvent.CALLBACK:
            Log.Grid(self.name).Event(event.source).Payload(str(event.payload)).call()
            if event.subtype == GEvent.MOVE_TO:
                new_pos = pygame.math.Vector2(event.payload["validation"]())
                ok, _ = self.move_it_gobject(event.source, new_pos.x, new_pos.y)
                if ok:
                    event.payload["callback"]()
            elif event.subtype == GEvent.DELETE:
                self.del_gobject(event.source)
        for gobj in self.gobjects:
            gobj.handle_custom_event(event, **kwargs)

    def update(self, surface, **kwargs):
        """update provides any functionality to be done every tick.
        """
        for gobj in self.gobjects:
            gobj.update(surface, **kwargs)
        if self.camera_follow:
            if self.camera.width < self.g_size.width or self.camera.height < self.g_size.height:
                camera_x = self.camera_follow.x
                camera_y = self.camera_follow.y
                Log.Grid(self.name).Cell(f"{self.g_to_cell(self.camera_follow.x, self.camera_follow.y)}").Follow(f"{self.camera_follow.x}, {self.camera_follow.y}").Position(f"{camera_x}, {camera_y}").Camera(self.camera).Size(self.g_size).call()
                if (camera_x >= self.camera.width / 2) and (self.g_size.width - camera_x >= self.camera.width / 2):
                    Log.Grid(self.name).NewCamera(self.camera).call()
                    self.camera.x = (self.camera_follow.x - self.camera.width / 2)
                if (camera_y >= self.camera.height / 2) and (self.g_size.height - camera_y >= self.camera.height / 2):
                    self.camera.y = (self.camera_follow.y - self.camera.height / 2)

    def render(self, surface, **kwargs):
        """render should draws the instance on the given surface.
        """
        if self.render_grid:
            for row in range(self.rows + 1):
                r = row * self.g_cell_size.height
                pygame.draw.line(self.image, Color.BLACK, (0, r), (self.g_size.width, r))
            for col in range(self.cols + 1):
                c = col * self.g_cell_size.width
                pygame.draw.line(self.image, Color.BLACK, (c, 0), (c, self.g_size.height))

        if self.tile_map:
            # self.tile_map.render(self.image, origin=pygame.Vector2(self.g_origin.x, self.g_origin.y), area=(0, 0, self.g_size.width, self.g_size.height), **kwargs)
            self.tile_map.render(self.image, origin=pygame.Vector2(0, 0), area=(0, 0, self.g_size.width, self.g_size.height), **kwargs)
        self.gobjects.draw(self.image)
        surface.blit(self.image, (self.g_origin.x, self.g_origin.y), area=self.camera)
        # surface.blit(self.image, (0, 0), area=self.camera)

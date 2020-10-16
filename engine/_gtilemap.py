import pygame
import pytmx
# from ._gobject import GObject
from ._loggar import Log


class TileMap:

    def __init__(self, filename):
        self.tmxdata = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight
        self.objects = []

    def render(self, surface):
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmxdata.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
        for to in self.tmxdata.objects:
            Log.TmxObject(to.name).Position(f"{to.x}, {to.y}").Size(f"{to.width}, {to.height}").Image(to.image).call()
            for k, v in to.properties.items():
                Log.TmxObjectx(to.name).Properties(f"{k}: {v}").call()
            self.objects.append(to)
            if to.image:
                surface.blit(to.image, (to.x, to.y))

    def make_map(self, **kwargs):
        width = kwargs.get("width", self.width)
        height = kwargs.get("height", self.height)
        temp_surface = pygame.Surface((width, height))
        self.render(temp_surface)
        return temp_surface


class GTileMap():

    def __init__(self, name, tile_map, x, y, **kwargs):
        self.name = name
        self.x = x
        self.y = y
        self.tile_map = tile_map
        self.image = self.tile_map.make_map()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    @property
    def objects(self):
        return self.tile_map.objects

    def render(self, surface, **kwargs):
        origin = kwargs.get("origin", pygame.Vector2(self.x, self.y))
        area = kwargs.get("area", None)
        surface.blit(self.image, (origin.x, origin.y), area=area)

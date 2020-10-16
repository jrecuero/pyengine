import os
import pygame
from ._gid import Gid


class GLoader(Gid):

    def __init__(self, name):
        super(GLoader, self).__init__()
        self.name = name
        self.image_db = {}
        self.sound_db = {}

    def load_image(self, path, filename):
        """load_image loads an image. If the image has already been loaded, it
        returns the cached version instead of loading it again.
        """
        f_name = os.path.join(path, filename)
        if f_name not in self.image_db:
            self.image_db[f_name] = pygame.image.load(f_name)
        return self.image_db[f_name]

    def load_sound(self, path, filename):
        """load_sound loads a sound. If the sound has already been loaded, it
        returns the cached version instead of loading it again.
        """
        f_name = os.path.join(path, filename)
        if f_name not in self.sound_db:
            self.sound_db[f_name] = pygame.mixer.Sound(f_name)
        return self.sound_db[f_name]

    def load_music(self, path, filename):
        """load_music loads a music file.
        """
        pygame.mixer.music.load(os.path.join(path, filename))

from ._gobject import GObject


class GImage(GObject):
    """GImage implements a graphical object that is rendered as an image from
    an image.
    """

    def __init__(self, name, image, x, y, **kwargs):
        rect = image.get_rect()
        super(GImage, self).__init__(name, x, y, rect.width, rect.height, **kwargs)
        self.image = image
        # self.rect = rect

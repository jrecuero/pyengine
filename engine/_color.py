import pygame


class Color:
    """Color represents some predefined pygame colors to be used across the
    application.
    """

    WHITE = pygame.Color(255, 255, 255)
    BLACK = pygame.Color(0, 0, 0)
    RED = pygame.Color(255, 0, 0)
    GREEN = pygame.Color(0, 128, 0)
    BLUE = pygame.Color(0, 0, 255)
    ALPHA = pygame.Color(255, 255, 255, 0)

    @staticmethod
    def color_to_str(color):
        """color_to_str returns the given color as a string.
        """
        if color == Color.WHITE:
            return "white"
        elif color == Color.BLACK:
            return "black"
        elif color == Color.RED:
            return "red"
        elif color == Color.GREEN:
            return "green"
        elif color == Color.BLUE:
            return "blue"
        else:
            return "none"

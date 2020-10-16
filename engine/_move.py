import random
import pygame

# from ._loggar import log


class Move:
    """Move defines movement for any graphical object in the application.
    """

    def __init__(self, x=None, y=None, speed=None):
        x = x if x is not None else 0
        y = y if y is not None else 0
        self.vector = pygame.math.Vector2(x, y)
        self.speed = speed
        self._shadow_vector = None

    def __str__(self):
        return f"({self.vector.x}, {self.vector.y}) @ {self.speed}"

    @property
    def x(self):
        """x property returns the X-axis movement component.
        """
        return self.vector.x

    @property
    def y(self):
        """y property returns the Y-axis movement component.
        """
        return self.vector.y

    @property
    def speed(self):
        """speed property returns the value for _speed attribute. This is the
        measure for the movement.
        """
        return self.__speed

    @speed.setter
    def speed(self, speed):
        """speed sets a new speed value for the move instance. Vector will
        be updated to fit the new speed value.
        """
        if (self.vector.x == 0) and (self.vector.y == 0):
            self.__speed = 0
        elif speed:
            self.vector.scale_to_length(speed)
            self.__speed = speed
        elif speed is None:
            self.__speed = self.vector.length()
        else:
            self.__speed = 0
            self.vector.x = 0
            self.vector.y = 0

    def is_up(self):
        """is_up checks if movement has an UP component.
        """
        return self.vector.y < 0

    def is_down(self):
        """is_down checks if movement has an DOWN component.
        """
        return self.vector.y > 0

    def is_right(self):
        """is_right checks if movement has an RIGHT component.
        """
        return self.vector.x > 0

    def is_left(self):
        """is_left checks if movement has an LEFT component.
        """
        return self.vector.x < 0

    def reverse(self):
        """reverse changes the vector to the oposite direction and sense.
        """
        self.vector.x = self.vector.x * (-1)
        self.vector.y = self.vector.y * (-1)
        return self.vector

    def bounce_x(self):
        """bounce_x bounces against an X-plane, it means y-component will
        be reversed.
        """
        self.vector.x = self.vector.x * (-1)
        return self.vector

    def bounce_y(self):
        """bounce_y bounces against an Y-plane, it means x-component will
        be reversed.
        """
        self.vector.y = self.vector.y * (-1)
        return self.vector

    def any(self, speed=None):
        """any changes the direction to any other one.
        """
        self.vector = pygame.math.Vector2(random.randint(-5, 5), random.randint(-5, 5))
        self.speed = speed
        return self.vector

    def pause(self):
        """pause stops any movement. Vector value is stored in a shadow
        variable in order to be able to retrieve it later on.
        """
        self._shadow_vector = self.vector
        self.vector = pygame.math.Vector2(0, 0)

    def resume(self):
        """resume sets vector to the shadow vector value that was setup
        previously by a pause call.
        """
        if self._shadow_vector:
            self.vector = self._shadow_vector
            self._shadow_vector = None

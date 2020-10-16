__GID = 0


def new_gid():
    """new_gid generates a new graphical object identifier.
    """
    global __GID
    __GID += 1
    return __GID


class Gid:
    def __init__(self):
        self.__gid = new_gid()

    @property
    def gid(self):
        """gid property returns the graphical id.
        """
        return self.__gid

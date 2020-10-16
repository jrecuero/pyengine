class Cell:
    """Class Cell identifies every unique instance in a grid. A Cell has a
    position in the bi-dimensional grid and it can contain furher objects.
    """

    def __init__(self, row, col, gobject=None):
        self.row = row
        self.col = col
        self.gobjects = [gobject, ] if gobject else []
        self.solid = False

    def __str__(self):
        return f"({self.row}, {self.col})"

    @property
    def solid_object(self):
        for gobject in self.gobjects:
            if gobject.solid:
                return gobject
        return None

    def add_gobject(self, gobject):
        """add_gobject adds a new gobject.
        """
        self.gobjects.append(gobject)
        gobject._cell = self
        self.solid = self.solid or gobject.solid

    def del_gobject(self, gobject):
        """del_gobject removes a gobject.
        """
        self.gobjects.remove(gobject)
        gobject._cell = None
        if gobject.solid:
            self.solid = False

    def collision(self, gobject):
        """collision checks if the gobject given has a collision with the cell.
        """
        return self.solid and gobject.solid

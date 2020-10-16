from pyengine import GRect, GEvent
from pyengine import Log


class GameActor(GRect):
    """GameActor contains all information related with any actor in the
    game.
    """

    def __init__(self, name, x, y, dx, dy, **kwargs):
        super(GameActor, self).__init__(name, x, y, dx, dy, **kwargs)
        self.life = kwargs.get("life", 100)
        self.pstr = kwargs.get("pstr", 25)
        self.pdef = kwargs.get("pdef", 10)

    def __str__(self):
        return f"[{self.gid}] : {self.__class__.__name__}@{self.name} | ({self.x}, {self.y}) ({self.life}, {self.pstr} {self.pdef})"

    def attack(self, other):
        """attack implements the battle attack against the given actor.
        """
        damage = self.pstr = other.pdef
        other.life -= damage
        if other.life < 0:
            other.life = 0
        Log.GameActor(self.name).Attach(other.name).Damage(damage).call()
        return damage

    def update(self, surface, **kwargs):
        """update calls update method for game actor.
        """
        if self.life == 0:
            event_bucket = kwargs.get("event-bucket", None)
            if event_bucket is not None:
                event = GEvent.new_event(GEvent.ENGINE,
                                         GEvent.DELETE,
                                         self,
                                         GEvent.BOARD,
                                         {"source": self, }, )
                event_bucket.append(event)

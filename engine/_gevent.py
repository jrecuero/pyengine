import pygame
from ._loggar import Log


class GEvent:
    """GEvent implements all codes related with user events used in the
    application via pygame events.
    """

    NONE = 0

    # GEvent type. Used by pygame events.
    # pygame.USEREVENT = 24
    USER = pygame.USEREVENT
    ENGINE = pygame.USEREVENT + 1
    TIMER = pygame.USEREVENT + 2
    CALLBACK = pygame.USEREVENT + 3
    APP_DEFINED = pygame.USEREVENT + 4
    USER_DEFINED = pygame.USEREVENT + 5

    # GEvent subtype. Used internaly
    MOVE_TO = 1
    DELETE = 2
    CREATE = 3
    LOGGER = 4
    SUBTYPE_USER_DEFINED = 1000
    _gevent_subtypes = {
        "MOVE_TO": 1,
        "DELETE": 2,
        "CREATE": 3,
        "LOGGER": 4,
        "USER_DEFINED": 1000, }
    _gevent_subtypes_user_defined_last = 1000

    # Event Source/Destination
    HANDLER = 1
    SCENE = 2
    BOARD = 3
    OBJECT = 4
    OTHER = 5
    SRC_DST_USER_DEFINED = 1000

    @classmethod
    def register_subtype_event(cls, name):
        """register_subtype_event registers a new user defined subtype event.
        """
        if name in cls._gevent_subtypes:
            return None
        cls._gevent_subtypes_user_defined_last += 1
        cls._gevent_subtypes[name] = cls._gevent_subtypes_user_defined_last
        return cls._gevent_subtypes[name]

    @classmethod
    def get_subtype_event(cls, name):
        """get_subtype_event returns the subtype for a given user defined
        subtype event.
        """
        return cls._gevent_subtypes.get(name, None)

    @staticmethod
    def check_destination(event, dest):
        """check_destination checked if the given destination is in the event
        dest attribute.
        """
        if isinstance(event.destination, list):
            return dest in event.destination
        else:
            return dest == event.destination

    @staticmethod
    def post_event(etype, esubtype, source, destination, payload, **kwargs):
        """post_event creates and post a new event.
        """
        the_event = pygame.event.Event(etype, subtype=esubtype, source=source, destination=destination, payload=payload, **kwargs)
        pygame.event.post(the_event)
        Log.Post().Event(etype).Subtype(esubtype).Source(source).Destination(destination).Payload(str(payload)).Kwargs(kwargs).call()

    @staticmethod
    def new_event(etype, esubtype, source, destination, payload, **kwargs):
        """new_event creates a new event.
        """
        the_event = pygame.event.Event(etype, subtype=esubtype, source=source, destination=destination, payload=payload, **kwargs)
        Log.New().Event(etype).Subtype(esubtype).Source(source).Destination(destination).Payload(str(payload)).Kwargs(kwargs).call()
        return the_event

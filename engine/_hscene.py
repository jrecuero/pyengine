class SceneHandler:
    """SceneHandler is a private class to be used by GHandler in order to
    handle all scenes in the app.
    SceneHandler allows to handle scene, moving from one to other in an
    idenpendant way.
    """

    def __init__(self, **kwargs):
        self.scenes = []
        self.iactive = None

    def active(self, scene=None, **kwargs):
        """active sets the given scene as the active one. If no scene is given
        sets the first scene as the active one.
        """
        if self.iactive is not None:
            self.scenes[self.iactive].close(**kwargs)
        if scene is None:
            self.iactive = 0
        elif scene in self.scenes:
            self.iactive = self.scenes.index(scene)
        self.scenes[self.iactive].open(**kwargs)

    def enable(self, scene=None):
        """enable sets the given scene as enable. If no scene is given sets
        the active scene as enable.
        """
        if scene is None:
            if self.iactive is not None:
                self.scenes[self.iactive].enable = True
        else:
            scene.enable = True

    def disable(self, scene=None):
        """disable sets the given scene as disable. if no scene is given sets
        the active scene as disable.
        """
        if scene is None:
            if self.iactive is not None:
                self.scenes[self.iactive].enable = False
        else:
            scene.enable = False

    def visible(self, scene=None):
        """visible sets the given scene as visible. if no scene is given sets
        the active scene as visible.
        """
        if scene is None:
            if self.iactive is not None:
                self.scenes[self.iactive].visible = True
        else:
            scene.visible = True

    def hidden(self, scene=None):
        """hidden sets the given scene as not visible. if no scene is given
        sets the active scene as not visible.
        """
        if scene is None:
            if self.iactive is not None:
                self.scenes[self.iactive].visible = False
        else:
            scene.visible = False

    def add(self, scene):
        """add adds a new scene.
        """
        index = len(self.scenes)
        self.scenes.append(scene)
        return index

    def delete(self, scene):
        """delete deletes an existing scene.
        """
        if scene in self.scenes:
            self.scenes.remove(scene)

    def scene(self):
        """scene returns the active scene.
        """
        if self.iactive is not None and self.scenes:
            return self.scenes[self.iactive]
        return None

    def next(self, **kwargs):
        """next moves to the next available scene. close will be called for
        the old active  scene and open will be called for the new active
        scene.
        """
        if self.iactive is not None and self.scenes:
            if (self.iactive + 1) < len(self.scenes):
                self.scenes[self.iactive].close(**kwargs)
                self.iactive = (self.iactive + 1) % len(self.scenes)
                self.scenes[self.iactive].open(**kwargs)

    def prev(self, **kwargs):
        """prev moves to the previous available scene. close will be called for
        the old active  scene and open will be called for the new active
        scene.
        """
        if self.iactive is not None and self.scenes:
            if (self.iactive - 1) >= 0:
                self.scenes[self.iactive].close(**kwargs)
                self.iactive = abs(self.iactive - 1) % len(self.scenes)
                self.scenes[self.iactive].open(**kwargs)

    def first(self, **kwargs):
        """first moves to the first available scene. close will be called for
        the old active  scene and open will be called for the new active
        scene.
        """
        if self.iactive is not None and self.scenes:
            self.scenes[self.iactive].close(**kwargs)
            self.iactive = 0
            self.scenes[self.iactive].open(**kwargs)

    def last(self, **kwargs):
        """last moves to the last available scene. close will be called for
        the old active  scene and open will be called for the new active
        scene.
        """
        if self.iactive is not None and self.scenes:
            self.scenes[self.iactive].close(**kwargs)
            self.iactive = len(self.scences) - 1
            self.scenes[self.iactive].open(**kwargs)

    def start_tick(self):
        """start_tick should set all elements ready for a new tick.
        """
        if self.iactive is not None and self.scenes:
            self.scenes[self.iactive].start_tick()

    def end_tick(self):
        """end_tick shoudl set all elements ready for the end of a tick. Any
        structure to be clean up can be done at this point.
        """
        if self.iactive is not None and self.scenes:
            self.scenes[self.iactive].end_tick()

    def handle_keyboard_event(self, event, **kwargs):
        """handle_keyboard_event should process the keyboard event given.
        Keyboard events are passed to the active scene to be handle.
        """
        if self.iactive is not None and self.scenes:
            self.scenes[self.iactive].handle_keyboard_event(event, **kwargs)

    def handle_mouse_event(self, event, **kwargs):
        """handle_mouse_event should process the mouse event given.
        Mouse events are passed to the active scene to be handle.
        """
        if self.iactive is not None and self.scenes:
            self.scenes[self.iactive].handle_mouse_event(event, **kwargs)

    def handle_custom_event(self, event, **kwargs):
        """handle_custom_event should process pygame custom event given.
        Any object in the game, like, scene, graphic objects, ... can post
        customs events, and those should be handled at this time.
        """
        if self.iactive is not None and self.scenes:
            self.scenes[self.iactive].handle_custom_event(event, **kwargs)

    def update(self, **kwargs):
        """update calls update for the active scene.
        """
        if self.scene():
            self.scene().update(**kwargs)

    def render(self, **kwargs):
        """render calls render for the active scene.
        """
        if self.scene():
            self.scene().render(**kwargs)

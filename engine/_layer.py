class Layer:

    BACKGROUND = -1
    GROUND = 0
    TOP = 2

    @classmethod
    def layer_to_string(cls, layer):
        if layer == cls.BACKGROUND:
            return "background"
        elif layer == cls.GROUND:
            return "ground"
        elif layer == cls.TOP:
            return "top"
        else:
            raise Exception(f"Unknown layer: {layer}")

    @classmethod
    def layers(cls):
        return [cls.BACKGROUND, cls.GROUND, cls.TOP]

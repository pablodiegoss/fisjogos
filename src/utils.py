


def move_to_floor(pyxel_object):
    floor_height = 0
    pyxel_object.y = GameConfig().height - pyxel_object.height - floor_height





class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class GameConfig(metaclass=SingletonMeta):
    width = 0
    height = 0
    fps = 0

    def get_screen_size(self):
        return (self.width, self.height)



from math import cos, sin, sqrt, pi
from pymunk import Transform, Vec2d
import pyxel


def move_to_floor(pyxel_object):
    floor_height = 3
    pyxel_object.y = GameConfig().height - pyxel_object.height - floor_height


def get_rot_mat(angle_rad):
    cos_ = cos(angle_rad)
    sin_ = sin(angle_rad)
    return Transform(a=cos_, b=sin_, c=-sin_, d=cos_, tx=0, ty=0)


def get_mouse_pos():
    return Vec2d(pyxel.mouse_x, pyxel.mouse_y)


def group_tri(seq):
    x, y, *rest = seq
    for z in rest:
        yield (x, y, z)
        y = z


def draw_poly(shape, color):
    for tri in group_tri(shape.get_vertices()):
        coords = []
        for v in tri:
            x, y = v.rotated(shape.body.angle) + shape.body.position
            coords.extend((x, y))
        pyxel.trib(*coords, color)


def edist(p, q):
    return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))


def invertAngle(angle):
    return (angle + pi) % (2 * pi)


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

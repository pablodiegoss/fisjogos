from math import cos, sin, sqrt, pi
from pymunk import Transform, Vec2d, Circle, Segment, Poly
import pyxel


def get_mouse_pos():
    return Vec2d(pyxel.mouse_x, pyxel.mouse_y) - pyxel.camera_offset


def get_mouse_angle(player):
    origin = player.slingshot.get_nock_origin()
    slingshot_horizontal_line = Vec2d(origin[0] + GameConfig().width, origin[1])
    mouse_pos = get_mouse_pos()

    slingshot_horizontal_line = slingshot_horizontal_line - origin
    mouse_pos = mouse_pos - origin

    return (
        mouse_pos.get_angle_degrees_between(slingshot_horizontal_line),
        mouse_pos.get_angle_between(slingshot_horizontal_line),
    )

def move_camera_to_player(player):
    move_camera_to(player.x - GameConfig().width / 2, 0)

def move_camera_by(x, y=0):
    pyxel.camera_offset[0] += x
    pyxel.camera_offset[1] += y
    if tuple(pyxel.camera_offset) < (-430, 0):
            pyxel.camera_offset = Vec2d(-430, 0)
    if tuple(pyxel.camera_offset) > (399, 0):
            pyxel.camera_offset = Vec2d(399, 0)

def move_camera_to(x, y):
    # base_center_offset = Vec2d(108.5, 128.0)
    pyxel.camera_offset = Vec2d(-x, y)

def draw_shape(shape, offset, color=pyxel.COLOR_RED):
    if isinstance(shape, Circle):
        pyxel.circb(*(shape.body.position + offset + shape.offset), shape.radius, color)
    elif isinstance(shape, Segment):
        ax, ay = shape.body.local_to_world(shape.a) + offset
        bx, by = shape.body.local_to_world(shape.b) + offset
        pyxel.line(ax, ay, bx, by, color)
    elif isinstance(shape, Poly):
        draw_poly(shape, offset, color)


def group_triangles(vertices):
    x, y, *rest = vertices
    for z in rest:
        yield (x, y, z)
        y = z


def draw_poly(shape, camera_offset, color):
    for tri in group_triangles(shape.get_vertices()):
        coords = []
        for v in tri:
            x, y = v.rotated(shape.body.angle) + shape.body.position + camera_offset
            coords.extend((x, y))
        pyxel.trib(*coords, color)


def edist(p, q):
    return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))


def invert_angle(angle):
    return (angle + pi) % (2 * pi)


def player_generator():
    while True:
        for player in pyxel.players:
            yield player
            # yield pyxel.players[0]


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

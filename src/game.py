import pyxel
from pymunk import Transform
from .models import *
from .utils import *
from math import cos, sin

tile = lambda x: x * 8
gc = GameConfig()


def get_mouse_angle():
    origin = pyxel.player1.get_shoulder()
    shoulder_horizontal_line = Vec2d(origin[0] + gc.width, origin[1])
    mouse_pos = Vec2d(pyxel.mouse_x, pyxel.mouse_y)

    shoulder_horizontal_line = shoulder_horizontal_line - origin
    mouse_pos = mouse_pos - origin
    return (
        mouse_pos.get_angle_degrees_between(shoulder_horizontal_line),
        mouse_pos.get_angle_between(shoulder_horizontal_line),
    )


def get_rot_mat(angle_rad):
    cos_ = cos(angle_rad)
    sin_ = sin(angle_rad)
    return Transform(a=cos_, b=sin_, c=-sin_, d=cos_, tx=0, ty=0)


def update():
    pyxel.angle, pyxel.angle_rad = get_mouse_angle()
    if pyxel.btnp(pyxel.KEY_UP, period=3):
        pyxel.force += 1
        if pyxel.force > 100:
            pyxel.force = 100
    if pyxel.btnp(pyxel.KEY_DOWN, period=3):
        pyxel.force -= 1
        if pyxel.force < 0:
            pyxel.force = 0
    p = pyxel.player1

    m = get_rot_mat(pyxel.angle_rad)
    p.bow.draw_pos = p.bow.pos - p.get_shoulder()
    p.bow.draw_pos = m * (p.bow.draw_pos)
    p.bow.draw_pos += p.get_shoulder()

def draw():
    pyxel.cls(pyxel.COLOR_WHITE)
    pyxel.bltm(0, 0, 0, 0, 0, tile(4), tile(3), pyxel.COLOR_WHITE)
    for o in pyxel.objects:
        o.draw()

    
    draw_hud()


def draw_hud():
    text = f'Angle = {"{:.3f}".format(pyxel.angle)} [mouse]'
    pyxel.text(pyxel.player1.x + 20, pyxel.player1.y + 15, text, pyxel.COLOR_BLACK)
    text = f"Force = {pyxel.force} [up|down]"
    pyxel.text(pyxel.player1.x + 20, pyxel.player1.y + 22, text, pyxel.COLOR_BLACK)


def set_up():
    pyxel.player1 = Player(15, 0, Sprite.BLUE)
    pyxel.player2 = Player(195, 0, Sprite.RED)
    tree = PyxelObject(64 * 4 / 2 - Sprite.TREE.value.width / 2, 0, Sprite.TREE)
    pyxel.objects = [
        pyxel.player1,
        PyxelObject(1, 0, Sprite.GROUND_ARROW),
        Arrow(45, 0),
        tree,
        Arrow(150, 0, Sprite.RED_ARROW),
        pyxel.player2,
        PyxelObject(205, 0, Sprite.GROUND_ARROW),
    ]
    for o in pyxel.objects:
        move_to_floor(o)
    tree.y += 3
    pyxel.force = 0

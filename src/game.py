import pyxel
from .models import *
from .utils import *
from math import acos, pi

tile = lambda x: x * 8
gc = GameConfig()


def get_mouse_angle():
    origin = pyxel.player1.get_shoulder()
    shoulder_horizontal_line = Vec2d(origin[0] + gc.width, origin[1])
    mouse_pos = Vec2d(pyxel.mouse_x, pyxel.mouse_y)

    shoulder_horizontal_line = shoulder_horizontal_line - origin
    mouse_pos = mouse_pos - origin
    return mouse_pos.get_angle_degrees_between(shoulder_horizontal_line)


def update():
    pyxel.angle = get_mouse_angle()


def draw():
    pyxel.cls(pyxel.COLOR_WHITE)
    pyxel.bltm(0, 0, 0, 0, 0, tile(4), tile(3), pyxel.COLOR_WHITE)
    for o in pyxel.objects:
        move_to_floor(o)
        o.draw()


    draw_hud()


def draw_hud():
    text = f"angle = {pyxel.angle} [z|x]"
    pyxel.text(pyxel.player1.x + 20, pyxel.player1.y + 20, text, pyxel.COLOR_BLACK)


def set_up():
    pyxel.player1 = Player(15, 0, Sprite.BLUE)
    pyxel.player2 = Player(195, 0, Sprite.RED)
    tree = PyxelObject(64 * 4 / 2 - Sprite.TREE.value.width / 2, 0, Sprite.TREE)
    pyxel.objects = [
        pyxel.player1,
        PyxelObject(1, 0, Sprite.GROUND_ARROW),
        PyxelObject(45, 0, Sprite.BLUE_ARROW),
        tree,
        PyxelObject(150, 0, Sprite.RED_ARROW),
        pyxel.player2,
        PyxelObject(205, 0, Sprite.GROUND_ARROW),
    ]
    for o in pyxel.objects:
        move_to_floor(o)
    tree.y += 3

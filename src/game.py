import pyxel
from .models import *
from .utils import *

def update():
    pass


tile = lambda x: x*8

def draw():
    pyxel.cls(pyxel.COLOR_WHITE)
    gc = GameConfig()
    pyxel.bltm(0,0,0,0,0,tile(4),tile(3),pyxel.COLOR_WHITE)
    tree = PyxelObject(gc.width/2 - Sprite.TREE.value.width/2,0, Sprite.TREE)
    objects= [
        PyxelObject(1,0, Sprite.GROUND_ARROW),
        Player(15, 0, Sprite.BLUE),
        PyxelObject(45,0, Sprite.BLUE_ARROW),
        tree,
        PyxelObject(150,0, Sprite.RED_ARROW),
        Player(195,0, Sprite.RED),
        PyxelObject(205,0, Sprite.GROUND_ARROW),
    ]
    for o in objects:
        move_to_floor(o)
        tree.y = tree.y + 3
        o.draw()


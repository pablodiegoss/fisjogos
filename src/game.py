import pyxel
from .models import *
from .utils import *

def update():
    pass


def draw():
    pyxel.cls(pyxel.COLOR_WHITE)
    gc = GameConfig()
    objects= [
        PyxelObject(1,0, Sprite.GROUND_ARROW),
        Player(15, 0, Sprite.BLUE),
        PyxelObject(45,0, Sprite.BLUE_ARROW),
        PyxelObject(gc.width/2 - Sprite.TREE.value.width/2,0, Sprite.TREE),
        PyxelObject(150,0, Sprite.RED_ARROW),
        Player(195,0, Sprite.RED),
        PyxelObject(205,0, Sprite.GROUND_ARROW),
    ]
    for o in objects:
        move_to_floor(o)
        o.draw()    



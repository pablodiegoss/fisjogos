import pyxel
from .models import *
from .utils import *

def update():
    pass


def draw():
    pyxel.cls(pyxel.COLOR_WHITE)

    p = Player(10, 0)
    e = Enemy(80,0)
    t = Tree(50,0)
    move_to_floor(p)
    move_to_floor(e)
    move_to_floor(t)

    p.draw()
    e.draw()
    t.draw()
    



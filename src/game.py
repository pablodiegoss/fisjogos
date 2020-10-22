import pyxel
from .models import *

def update():
    pass


def draw():
    pyxel.cls(pyxel.COLOR_WHITE)

    p = Player(10, 10)
    e = Enemy(60,10)
    p.draw()
    e.draw()




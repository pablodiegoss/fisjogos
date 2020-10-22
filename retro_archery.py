"""Archery Game based on Pyxel and Pymunk"""

__version__ = "0.0.1"

from src import update, draw
import pyxel

FPS = 60

if __name__ == "__main__":
    pyxel.init(120, 90, fps=FPS, caption="Retro Archery Challenge")
    pyxel.mouse(True)
    pyxel.load("res/my_resource.pyxres")
    pyxel.run(update, draw)


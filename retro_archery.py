"""Archery Game based on Pyxel and Pymunk"""

__version__ = "0.0.1"

from src import update, draw, GameConfig
import pyxel

FPS = 60
SCREEN_SIZE = (220, 150)


if __name__ == "__main__":
    gc = GameConfig()
    gc.fps = FPS
    gc.width = SCREEN_SIZE[0]
    gc.height = SCREEN_SIZE[1]
    pyxel.init(gc.width, gc.height, fps=gc.fps, caption="Retro Archery Challenge")
    pyxel.mouse(True)
    pyxel.load("res/my_resource.pyxres")
    pyxel.run(update, draw)

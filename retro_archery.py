"""Archery Game based on Pyxel and Pymunk"""

__version__ = "0.0.1"

from src import update, draw, GameConfig, set_up
import pyxel

FPS = 60
PYXEL_TILE_SIZE = 64
SCREEN_SIZE = (PYXEL_TILE_SIZE * 4, PYXEL_TILE_SIZE * 3)


if __name__ == "__main__":
    gc = GameConfig()
    gc.fps = FPS
    gc.width = SCREEN_SIZE[0]
    gc.height = SCREEN_SIZE[1]
    pyxel.init(gc.width, gc.height, fps=gc.fps, caption="Retro Archery Challenge")
    pyxel.mouse(True)
    pyxel.load("res/my_resource.pyxres")
    set_up()
    pyxel.run(update, draw)

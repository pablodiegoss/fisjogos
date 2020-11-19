import pyxel
from .utils import GameConfig

tile = lambda x: x * 8


def draw_background():
    pyxel.cls(pyxel.COLOR_WHITE)
    pyxel.bltm(
        *((-400, 0) + pyxel.camera_offset),
        0,
        0,
        0,
        tile(17),
        tile(3),
        pyxel.COLOR_WHITE,
    )


def draw_hud():
    text = f'Angle = {"{:.1f}".format(pyxel.angle)} [mouse]'
    pyxel.text(
        pyxel.active_player.x + 20, pyxel.active_player.y + 15, text, pyxel.COLOR_BLACK
    )
    text = f'Force = {"{:.1f}".format(pyxel.force)} [mouse distance]'
    pyxel.text(
        pyxel.active_player.x + 20, pyxel.active_player.y + 22, text, pyxel.COLOR_BLACK
    )

    pyxel.wind.draw(GameConfig().width / 2, 12)

    draw_hp_bar("P1", pyxel.players[0].life, 1, 8)
    draw_hp_bar("P2", pyxel.players[1].life, 195, 8)


def draw_hp_bar(name, player_life, x, y):
    pyxel.text(x, y, name, pyxel.COLOR_BLACK)
    pyxel.rect(x + 8, y - 3, 51, 11, pyxel.COLOR_BLACK)
    pyxel.rect(x + 9, y - 2, 49 * (player_life / 100), 9, pyxel.COLOR_GREEN)
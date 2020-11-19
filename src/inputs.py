import pyxel
from pymunk import Vec2d
from .cooldowns import Cooldown, TimedEvent


def check_game_inputs():
    if pyxel.btnp(pyxel.KEY_C, period=100):
        pyxel.collisors = not pyxel.collisors

    if pyxel.btnp(pyxel.KEY_J, period=2):
        pyxel.camera_offset += (+3, 0)
        if tuple(pyxel.camera_offset) > (399, 0):
            pyxel.camera_offset = Vec2d(399, 0)

    if pyxel.btnp(pyxel.KEY_K, period=2):
        pyxel.camera_offset += (-3, 0)
        if tuple(pyxel.camera_offset) < (-430, 0):
            pyxel.camera_offset = Vec2d(-430, 0)

    if pyxel.btnp(pyxel.KEY_U, period=2):
        pyxel.wind.direction += (1, 0)
        print(pyxel.wind.direction)
    if pyxel.btnp(pyxel.KEY_I, period=2):
        pyxel.wind.direction += (0, 1)
        print(pyxel.wind.direction)
    if pyxel.btnp(pyxel.KEY_N, period=2):
        pyxel.wind.direction += (-1, 0)
        print(pyxel.wind.direction)
    if pyxel.btnp(pyxel.KEY_M, period=2):
        pyxel.wind.direction += (0, -1)
        print(pyxel.wind.direction)

    check_shoot(pyxel.active_player)


def check_shoot(player):
    if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and Cooldown.check(TimedEvent.SHOT_TIMEOUT):
        player.shoot()
        Cooldown.activate(TimedEvent.SHOT_TIMEOUT)
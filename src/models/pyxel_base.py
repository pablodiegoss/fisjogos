import pyxel
from enum import Enum
from pymunk import Vec2d, Body, Circle


class SpriteData:
    def __init__(self, sprite_page, sprite_x, sprite_y, width, height, color_alpha):
        self.sprite_page = sprite_page
        self.sprite_x = sprite_x
        self.sprite_y = sprite_y
        self.width = width
        self.height = height
        self.color_alpha = color_alpha

    def as_tuple(self):
        return (
            self.sprite_page,
            self.sprite_x,
            self.sprite_y,
            self.width,
            self.height,
            self.color_alpha,
        )


class Sprite(Enum):
    # Sprite Page, Sprite X, Sprite Y, Width, Height, Color Alpha.
    BLUE = SpriteData(0, 3, 3, 10, 28, 2)
    RED = SpriteData(0, 19, 3, 10, 28, 2)
    TREE = SpriteData(0, 60, 0, 39, 64, pyxel.COLOR_WHITE)
    ROCK = SpriteData(0, 18, 34, 10, 8, pyxel.COLOR_PURPLE)
    BLUE_SLING = SpriteData(0, 36, 32, 9, 16, pyxel.COLOR_WHITE)
    RED_SLING = SpriteData(0, 36, 48, 9, 16, pyxel.COLOR_WHITE)


class PyxelObject:
    def __init__(self, x, y, sprite):
        self.shapes = []
        self.body = Body(body_type=Body.KINEMATIC)
        self.body.position = (x, y)
        self.sprite = sprite
        self.width = sprite.value.width
        self.height = sprite.value.height
        self.is_active = True

    @property
    def x(self):
        return self.body.position[0]

    @x.setter
    def x(self, x):
        self.body.position = (x, self.y)

    @property
    def y(self):
        return self.body.position[1]

    @y.setter
    def y(self, y):
        self.body.position = (self.x, y)

    def blit(self):
        return (*self.body.position, *self.sprite.value.as_tuple())

    def draw(self, collisors=None):
        pyxel.blt(*self.blit())

    def update(self):
        pass

    def adjust(self, position):
        width = self.sprite.value.width
        height = self.sprite.value.height
        return (position[0] + width / 2, position[1] + height / 2)

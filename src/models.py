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
    BOW = SpriteData(0, 0, 32, 13, 17, pyxel.COLOR_WHITE)
    BOW_INVERTED = SpriteData(0, 0, 32, -13, 17, pyxel.COLOR_WHITE)
    TREE = SpriteData(0, 60, 0, 39, 64, pyxel.COLOR_WHITE)
    GROUND_ARROW = SpriteData(0, 32, 21, 16, 11, pyxel.COLOR_WHITE)
    RED_ARROW = SpriteData(0, 33, 0, 15, 5, pyxel.COLOR_WHITE)
    BLUE_ARROW = SpriteData(0, 33, 7, 15, 5, pyxel.COLOR_WHITE)
    ROCK = SpriteData(0,18,34,10,8,pyxel.COLOR_PURPLE)


class PyxelObject:
    def __init__(self, x, y, sprite):
        self.pos = Vec2d(0,0)
        self.draw_pos = Vec2d(0,0)
        self.x = x
        self.y = y
        self.sprite = sprite
        self.width = sprite.value.width
        self.height = sprite.value.height

    @property
    def x(self):
        return self.pos.x

    @x.setter
    def x(self, x):
        self.pos.x = x

    @property
    def y(self):
        return self.pos.y

    @y.setter
    def y(self, y):
        self.pos.y = y

    def blit(self):
        return (self.x, self.y, *self.sprite.value.as_tuple())

    def draw(self):
        pyxel.blt(*self.blit())


class Bow(PyxelObject):
    def __init__(self, x, y):
        super().__init__(x, y, Sprite.BOW)

    def get_handle(self):
        return Vec2d(self.draw_pos.x + self.width, self.draw_pos.y + self.height / 2)

    def get_string(self):
        return Vec2d(self.draw_pos.x, self.draw_pos.y + self.height / 2)
    
    def blit(self):
        return (self.draw_pos.x, self.draw_pos.y, *self.sprite.value.as_tuple())


class Player(PyxelObject):
    bow_offset = (3, 5)

    def __init__(self, x, y, sprite):
        self.bow = Bow(0, 0)
        if sprite.value == Sprite.RED.value:
            self.bow_offset = (-6, 5)
            self.bow.sprite = Sprite.BOW_INVERTED
        super().__init__(x, y, sprite)

    @property   
    def x(self):
        return self.pos.x

    @x.setter
    def x(self, x):
        self.pos.x = x
        self.bow.x = x + self.bow_offset[0]

    @property
    def y(self):
        return self.pos.y

    @y.setter
    def y(self, y):
        self.pos.y = y
        self.bow.y = y + self.bow_offset[1]

    def get_shoulder(self):
        shoulder_position = Vec2d(self.x + self.width / 2, self.y + (self.height / 2) - 4)
        return shoulder_position

    def draw(self):
        super().draw()
        shoulder_position = self.get_shoulder()

        # bow arm
        pyxel.line(*shoulder_position, *self.bow.get_handle(), pyxel.COLOR_BLACK)
        self.bow.draw()

        # string arm
        elbow_position = (self.x - 2, shoulder_position[1] + 2)
        pyxel.line(*shoulder_position, *elbow_position, pyxel.COLOR_BLACK)
        pyxel.line(*elbow_position, *self.bow.get_string(), pyxel.COLOR_BLACK)


class Rock(PyxelObject):
    def __init__(self, x, y, sprite = Sprite.ROCK):
        super().__init__(x, y, sprite)
        self.body = Body(mass=1, moment=1)
        self.body.position = (x,y)
        self.shape = Circle(self.body, 10)
        self.shape.elasticity = 0.1
    def blit(self):
        return (*self.body.position, *self.sprite.value.as_tuple())



from ..utils import get_rot_mat
from .pyxel_base import *

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

    def draw(self, collisors=None):
        super().draw()
        shoulder_position = self.get_shoulder()

        # bow arm
        pyxel.line(*shoulder_position, *self.bow.get_handle(), pyxel.COLOR_BLACK)
        self.bow.draw()

        # string arm
        elbow_position = (self.x - 2, shoulder_position[1] + 2)
        pyxel.line(*shoulder_position, *elbow_position, pyxel.COLOR_BLACK)
        pyxel.line(*elbow_position, *self.bow.get_string(), pyxel.COLOR_BLACK)

    def update(self):
        m = get_rot_mat(pyxel.angle_rad)
        self.bow.draw_pos = self.bow.pos - self.get_shoulder()
        self.bow.draw_pos = m * (self.bow.draw_pos)
        self.bow.draw_pos += self.get_shoulder()



    
class Rock(PyxelObject):
    def __init__(self, x, y, sprite = Sprite.ROCK):
        super().__init__(x, y, sprite)
        self.body = Body(mass=1, moment=1)
        self.body.position = (x,y)
        self.shape = Circle(self.body, sprite.value.width/2.4)
        self.shape.elasticity = 0.1

    def blit(self):
        return (*self.body.position, *self.sprite.value.as_tuple())

    def draw(self, collisors=None):
        pyxel.blt(*self.blit())
        if(collisors):
            pyxel.circb(*(self.adjust(self.body.position)), self.shape.radius, pyxel.COLOR_RED)
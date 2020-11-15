from ..utils import get_rot_mat, GameConfig, get_mouse_pos
from .pyxel_base import *


class Slingshot(PyxelObject):
    def __init__(self, x, y):
        self.nock_offset = Vec2d(4, 1)
        super().__init__(x, y, Sprite.BLUE_SLING)
        self.nock_position = self.get_nock_origin()

    @property
    def x(self):
        return self.position.x

    @x.setter
    def x(self, x):
        self.position.x = x
        self.nock_position = self.get_nock_origin()

    @property
    def y(self):
        return self.position.y

    @y.setter
    def y(self, y):
        self.position.y = y
        self.nock_position = self.get_nock_origin()

    def get_handle(self):
        return Vec2d(self.x + self.width / 2, self.y + 2 + self.height / 2)

    def get_nock_origin(self):
        return self.position + self.nock_offset

    def left_stick(self):
        return self.get_nock_origin() - Vec2d(3, 0)

    def right_stick(self):
        return self.get_nock_origin() + Vec2d(3, 0)

    def get_nock_position(self):
        return self.nock_position

    def blit(self):
        return (self.position.x, self.position.y, *self.sprite.value.as_tuple())

    def draw(self, collisors=False):
        super().draw()
        pyxel.line(*self.nock_position, *self.left_stick(), pyxel.COLOR_BLACK)
        pyxel.line(*self.nock_position, *self.right_stick(), pyxel.COLOR_BLACK)
        if collisors:
            pyxel.circb(*self.get_nock_position(), 2, pyxel.COLOR_RED)

    def update(self):
        mouse_pos = get_mouse_pos()
        origin = self.get_nock_origin()
        nock_pos = mouse_pos - origin
        nock_pos *= -1
        self.nock_position = nock_pos + origin
        string_length = 40
        if self.nock_position.x < self.get_nock_origin().x - string_length:
            self.nock_position.x = self.get_nock_origin().x - string_length
        if self.nock_position.x >= self.get_nock_origin().x + string_length:
            self.nock_position.x = self.get_nock_origin().x + string_length

        if self.nock_position.y < self.get_nock_origin().y - string_length / 2:
            self.nock_position.y = self.get_nock_origin().y - string_length / 2
        if self.nock_position.y >= self.get_nock_origin().y + string_length / 2:
            self.nock_position.y = self.get_nock_origin().y + string_length / 2


class Player(PyxelObject):
    slingshot_offset = Vec2d(12, 0)

    def __init__(self, x, y, sprite):
        self.slingshot = Slingshot(0, 0)
        self.flipped = False
        if sprite.value == Sprite.RED.value:
            self.flipped = True
            self.slingshot_offset = (self.slingshot_offset[0] * -1, self.slingshot_offset[1])
            self.slingshot.sprite = Sprite.RED_SLING
        super().__init__(x, y, sprite)

    @property
    def x(self):
        return self.position.x

    @x.setter
    def x(self, x):
        self.position.x = x
        self.slingshot.x = x + self.slingshot_offset[0]

    @property
    def y(self):
        return self.position.y

    @y.setter
    def y(self, y):
        self.position.y = y
        self.slingshot.y = y + self.slingshot_offset[1]

    def get_shoulder(self):
        shoulder_position = Vec2d(
            self.x + self.width / 2, self.y + (self.height / 2) - 4
        )
        return shoulder_position

    def draw(self, collisors=None):
        super().draw()
        shoulder_position = self.get_shoulder()

        # slingshot arm
        pyxel.line(*shoulder_position, *self.slingshot.get_handle(), pyxel.COLOR_BLACK)
        self.slingshot.draw(collisors)

        # # string arm
        elbow_x = self.x - 2 if not self.flipped else self.x + 11
        elbow_position = (elbow_x, shoulder_position[1] + 2)
        # pyxel.line(*shoulder_position, *elslingshot_position, pyxel.COLOR_BLACK)
        # pyxel.line(*elslingshot_position, *self.slingshot.get_nock_position(), pyxel.COLOR_BLACK)

    def update(self):
        self.slingshot.update()
        # m = get_rot_mat(pyxel.angle_rad)
        # self.slingshot.draw_pos = self.slingshot.pos - self.get_shoulder()
        # self.slingshot.draw_pos = m * (self.slingshot.draw_pos)
        # self.slingshot.draw_pos += self.get_shoulder()


class Rock(PyxelObject):
    def __init__(self, x, y):
        super().__init__(x, y, Sprite.ROCK)
        self.body = Body(mass=1, moment=1)
        self.body.position = (x, y)
        self.shape = Circle(self.body, Sprite.ROCK.value.width / 2.4)
        self.shape.elasticity = 0.1

    def blit(self):
        return (*self.body.position, *self.sprite.value.as_tuple())

    def draw(self, collisors=None):
        pyxel.blt(*self.blit())
        if collisors:
            pyxel.circb(
                *(self.adjust(self.body.position)), self.shape.radius, pyxel.COLOR_RED
            )

    def update(self):
        x, y = self.body.position
        if x < -50 or x > GameConfig().width + 50:
            self.is_active = False
        if y > GameConfig().height + 50:
            self.is_active = False

class Tree(PyxelObject):
    def __init__(self, x, y):
        super().__init__(x, y, Sprite.TREE)
        self.body = Body(mass=1, moment=1)
        self.body.position = (x, y)
        self.shape = Circle(self.body, Sprite.TREE.value.width / 2.4)
        self.shape.elasticity = 0.1

    def blit(self):
        return (*self.body.position, *self.sprite.value.as_tuple())

    def draw(self, collisors=None):
        pyxel.blt(*self.blit())
        if collisors:
            pyxel.circb(
                *(self.adjust(self.body.position)), self.shape.radius, pyxel.COLOR_RED
            )

    def update(self):
        x, y = self.body.position
        if x < -50 or x > GameConfig().width + 50:
            self.is_active = False
        if y > GameConfig().height + 50:
            self.is_active = False
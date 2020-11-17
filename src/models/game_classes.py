from ..utils import get_rot_mat, GameConfig, get_mouse_pos, draw_poly
from .pyxel_base import *
from pymunk import Poly
from math import sqrt
from random import randint
import copy


class Slingshot(PyxelObject):
    def __init__(self, x, y):
        self.nock_offset = Vec2d(4, 1)
        super().__init__(x, y, Sprite.BLUE_SLING)
        self.nock_position = self.get_nock_origin()

    @property
    def x(self):
        return self.body.position[0]

    @x.setter
    def x(self, x):
        self.body.position = (x, self.y)
        self.nock_position = self.get_nock_origin()

    @property
    def y(self):
        return self.body.position[1]

    @y.setter
    def y(self, y):
        self.body.position = (self.x, y)
        self.nock_position = self.get_nock_origin()

    def get_handle(self):
        return Vec2d(self.x + self.width / 2, self.y + 2 + self.height / 2)

    def get_nock_origin(self):
        return self.body.position + self.nock_offset

    def left_stick(self):
        return self.get_nock_origin() - Vec2d(3, 0)

    def right_stick(self):
        return self.get_nock_origin() + Vec2d(3, 0)

    def get_nock_position(self):
        return self.nock_position

    def draw(self, camera_offset, collisors=False):
        super().draw(camera_offset, collisors)
        pyxel.line(
            *(self.nock_position + camera_offset),
            *(self.left_stick() + camera_offset),
            pyxel.COLOR_BLACK
        )
        pyxel.line(
            *(self.nock_position + camera_offset),
            *(self.right_stick() + camera_offset),
            pyxel.COLOR_BLACK
        )
        if collisors:
            pyxel.circb(*(self.get_nock_position() + camera_offset), 2, pyxel.COLOR_RED)

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
        super().__init__(x, y, sprite)
        self.life = 100
        self.flipped = False
        self.slingshot = Slingshot(x, y)
        if sprite.value == Sprite.RED.value:
            self.flipped = True
            self.slingshot_offset = (
                self.slingshot_offset[0] * -1,
                self.slingshot_offset[1],
            )
            self.slingshot.sprite = Sprite.RED_SLING
        self.slingshot.body.position = (
            self.slingshot.body.position + self.slingshot_offset
        )

    @property
    def x(self):
        return self.body.position[0]

    @x.setter
    def x(self, x):
        self.body.position = (x, self.y)
        self.slingshot.x = x + self.slingshot_offset[0]

    @property
    def y(self):
        return self.body.position[1]

    @y.setter
    def y(self, y):
        self.body.position = (self.x, y)
        self.slingshot.y = y + self.slingshot_offset[1]

    def get_shoulder(self):
        shoulder_position = Vec2d(
            self.x + self.width / 2, self.y + (self.height / 2) - 4
        )
        return shoulder_position

    def draw(self, camera_offset, collisors=None):
        super().draw(camera_offset, collisors)
        shoulder_position = self.get_shoulder() + camera_offset

        # slingshot arm
        pyxel.line(
            *shoulder_position,
            *(self.slingshot.get_handle() + camera_offset),
            pyxel.COLOR_BLACK
        )
        self.slingshot.draw(camera_offset, collisors)

        # # string arm
        elbow_x = self.x - 2 if not self.flipped else self.x + 11
        elbow_position = (elbow_x, shoulder_position[1] + 2) + camera_offset
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
        self.body = Body(mass=3, moment=1)
        self.body.position = (x, y)
        shape = Circle(self.body, Sprite.ROCK.value.width / 2)
        shape.elasticity = 0.8
        self.shapes.append(shape)

    def blit(self, camera_offset):
        return (
            *(self.body.position - Vec2d(4, 3) + camera_offset),
            *self.sprite.value.as_tuple(),
        )

    def update(self):
        x, y = self.body.position
        if x < -700 or x > 700:
            self.is_active = False
        if y > GameConfig().height + 650:
            self.is_active = False


class Tree(PyxelObject):
    def __init__(self, x, y):
        super().__init__(x, y, Sprite.TREE)
        # self.body = Body(body_type=Body.STATIC)
        # self.body.position = (x, y)
        top = [(0, 20), (20, 0), (40, 20)]
        top = Poly(self.body, [*top])
        top.elasticity = 0.1
        middle = [(0, 20), (0, 35), (40, 20), (40, 35)]
        middle = Poly(self.body, [*middle])
        middle.elasticity = 0.1
        bottom = [(15, 35), (25, 35), (15, 60), (25, 60)]
        bottom = Poly(self.body, [*bottom])
        bottom.elasticity = 1
        self.shapes.append(top)
        self.shapes.append(middle)
        self.shapes.append(bottom)
        pyxel.space.add(*self.shapes)


class Wind:
    def __init__(self):
        self.direction = Vec2d(0, 0)

    def get_wind(self):
        return self.direction

    def change(self):
        self.direction = Vec2d(randint(-100, 100), randint(-100, 100))

    def get_status(self):
        if max(self.direction) > 66:
            return "Strong"
        elif max(self.direction) > 33:
            return "Medium"
        else:
            return "Weak"

    def draw(self, x, y):
        sprite = self.get_arrow_direction()
        pyxel.blt(
            x - abs(sprite.width) / 2, y - abs(sprite.height) / 2, *sprite.as_tuple()
        )
        status = self.get_status()
        pyxel.text(x + 10, y - 2, status, pyxel.COLOR_BLACK)

    def get_arrow_direction(self):
        x, y = self.direction

        def x_direction(sprite):
            if x > 0:
                return sprite
            else:
                sprite.width = -sprite.width
                return sprite

        def y_direction(sprite):
            if y > 0:
                return sprite
            else:
                sprite.height = -sprite.height
                return sprite

        minimum_wind = 20
        if abs(x) < minimum_wind and abs(y) < minimum_wind:
            return Sprite.CIRCLE.value
        elif abs(x) < minimum_wind or abs(y) < minimum_wind:
            if abs(x) > abs(y):
                sprite = copy.copy(Sprite.HORIZONTAL_ARROW.value)
                return x_direction(sprite)
            else:
                sprite = copy.copy(Sprite.VERTICAL_ARROW.value)
                return y_direction(sprite)
        else:
            sprite = copy.copy(Sprite.DIAGONAL_ARROW.value)
            sprite = x_direction(sprite)
            sprite = y_direction(sprite)
            return sprite

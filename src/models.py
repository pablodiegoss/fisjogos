import pyxel


class PyxelObject:
    def __init__(
        self, x, y, sprite_page, sprite_x, sprite_y, width, height, color_alpha
    ):
        self.x = x
        self.y = y
        self.sprite_page = sprite_page
        self.sprite_x = sprite_x
        self.sprite_y = sprite_y
        self.width = width
        self.height = height
        self.color_alpha = color_alpha

    def blit(self):
        return (
            self.x,
            self.y,
            self.sprite_page,
            self.sprite_x,
            self.sprite_y,
            self.width,
            self.height,
            self.color_alpha,
        )

    def draw(self):
        pyxel.blt(*self.blit())


class Player(PyxelObject):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.sprite_x, self.sprite_y = 3, 3
        self.width, self.height = 10, 28
        self.sprite_page = 0
        self.color_alpha = 2
        self.bow = Bow(x + 2, y + 5)

    def draw(self):
        super().draw()
        shoulder_position = (self.x + self.width / 2, self.y + (self.height / 2) - 4)
        
        # bow arm
        pyxel.line(*shoulder_position, *self.bow.get_handle(), pyxel.COLOR_BLACK)
        self.bow.draw()
        
        # string arm
        elbow_position = (self.x - 2, shoulder_position[1] + 2)
        pyxel.line(*shoulder_position, *elbow_position, pyxel.COLOR_BLACK)
        pyxel.line(*elbow_position, *self.bow.get_string(), pyxel.COLOR_BLACK)


class Enemy(PyxelObject):
    def __init__(self, x, y):
        super().__init__(x, y, 0, 19, 3, 10, 28, 2)
        self.bow = Bow(x, y)

    def draw(self):
        super().draw()
        self.bow.draw()


class Bow(PyxelObject):
    def __init__(self, x, y):
        super().__init__(x, y, 0, 48, 0, 13, 17, pyxel.COLOR_WHITE)

    def get_handle(self):
        return (self.x + self.width, self.y + self.height / 2)

    def get_string(self):
        return (self.x, self.y + self.height / 2)

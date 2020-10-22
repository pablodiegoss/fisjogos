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
    @property 
    def x(self):
        return self.__x
    @x.setter
    def x(self,x):
        self.__x = x
    
    @property 
    def y(self):
        return self.__y
    @y.setter
    def y(self,y):
        self.__y = y


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

class Bow(PyxelObject):
    def __init__(self, x, y):
        super().__init__(x, y, 0, 0, 32, 13, 17, pyxel.COLOR_WHITE)

    def get_handle(self):
        return (self.x + self.width, self.y + self.height / 2)

    def get_string(self):
        return (self.x, self.y + self.height / 2)

class Player(PyxelObject):
    bow_offset = (2,5)
    bow = Bow(0,0)
    def __init__(self, x, y):
        super().__init__(
            x=x, 
            y=y, 
            sprite_page=0, 
            sprite_x=3, 
            sprite_y=3, 
            width=10, 
            height=28, 
            color_alpha=2
        )

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x
        self.bow.x = x + self.bow_offset[0]
    
    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y
        self.bow.y = y + self.bow_offset[1]
    
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
        super().__init__(
            x=x, 
            y=y, 
            sprite_page=0, 
            sprite_x=19, 
            sprite_y=3, 
            width=10, 
            height=28, 
            color_alpha=2
        )
        self.bow = Bow(x, y)

    def draw(self):
        super().draw()
        self.bow.draw()





class Tree(PyxelObject):
    def __init__(self, x, y):
        super().__init__(x, y, 0, 60, 0, 39, 64, pyxel.COLOR_WHITE)
import pyxel
import random
from math import sqrt

class Body:
    def __init__(self, pos=(0, 0), vel=(0, 0), mass=1.0, color=0):
        self.position_x, self.position_y = pos
        self.velocity_x, self.velocity_y = vel
        self.mass = mass
        self.color = color
 
        self.force_x = 0.0
        self.force_y = 0.0
 
    def apply_force(self, fx, fy):
        self.force_x += fx
        self.force_y += fy        
 
    def update_velocity(self, dt):
        acc_x = self.force_x / self.mass
        acc_y = self.force_y / self.mass
        
        self.velocity_x += acc_x * dt
        self.velocity_y += acc_y * dt
 
        self.force_x = self.force_y = 0.0
 
    def update_position(self, dt):
        self.position_x += self.velocity_x * dt
        self.position_y += self.velocity_y * dt
 
    def draw(self):
        pyxel.pset(self.position_x, self.position_y, self.color)
 

class Circle(Body):
    def __init__(self, radius, *args, **kwargs):
        self.radius = radius
        super().__init__(*args, **kwargs)
    
    def draw(self):
        pyxel.circ(self.position_x, self.position_y, self.radius, self.color)

class Rect(Body):
    def __init__(self, width, height, *args, **kwargs):
        self.width = width
        self.height = height
        super().__init__(*args, **kwargs)
    
    def draw(self):
        pyxel.rect(self.position_x,self.position_y, self.width, self.height, self.color)

class Space:
    def __init__(self):
        self.bodies = []
 
    def add_body(self, body):
        self.bodies.append(body)
 
    def add_circle(self, *args, **kwargs):
        circle = Circle(*args, **kwargs)
        self.add_body(circle)
        return circle
    
    def add_rect(self, *args, **kwargs):
        rect = Rect(*args, **kwargs)
        self.add_body(rect)
        return rect
    # tri, lines, ...
 
    def update(self, dt):
        for body in self.bodies:
            body.update_velocity(dt)
 
        for body in self.bodies:
            body.update_position(dt)
 
    def draw(self):
        for body in self.bodies:
            body.draw()
 
FPS = 60
dt = 1 / FPS
pyxel.init(180, 120, fps=FPS)
 
sp = Space()
cte = 10000

# for _ in range(50):
sp.add_circle(
    radius=random.uniform(2, 7),
    pos=(100, 100),
    vel=(0,20),
    color=random.randrange(16),
)
sp.add_circle(
    radius=random.uniform(2, 7),
    pos=(120, 100),
    vel=(0,-20),
    color=random.randrange(16),
)

def calcular_gravidade(body1, body2):
    dx = body1.position_x - body2.position_x
    dy = body1.position_y - body2.position_y
    r = sqrt(dx**2 + dy**2)

    # Aqui vocês podem colocar várias outras expressões: isso representa o módulo da força
    F = -cte / r**2
    Fx = dx / r * F
    Fy = dy / r * F
    return (Fx,Fy)

def update():
    forca1 = calcular_gravidade(sp.bodies[0], sp.bodies[1])
    forca2 = calcular_gravidade(sp.bodies[1], sp.bodies[0])
    sp.bodies[0].apply_force(forca1[0], forca1[1])
    sp.bodies[1].apply_force(forca2[0], forca2[1])
    print(forca1)
    print(forca2)
    sp.update(dt)
 
def draw():
    pyxel.cls(7)
    sp.draw()
 
pyxel.run(update, draw)
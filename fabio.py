import pyxel
import math

def update():
    global x, y, vx, vy, k, gamma, r, e

    if pyxel.btn(pyxel.KEY_SPACE):
        g = 0.0
    else:
        g = gamma

    Fx = -k * (x - pyxel.mouse_x) - g * vx
    Fy = -k * (y - pyxel.mouse_y) - g * vy

    ax = Fx / m
    ay = Fy / m

    x += vx * dt
    y += vy * dt

    vx += ax * dt
    vy += ay * dt

    if x < r: 
        vx = e * abs(vx)
    if x > pyxel.width - r:
        vx = -e * abs(vx)
    if y < r: 
        vy = e * abs(vy)
    if y > pyxel.height - r:
        vy = -e * abs(vy)


def draw():
    pyxel.cls(pyxel.COLOR_BLACK)
    pyxel.line(x,y, pyxel.mouse_x, pyxel.mouse_y, pyxel.COLOR_WHITE)
    pyxel.circ(x,y,4,pyxel.COLOR_WHITE)
    pyxel.rect(x,y,5,5,pyxel.COLOR_RED)

r = 4
k = 20
dt = 1/30
m = 10
x,y = (10,60)
vx, vy = (0, 100)
gamma = 5
e = 0.5

pyxel.init(180, 120, fps=30, caption = "Meu jogo!")
pyxel.mouse(True)
pyxel.run(update,draw)
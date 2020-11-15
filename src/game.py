import pyxel
from pymunk import Space
from .models import *
from .utils import *
from math import cos, sin

tile = lambda x: x * 8
gc = GameConfig()


def get_mouse_angle():
    origin = pyxel.player1.get_shoulder()
    shoulder_horizontal_line = Vec2d(origin[0] + gc.width, origin[1])
    mouse_pos = Vec2d(pyxel.mouse_x, pyxel.mouse_y)

    shoulder_horizontal_line = shoulder_horizontal_line - origin
    mouse_pos = mouse_pos - origin
    return (
        mouse_pos.get_angle_degrees_between(shoulder_horizontal_line),
        mouse_pos.get_angle_between(shoulder_horizontal_line),
    )


def update():
    pyxel.angle, pyxel.angle_rad = get_mouse_angle()
    player = pyxel.player1
    pyxel.force = edist((player.x, player.y), (pyxel.mouse_x, pyxel.mouse_y))
    if pyxel.force > 100:
        pyxel.force = 100

    if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON, period=1):
        player = pyxel.player1
        rock = Rock(*player.slingshot.get_nock_position())
        force = pyxel.force * 1.5
        impulse = (cos(pyxel.angle_rad) * force, sin(-pyxel.angle_rad) * force)

        rock.body.apply_impulse_at_world_point(impulse, player.slingshot.get_nock_position())
        pyxel.space.add(rock.body, rock.shape)
        pyxel.objects.append(rock)

    for rock in filter(lambda obj: isinstance(obj, Rock), pyxel.objects):
        rock.body.apply_force_at_world_point((0, 40), (0, 0))

    for o in pyxel.objects:
        o.update()

    # Delete deactivated objects
    deletable = list(filter(lambda o: not o.is_active, pyxel.objects))
    for o in deletable:
        pyxel.space.remove([o.body, o.shape])
        pyxel.objects.remove(o)

    pyxel.space.step(1 / GameConfig().fps)


def draw():
    pyxel.cls(pyxel.COLOR_WHITE)
    pyxel.bltm(0, 0, 0, 0, 0, tile(4), tile(3), pyxel.COLOR_WHITE)
    for o in pyxel.objects:
        o.draw(collisors=True)

    draw_hud()


def draw_hud():
    text = f'Angle = {"{:.1f}".format(pyxel.angle)} [mouse]'
    pyxel.text(pyxel.player1.x + 20, pyxel.player1.y + 15, text, pyxel.COLOR_BLACK)
    text = f'Force = {"{:.1f}".format(pyxel.force)} [mouse distance]'
    pyxel.text(pyxel.player1.x + 20, pyxel.player1.y + 22, text, pyxel.COLOR_BLACK)


def set_up():
    pyxel.space = Space()
    pyxel.player1 = Player(15, 0, Sprite.BLUE)

    pyxel.player2 = Player(195, 0, Sprite.RED)
    tree = PyxelObject(64 * 4 / 2 - Sprite.TREE.value.width / 2, 0, Sprite.TREE)
    
    pyxel.objects = [
        pyxel.player1,
        tree,
        pyxel.player2,
    ]
    for o in pyxel.objects:
        move_to_floor(o)
    tree.y += 3
    pyxel.force = 0

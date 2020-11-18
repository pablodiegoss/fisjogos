import pyxel
from pymunk import Space, Segment
from .models import *
from .utils import *
from math import cos, sin
from .cooldowns import TimedEvent, Cooldown

tile = lambda x: x * 8
gc = GameConfig()
from time import time


def get_mouse_angle():
    origin = pyxel.player1.slingshot.get_nock_origin()
    slingshot_horizontal_line = Vec2d(origin[0] + gc.width, origin[1])
    mouse_pos = get_mouse_pos()

    slingshot_horizontal_line = slingshot_horizontal_line - origin
    mouse_pos = mouse_pos - origin
    return (
        mouse_pos.get_angle_degrees_between(slingshot_horizontal_line),
        mouse_pos.get_angle_between(slingshot_horizontal_line),
    )


def update():
    pyxel.angle, pyxel.angle_rad = get_mouse_angle()
    player = pyxel.player1
    pyxel.force = edist(player.slingshot.get_nock_origin(), get_mouse_pos())
    if pyxel.force > 100:
        pyxel.force = 100

    if pyxel.btnp(pyxel.KEY_C, period=100):
        pyxel.collisors = not pyxel.collisors

    if pyxel.btnp(pyxel.KEY_J, period=2):
        pyxel.camera_offset += (+3, 0)
        if tuple(pyxel.camera_offset) > (399, 0):
            pyxel.camera_offset = Vec2d(399, 0)

    if pyxel.btnp(pyxel.KEY_K, period=2):
        pyxel.camera_offset += (-3, 0)
        if tuple(pyxel.camera_offset) < (-430, 0):
            pyxel.camera_offset = Vec2d(-430, 0)

    if pyxel.btnp(pyxel.KEY_U, period=2):
        pyxel.wind.direction += (1, 0)
        print(pyxel.wind.direction)
    if pyxel.btnp(pyxel.KEY_I, period=2):
        pyxel.wind.direction += (0, 1)
        print(pyxel.wind.direction)
    if pyxel.btnp(pyxel.KEY_N, period=2):
        pyxel.wind.direction += (-1, 0)
        print(pyxel.wind.direction)
    if pyxel.btnp(pyxel.KEY_M, period=2):
        pyxel.wind.direction += (0, -1)
        print(pyxel.wind.direction)

    if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON, period=100):
        player = pyxel.player1
        rock = Rock(*player.slingshot.get_nock_position())
        force = pyxel.force * 10
        impulse = (cos(pyxel.angle_rad) * force, sin(-pyxel.angle_rad) * force)

    if Cooldown.check(TimedEvent.WIND_CHANGE):
        pyxel.wind.change()
        Cooldown.activate(TimedEvent.WIND_CHANGE)
        pyxel.space.add(rock.body, *rock.shapes)
        pyxel.objects.append(rock)

    for rock in filter(lambda obj: isinstance(obj, Rock), pyxel.objects):
        rock.body.apply_force_at_world_point((0, 80), (0, 0))

    for o in pyxel.objects:
        o.update()

    # Delete deactivated objects
    deletable = list(filter(lambda o: not o.is_active, pyxel.objects))
    for o in deletable:
        pyxel.objects.remove(o)
        pyxel.space.remove([o.body, *o.shapes])

    pyxel.space.step(1 / GameConfig().fps)


def draw():
    pyxel.cls(pyxel.COLOR_WHITE)
    pyxel.bltm(
        *((-400, 0) + pyxel.camera_offset),
        0,
        0,
        0,
        tile(17),
        tile(3),
        pyxel.COLOR_WHITE,
    )

    if pyxel.collisors:
        pyxel.line(*pyxel.floor.a, *pyxel.floor.b, pyxel.COLOR_RED)

    for o in pyxel.objects:
        o.draw(pyxel.camera_offset, collisors=pyxel.collisors)

    draw_hud()


def draw_hud():
    text = f'Angle = {"{:.1f}".format(pyxel.angle)} [mouse]'
    pyxel.text(pyxel.player1.x + 20, pyxel.player1.y + 15, text, pyxel.COLOR_BLACK)
    text = f'Force = {"{:.1f}".format(pyxel.force)} [mouse distance]'
    pyxel.text(pyxel.player1.x + 20, pyxel.player1.y + 22, text, pyxel.COLOR_BLACK)

    pyxel.wind.draw(GameConfig().width / 2, 12)

    draw_hp_bar("P1", pyxel.player1.life, 1, 8)
    draw_hp_bar("P2", pyxel.player1.life, 195, 8)


def draw_hp_bar(name, player_life, x, y):
    pyxel.text(x, y, name, pyxel.COLOR_BLACK)
    pyxel.rect(x + 8, y - 3, 51, 11, pyxel.COLOR_BLACK)
    pyxel.rect(x + 9, y - 2, 49 * (player_life / 100), 9, pyxel.COLOR_GREEN)


def set_up():
    pyxel.space = Space()
    pyxel.space.damping = 0.75
    pyxel.space.gravity = (0, 60)
    pyxel.collisors = True

    floor = Body(body_type=Body.STATIC)
    floor_shape = Segment(
        floor, (-700, GameConfig().height - 1), (700, GameConfig().height - 1), 2
    )
    floor_shape.elasticity = 0.7
    pyxel.floor = floor_shape
    pyxel.space.add(floor, floor_shape)

    pyxel.camera_offset = Vec2d(0, 0)

    pyxel.wind = Wind()

    pyxel.player1 = Player(15, 0, Sprite.BLUE)
    pyxel.player2 = Player(195, 0, Sprite.RED)
    tree = Tree(64 * 4 / 2 - Sprite.TREE.value.width / 2, 0)
    pyxel.objects = [
        pyxel.player1,
        tree,
        pyxel.player2,
    ]
    for o in pyxel.objects:
        move_to_floor(o)
    tree.y += 3
    pyxel.force = 0
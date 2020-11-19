from src.hud import draw_background, draw_hud
from .inputs import check_game_inputs
import pyxel
from pymunk import Space, Segment
from .models import *
from .utils import *
from .cooldowns import TimedEvent, Cooldown


def update():
    pyxel.angle, pyxel.angle_rad = get_mouse_angle(pyxel.active_player)
    player = get_active_player()

    pyxel.force = edist(player.slingshot.get_nock_origin(), get_mouse_pos())
    if pyxel.force > 100:
        pyxel.force = 100

    check_game_inputs()
    if Cooldown.check(TimedEvent.WIND_CHANGE):
        pyxel.wind.change()
        Cooldown.activate(TimedEvent.WIND_CHANGE)

    for rock in filter(lambda obj: isinstance(obj, Rock), pyxel.objects):
        rock.body.apply_force_at_local_point(pyxel.wind.get_wind(), (0, 0))

    player.update()
    for o in pyxel.objects:
        o.update()

    # Delete deactivated objects
    deletable = list(filter(lambda o: not o.is_active, pyxel.objects))
    for o in deletable:
        pyxel.objects.remove(o)
        pyxel.space.remove([o.body, *o.shapes])

    pyxel.space.step(1 / GameConfig().fps)


def get_active_player():
    if pyxel.active_player.has_shot and (Cooldown.check(TimedEvent.SHOT_TIMEOUT)):
        pyxel.active_player.has_shot = False
        pyxel.active_rock = None
        pyxel.active_player = next(pyxel.player_changer)
        move_camera_to_player(pyxel.active_player)

    return pyxel.active_player

def get_camera_range():
    border_size = 0.2
    screen_width = GameConfig().width    
    camera_x_offset = pyxel.camera_offset.x
    return (screen_width*border_size - camera_x_offset,screen_width*(1-border_size) - camera_x_offset)

def in_camera_range(x):
    camera_range = get_camera_range()
    print(camera_range)
    if x < camera_range[0]:
        return False
    elif x > camera_range[1]:
        return False
    return True

def draw():
    draw_background()

    if pyxel.collisors:
        pyxel.line(*pyxel.floor.shape.a, *pyxel.floor.shape.b, pyxel.COLOR_RED)
    if pyxel.active_rock:
        x = pyxel.active_rock.body.position.x
        if not in_camera_range(x):
            camera_range = get_camera_range()
            difference = min(abs(x - camera_range[0]), abs(x- camera_range[1]))
            print(difference)
            if x > camera_range[1]:
                pyxel.camera_offset[0] -= difference
            if x < camera_range[0]:
                pyxel.camera_offset[0] += difference

    for o in [*pyxel.objects, *pyxel.players]:
        o.draw(pyxel.camera_offset, collisors=pyxel.collisors)

    draw_hud()


def set_up():
    pyxel.wind = Wind()
    pyxel.floor = Floor()
    pyxel.space = Space()
    pyxel.camera_offset = Vec2d(0, 0)
    pyxel.player_changer = player_generator()
    pyxel.force = 0
    pyxel.active_rock = None
    pyxel.space.damping = 0.75
    pyxel.space.gravity = (0, 60)
    pyxel.collisors = True

    set_up_collisions(pyxel.space)
    pyxel.space.add(pyxel.floor.body, pyxel.floor.shape)

    players_distance = 100
    p1 = Player(15 - players_distance, 161, Sprite.BLUE)
    p2 = Player(195 + players_distance, 161, Sprite.RED)
    pyxel.players = [p1, p2]
    pyxel.active_player = next(pyxel.player_changer)
    move_camera_to_player(pyxel.active_player)

    pyxel.objects = [Tree(64 * 4 / 2 - Sprite.TREE.value.width / 2, 128)]


def set_up_collisions(space):
    head_multiplier = 2
    body_multiplier = 1.5
    feet_multiplier = 1
    rock_damage = 10

    def collision_handler_generator(damage, multiplier):
        def collision_handler(arbiter, space, data):
            for shape in arbiter.shapes:
                if isinstance(shape.obj, Rock):
                    shape.obj.is_active = False
                if isinstance(shape.obj, Player):
                    shape.obj.life -= damage * multiplier

        return collision_handler

    rock_head_h = space.add_collision_handler(1, 2)
    rock_head_h.post_solve = collision_handler_generator(rock_damage, head_multiplier)

    rock_body_h = space.add_collision_handler(1, 3)
    rock_body_h.post_solve = collision_handler_generator(rock_damage, body_multiplier)

    rock_feet_h = space.add_collision_handler(1, 4)
    rock_feet_h.post_solve = collision_handler_generator(rock_damage, feet_multiplier)

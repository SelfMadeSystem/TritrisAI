import glfw

import tai_piece
import tai_renderer
import tai_utils
import tai_grid
import random

inp = tai_utils.Input()
p_inp = tai_utils.Input()  # prev
down_time = 0
move_time = 0
move_again = False


# noinspection PyUnusedLocal
def key_callback(w, key, scancode, action, mods):
    global move_again
    if key == glfw.KEY_DOWN:
        inp.key_down = action != glfw.RELEASE
        if action == glfw.PRESS:
            move_again = True
    elif key == glfw.KEY_UP:
        if action != glfw.RELEASE:
            move_piece(0, 1, 0)
    elif key == glfw.KEY_LEFT:
        inp.key_left = action != glfw.RELEASE
        if action == glfw.PRESS:
            move_again = True
    elif key == glfw.KEY_RIGHT:
        inp.key_right = action != glfw.RELEASE
        if action == glfw.PRESS:
            move_again = True
    if action == glfw.REPEAT:
        return
    if key == glfw.KEY_Z:
        inp.key_z = action != glfw.RELEASE
        if action == glfw.PRESS:
            move_again = True
    elif key == glfw.KEY_X:
        inp.key_x = action != glfw.RELEASE
        if action == glfw.PRESS:
            move_again = True


def render_update():
    # tai_renderer.set_color((255, 0, 0))
    # tai_renderer.begin(7)
    # tai_renderer.add_vec_pos_raw((-10, -10))
    # tai_renderer.add_vec_pos_raw((-10, 10))
    # tai_renderer.add_vec_pos_raw((10, 10))
    # tai_renderer.add_vec_pos_raw((10, -10))
    # tai_renderer.end()
    global move_again
    main_grid.render()
    current_piece.render()
    time = tai_utils.time_ms()
    if inp.key_down:
        global down_time
        if down_time + 50 < time:
            down_time = time
            update()
            timer.incr_time = 0
    else:
        global move_time
        timer.update()

        x = 0
        r = 0
        st = False
        move = move_time + 100 < time or move_again
        if inp.key_left and move:
            st = True
            x -= 1
        if inp.key_right and move:
            st = True
            x += 1
        if st:
            move_time = time
        if inp.key_x and (not p_inp.key_x or move_again):
            if inp.key_z and (not p_inp.key_z or move_again):
                r = 2
            else:
                r = 1
        elif inp.key_z and (not p_inp.key_z or move_again):
            r = -1
        if x != 0 or r != 0:
            move_piece(x, 0, r)
    p_inp.set(inp)
    move_again = False


def update():
    x = 0
    r = 0
    if inp.key_left:
        x -= 1
    if inp.key_right:
        x += 1
    if inp.key_x:
        if inp.key_z:
            r = 2
        else:
            r = 1
    elif inp.key_z:
        r = -1
    inp.key_x = False
    inp.key_z = False
    move_piece(x, -1, r)


def reset_input(result: tai_utils.MoveResult):
    if result.x:
        inp.key_left = False
        inp.key_right = False
    if result.r:
        inp.key_x = False
        inp.key_z = False


def place_piece():
    global ninja_count
    current_piece.place()
    if ninja_count <= 1:
        main_grid.check_lines()
    ninja_count -= 1
    new_piece()


def new_piece():
    global current_piece, bag, ninja_count
    if ninja_count > 0:
        current_piece = tai_piece.new_piece(0)
        return
    if len(bag) == 0:
        bag = list(range(0, 7))
    rand = random.randint(0, len(bag) - 1)
    i = bag.pop(rand)
    current_piece = tai_piece.new_piece(i)
    if i == 0:
        ninja_count = 3


def move_piece(x: int, y: int, r: int):
    if y < 0:
        timer.incr_time = 0
    result = current_piece.move(x, y, r)
    if result.place:
        place_piece()
    reset_input(result)


def set_speed():
    global fall_speed
    lvl = min(29, max(0, level))
    while True:
        if lvl in level_speeds:
            fall_speed = level_speeds[lvl]
            timer.delay = fall_speed
            return
        lvl -= 1
        if lvl < 0:
            print("Couldn't get level speed!!!")
            return


# noinspection PyTypeChecker
renderer_obj = None  # type: tai_renderer.Renderer
last_draw = tai_utils.time_ms()
timer = tai_utils.Timer(1000, update)
main_grid = tai_grid.Grid((8, 16))
level_speeds = {
    0: 48,
    1: 43,  # From https://tetris.wiki/Tetris_(NES,_Nintendo)
    2: 38,
    3: 33,
    4: 28,
    5: 23,
    6: 18,
    7: 13,
    8: 8,
    9: 6,
    10: 5,  # Level 10-12
    13: 4,  # 13 - 15
    16: 3,  # 16 - 18
    19: 2,  # 19 - 28
    29: 1,  # 29+
}

for l in level_speeds:
    level_speeds[l] = level_speeds[l] / 60 * 1000

level = 0
fall_speed = 0

bag = list(range(0, 7))
# noinspection PyTypeChecker
current_piece = None  # type: tai_piece.Piece
ninja_count = 0

colors = ((255, 0, 0),
          (0, 255, 0),
          (255, 255, 0),
          (255, 0, 255),
          (0, 255, 255),
          (250, 100, 25),
          (255, 255, 255))
set_speed()


def start():
    global renderer_obj
    m = 2 / max(main_grid.w, main_grid.h)
    tai_renderer.render_scale = (m, m)
    tai_renderer.render_offset = (-1, -1)
    new_piece()
    renderer_obj = tai_renderer.Renderer(500, 500, "Tritris", key_callback, render_update)
    renderer_obj.start_render_loop()

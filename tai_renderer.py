from OpenGL.GL import *

import glfw
import freetype
from typing import Tuple

import tai_game_manager


def on_resize(w, x, y):
    a = x / tai_game_manager.main_grid.w
    b = y / tai_game_manager.main_grid.h
    c = tai_game_manager.main_grid.h / tai_game_manager.main_grid.w
    d = tai_game_manager.main_grid.w / tai_game_manager.main_grid.h
    m = int((y * (d if c < d else 1)) if a > b else (x * (c if c > d else 1)))
    glViewport(0, 0, m, m)


class Renderer:
    def __init__(self, window_width: int, window_height: int, window_title: str, key_callback: (),
                 update_method: ()):
        if not glfw.init():
            OSError("GLFW Not Initialised")
        glfw.window_hint(glfw.STENCIL_BITS, 8)
        glfw.window_hint(glfw.SAMPLES, 8)
        glfw.window_hint(glfw.ALPHA_BITS, 8)
        self.window = glfw.create_window(window_width, window_height, window_title, None, None)
        self.window_width = window_width
        self.window_height = window_height
        self.window_title = window_title
        glfw.set_window_size_callback(self.window, on_resize)
        if self.window == 0:
            OSError("Could not create window")
        glfw.set_key_callback(self.window, key_callback)

        # glfw.set_window_attrib(self.window, glfw.RESIZABLE, 0)
        glfw.set_window_attrib(self.window, glfw.TRANSPARENT_FRAMEBUFFER, 1)

        glfw.make_context_current(self.window)

        glfw.show_window(self.window)
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glfw.window_hint(glfw.SAMPLES, 4)

        self.update_method = update_method

    def start_render_loop(self):
        while not glfw.window_should_close(self.window):
            self.pre_update()
            self.update()
            self.post_update()
            size = glfw.get_window_size(self.window)
            self.window_width = size[0]
            self.window_height = size[1]
        glfw.terminate()

    def pre_update(self):
        glClearColor(0.0, 0.0, 0.0, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glClearColor(0.0, 0.0, 0.0, 0)

    def update(self):
        self.update_method()

    def post_update(self):
        glfw.swap_buffers(self.window)
        glfw.poll_events()

    def get_size(self) -> Tuple[int, int]:
        return glfw.get_window_size(self.window)

    def get_pos(self) -> Tuple[int, int]:
        return glfw.get_window_pos(self.window)


render_offset = (0., 0.)
render_scale = (1., 1.)


def draw_rect(pos: Tuple[float, float], size: Tuple[float, float]):
    begin(GL_QUADS)
    add_vec_pos((pos[0], pos[1]))
    add_vec_pos((pos[0] + size[0], pos[1]))
    add_vec_pos((pos[0] + size[0], pos[1] + size[1]))
    add_vec_pos((pos[0], pos[1] + size[1]))
    add_vec_pos((pos[0], pos[1]))
    end()


def draw_triangle(pos0: Tuple[float, float], pos1: Tuple[float, float], pos2: Tuple[float, float]):
    begin(GL_TRIANGLES)
    add_vec_pos(pos0)
    add_vec_pos(pos1)
    add_vec_pos(pos2)
    end()


def set_color(color: Tuple[int, int, int]):
    glColor3d(color[0] / 255, color[1] / 255, color[2] / 255)


def add_vec_pos(pos: Tuple[float, float]):
    add_vec_pos_raw((pos[0] * render_scale[0] + render_offset[0], pos[1] * render_scale[1] + render_offset[1]))


def add_vec_pos_raw(pos: Tuple[float, float]):
    glVertex2d(pos[0], pos[1])


def begin(mode: int):
    glBegin(mode)


def end():
    glEnd()

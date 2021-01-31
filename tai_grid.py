from typing import Tuple, List

import tai_game_manager
import tai_renderer


class Grid:
    def __init__(self, size: Tuple[int, int]):
        self.w = size[0]
        self.h = size[1]
        self.matrix = []  # type: List[List[Cell]]
        self.clear_lines()

    def clear_lines(self):
        self.matrix = [[Cell()]] * self.h
        i = 0
        while i < self.h:
            self.matrix[i] = new_line(self.w)
            i += 1

    def remove_line(self, row: int):
        self.matrix.pop(row)
        self.matrix.append(new_line(self.w))

    def check_lines(self):
        i = self.h - 1
        while i >= 0:
            j = 0
            full = True
            while j < self.w:
                full &= self.matrix[i][j].is_full()
                j += 1
            if full:
                self.remove_line(i)
            i -= 1

    def render(self):
        x = 0
        while x < self.w:
            y = 0
            while y < self.h:
                self.matrix[y][x].render(x, y)
                y += 1
            x += 1


class Cell:
    def __init__(self, triangles=None, draw_bg=True):
        if triangles is None:
            triangles = [[-1, -1], [-1, -1]]
        self.tris = triangles
        self.draw_bg = draw_bg
        self.bg_color = (50, 50, 50)

    def rotate_left(self):
        return Cell([
            [self.tris[0][1], self.tris[1][1]],
            [self.tris[0][0], self.tris[1][0]],
        ], self.draw_bg)

    def rotate_right(self):
        return Cell([
            [self.tris[1][0], self.tris[0][0]],
            [self.tris[1][1], self.tris[0][1]],
        ], self.draw_bg)

    def is_full(self):
        return (self.tris[0][0] != -1 and self.tris[1][1] != -1) or (self.tris[1][0] != -1 and self.tris[0][1] != -1)

    def is_empty(self):
        return self.tris[0][0] == -1 and self.tris[1][1] == -1 and self.tris[1][0] == -1 and self.tris[0][1] == -1

    def add(self, cell):
        """
        :type cell: Cell
        """
        x = 0
        while x < len(cell.tris):
            y = 0
            while y < len(cell.tris[x]):
                if cell.tris[x][y] >= 0:
                    self.tris[x][y] = cell.tris[x][y]
                y += 1
            x += 1

    def collides(self, cell) -> bool:
        x = 0
        while x < len(cell.tris):
            y = 0
            while y < len(cell.tris[x]):
                if self.tris[x][y] == -1:
                    y += 1
                    continue
                if (
                        cell.tris[x][y] != -1 or
                        cell.tris[(x + 1) % 2][y] != -1 or
                        cell.tris[x][(y + 1) % 2] != -1
                ):
                    return True
                y += 1
            x += 1
        return False

    def render(self, x, y):
        if self.draw_bg:
            tai_renderer.set_color(self.bg_color)
            tai_renderer.draw_rect((x, y), (0.9, 0.9))
        self._render(x, y, 0, 0)
        self._render(x, y, 1, 0)
        self._render(x, y, 0, 1)
        self._render(x, y, 1, 1)

    def _render(self, x, y, a, b):
        c = 0 if a != 0 else 0.9
        d = 0 if b != 0 else 0.9
        t = self.tris[a][b]
        if t >= 0:
            a *= 0.9
            b *= 0.9
            tai_renderer.set_color(tai_game_manager.colors[t])
            tai_renderer.draw_triangle((x + a, y + b), (x + c, y + b), (x + c, y + d))

    def __str__(self):
        return str(self.tris)

    def __repr__(self):
        return "Cell({0})".format(self.__str__())


def new_line(w: int) -> List[Cell]:
    lis = [Cell()] * w
    i = 0
    while i < w:
        lis[i] = Cell()
        i += 1
    return lis

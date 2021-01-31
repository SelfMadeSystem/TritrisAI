from typing import List, Tuple

import tai_game_manager
import tai_grid
import json

import tai_renderer
import tai_utils


class Piece:
    def __init__(self, part):
        self.json = part
        self.grid = []  # type: List[List[tai_grid.Cell]]
        pieces = part["pieces"]
        row = 0
        while row < len(pieces):
            self.grid.append([])
            col = 0
            while col < len(pieces[0]):
                self.grid[row].append(tai_grid.Cell(pieces[row][col], False))
                col += 1
            row += 1
        self.rotation = 0
        self.rotations = part["rotationOffset"] if "rotationOffset" in part is not None else [[0, 0]]
        self.pos = tai_utils.Pos(int(tai_game_manager.main_grid.w / 2),
                                 int(tai_game_manager.main_grid.h) - len(pieces[0]))

    def move(self, x, y, r) -> tai_utils.MoveResult:
        p = False  # Place
        if self.pos.y + y < 0:
            y = 0
            p = True
        if self.is_viable(tai_utils.Pos(x, y), r):
            self.pos.add(x, y)
            return tai_utils.MoveResult(p, x, r)
        if self.is_viable(tai_utils.Pos(x, y), 0):
            self.pos.add(x, y)
            return tai_utils.MoveResult(p, x, 0)
        if self.is_viable(tai_utils.Pos(0, y), r):
            self.pos.add(0, y)
            return tai_utils.MoveResult(p, 0, r)
        if self.is_viable(tai_utils.Pos(0, y), 0):
            self.pos.add(0, y)
            return tai_utils.MoveResult(p, 0, 0)
        if self.is_viable(tai_utils.Pos(x, 0), r):
            self.pos.add(x, 0)
            return tai_utils.MoveResult(y < 0, x, r)
        if self.is_viable(tai_utils.Pos(x, 0), 0):
            self.pos.add(x, 0)
            return tai_utils.MoveResult(y < 0, x, 0)
        if self.is_viable(tai_utils.Pos(0, 0), r):
            return tai_utils.MoveResult(y < 0, 0, r)
        return tai_utils.MoveResult(y < 0, 0, 0)

    def is_viable(self, add=tai_utils.Pos(0, 0), rotate=0) -> bool:
        grid = tai_game_manager.main_grid

        self.rotate(rotate)
        pos = self.pos.copy().add(add)

        if pos.y < 0:
            return self.unrotate(rotate)
        elif pos.y + len(self.grid[0]) > len(grid.matrix):
            return self.unrotate(rotate)
        if pos.x - len(self.grid) < -1:
            return self.unrotate(rotate)
        elif pos.x >= len(grid.matrix[0]):
            return self.unrotate(rotate)

        row = 0
        while row < len(self.grid):
            col = 0
            while col < len(self.grid[0]):
                if grid.matrix[pos.y + col][pos.x - row].collides(self.grid[row][col]):
                    return self.unrotate(rotate)
                col += 1
            row += 1
        return True

    def unrotate(self, rotate) -> bool:
        if rotate == 2:
            self.rotate_180()
        elif rotate == 1:
            self.rotate_right()
        elif rotate == -1:
            self.rotate_left()
        return False

    def rotate(self, rotate) -> bool:
        if rotate == 2:
            self.rotate_180()
        elif rotate == 1:
            self.rotate_left()
        elif rotate == -1:
            self.rotate_right()
        return False

    def place(self):
        row = 0
        while row < len(self.grid):
            col = 0
            while col < len(self.grid[0]):
                tai_game_manager.main_grid.matrix[self.pos.y + col][self.pos.x - row].add(self.grid[row][col])
                col += 1
            row += 1

    def rotate_180(self):
        self.rotate_left()  # Lazy way
        self.rotate_left()

    def rotate_left(self):
        new_grid = []
        new_row = 0
        while new_row < len(self.grid[0]):
            new_grid.append([])
            new_col = 0
            while new_col < len(self.grid):
                old_row = new_col
                old_col = len(self.grid[0]) - 1 - new_row
                new_grid[new_row].append(self.grid[old_row][old_col].rotate_left())
                new_col += 1
            new_row += 1

        self.grid = new_grid

        # Calculates a new position so the piece stays centered around the same piece
        self.pos.add(self.rotations[self.rotation][0], self.rotations[self.rotation][1])
        self.rotation = (self.rotation + 1) % len(self.rotations)

    def rotate_right(self):
        new_grid = []
        new_row = 0
        while new_row < len(self.grid[0]):
            new_grid.append([])
            new_col = 0
            while new_col < len(self.grid):
                old_row = len(self.grid) - 1 - new_col
                old_col = new_row
                new_grid[new_row].append(self.grid[old_row][old_col].rotate_right())
                new_col += 1
            new_row += 1

        self.grid = new_grid

        # Calculates a new position so the piece stays centered around the same piece
        self.rotation = (self.rotation - 1 + len(self.rotations)) % len(self.rotations)
        self.pos.sub(self.rotations[self.rotation][0], self.rotations[self.rotation][1])

    def render(self):
        x = 0
        while x < len(self.grid):
            y = 0
            while y < len(self.grid[x]):
                self.grid[x][y].render(self.pos.x - x, self.pos.y + y)
                y += 1
            x += 1
        tai_renderer.set_color((255, 0, 0))
        tai_renderer.draw_rect(self.pos.to_tuple(), (0.1, 0.9))
        tai_renderer.draw_rect(self.pos.to_tuple(), (0.9, 0.1))
        tai_renderer.draw_rect(self.pos.copy().add(0.8, 0).to_tuple(), (0.1, 0.9))
        tai_renderer.draw_rect(self.pos.copy().add(0, 0.8).to_tuple(), (0.9, 0.1))

    def __str__(self) -> str:
        return "{0}".format(self.grid)


with open("pieces.json") as f:
    loaded_json = json.load(f)  # type: dict


def new_piece(i: int) -> Piece:
    return Piece(loaded_json["pieces"][i])

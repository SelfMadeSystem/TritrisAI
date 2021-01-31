import time

from typing import Tuple


def time_ms() -> int:
    return int(time.time_ns() / 1000000)


class Timer:
    def __init__(self, delay: int, method: ()):
        self.delay = delay
        self.method = method
        self.last_update = time_ms()
        self.last_time = time_ms()
        self.incr_time = 0

    def update(self):
        current_time = time_ms()
        self.incr_time += max(0, int(current_time - self.last_time))
        while self.incr_time >= self.delay:
            self.incr_time -= self.delay
            self.method()
            self.last_update = current_time
        self.last_time = current_time


class Pos:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def add(self, x, y=None):
        if y is None:
            if x is None:
                return self
            if isinstance(x, Pos):
                self.x += x.x
                self.y += x.y
            else:
                self.x += x
                self.y += x
            return self
        self.x += x
        self.y += y
        return self

    def sub(self, x, y):
        self.x -= x
        self.y -= y
        return self

    def copy(self):
        return Pos(self.x, self.y)

    def to_tuple(self) -> Tuple[float, float]:
        return self.x, self.y


class Input:
    def __init__(self):
        self.key_down = False
        self.key_left = False
        self.key_right = False
        self.key_x = False
        self.key_z = False

    def set(self, other):
        self.key_down = other.key_down
        self.key_left = other.key_left
        self.key_right = other.key_right
        self.key_x = other.key_x
        self.key_z = other.key_z


class MoveResult:  # idk what to call it xd
    def __init__(self, place: bool, x: int, r: int):
        self.place = place
        self.x = x != 0
        self.r = r != 0

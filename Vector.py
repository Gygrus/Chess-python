from enum import Enum


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def black_or_white_cell(self):
        return (self.x + self.y) % 2

    def up(self):
        return Vector(self.x - 1, self.y)

    def down(self):
        return Vector(self.x + 1, self.y)

    def right(self):
        return Vector(self.x, self.y + 1)

    def left(self):
        return Vector(self.x, self.y - 1)

    def in_chessboard(self):
        return 0 <= self.x < 8 and 0 <= self.y < 8

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def equal(self, other):
        return self.x == other.x and self.y == other.y

    def one_line(self, other):
        return self.y == other.y

    def one_row(self, other):
        return self.x == other.x

    def one_diagonal(self, other):
        return abs(self.x - other.x) == abs(self.y - other.y)

    def move_line_up(self, other):
        return self.x > other.x

    def move_line_down(self, other):
        return self.x < other.x

    def move_row_right(self, other):
        return self.y < other.y

    def move_row_left(self, other):
        return self.y > other.y

    def move_right_up(self, other):
        return self.y < other.y and self.x > other.x

    def move_left_up(self, other):
        return self.y > other.y and self.x > other.x

    def move_right_down(self, other):
        return self.y < other.y and self.x < other.x

    def move_left_down(self, other):
        return self.y > other.y and self.x < other.x

    def is_second_row(self):
        return self.x == 6

    def is_seventh_row(self):
        return self.x == 1





class Direction(Enum):
    UP = Vector(-1, 0),
    DOWN = Vector(1, 0),
    RIGHT = Vector(0, 1),
    LEFT = Vector(0, -1),
    UP_RIGHT = Vector(-1, 1),
    UP_LEFT = Vector(-1, -1),
    DOWN_RIGHT = Vector(1, 1),
    DOWN_LEFT = Vector(1, -1)

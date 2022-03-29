class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def black_or_white_cell(self):
        return (self.x + self.y) % 2

    def up(self):
        return Vector(self.x, self.y - 1)

    def down(self):
        return Vector(self.x, self.y + 1)

    def right(self):
        return Vector(self.x + 1, self.y)

    def left(self):
        return Vector(self.x - 1, self.y)

    def in_chessboard(self):
        return 0 <= self.x < 8 and 0 <= self.y < 8

    def add(self, vector):
        return Vector(self.x + vector.x, self.y + vector.y)

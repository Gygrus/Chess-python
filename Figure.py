from Chessboard import *
from Vector import Direction


def column(x):
    return {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,}[x]


class Element:
    def __init__(self, position):
        self.color = 'black' if position.black_or_white_cell() else 'white'
        self.image = '\u25FB' if position.black_or_white_cell() else '\u25FC'
        self.position = position

    def print_in_console(self):
        return self.image


class Figure(Element):
    def __init__(self, position):
        Element.__init__(self, position)
        self.position = position
        self.alive = 'yes'

    def one_line(self, destination):
        return self.position.one_line(destination)

    def one_row(self, destination):
        return self.position.one_row(destination)

    def one_diagonal(self, destination):
        return self.position.one_diagonal(destination)

    def direction(self, destination):
        if self.one_line(destination):
            return Direction.UP if self.position.move_line_up(destination) else Direction.DOWN
        if self.one_row(destination):
            return Direction.RIGHT if self.position.move_row_right(destination) else Direction.LEFT
        if self.one_diagonal(destination):
            if self.position.move_line_up(destination):
                return Direction.UP_RIGHT if self.position.move_row_right(destination) else Direction.UP_LEFT
            else:
                return Direction.DOWN_RIGHT if self.position.move_row_right(destination) else Direction.DOWN_LEFT


class Pawn(Figure):
    def __init__(self, color, position):
        Figure.__init__(self, position)
        self.color = color
        self.position = position
        self.image = '\u265F' if self.color == 'white' else '\u2659'

    def is_second_row(self):
        return self.position.is_second_row() if self.color == 'white' else self.position.is_seventh_row()

    def calculate_possible_moves(self, board):
        pass

    def promotion(self):
        pass


class Knight(Figure):
    def __init__(self, color, position):
        Figure.__init__(self, position)
        self.color = color
        self.position = position
        self.image = '\u265E' if self.color == 'white' else '\u2658'


class Bishop(Figure):
    def __init__(self, color, position):
        Figure.__init__(self, position)
        self.color = color
        self.position = position
        self.image = '\u265D' if self.color == 'white' else '\u2657'

    def correct_move(self, destination):
        return self.one_diagonal(destination)


class Rook(Figure):
    def __init__(self, color, position):
        Figure.__init__(self, position)
        self.color = color
        self.position = position
        self.image = '\u265C' if self.color == 'white' else '\u2656'

    def correct_move(self, destination):
        return self.one_row(destination) or self.one_line(destination)


class Queen(Figure):
    def __init__(self, color, position):
        Figure.__init__(self, position)
        self.color = color
        self.position = position
        self.image = '\u265B' if self.color == 'white' else '\u2655'

    def correct_move(self, destination):
        return self.one_row(destination) or self.one_line(destination) or self.one_diagonal(destination)


class King(Figure):
    def __init__(self, color, position):
        Figure.__init__(self, position)
        self.color = color
        self.position = position
        self.right_to_castling = 'yes'
        self.image = '\u265A' if self.color == 'white' else '\u2654'

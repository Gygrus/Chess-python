from Chessboard import *


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


class Pawn(Figure):
    def __init__(self, color, position):
        Figure.__init__(self, position)
        self.color = color
        self.position = position
        self.image = '\u265F' if self.color == 'white' else '\u2659'

    def calculate_possible_moves(self, board):
        pass
    #     MOVES = []
    #     if board.get_przelot is not None and self.color == 'white' and self.position.y == 3 and self.position.x - column(board.get_przelot) == 1:
    #         MOVES.append((self.position.x + 1, self.position.y - 1))
    #     if board.get_przelot is not None and self.color == 'white' and self.position.y == 3 and self.position.x - column(board.get_przelot) == -1:
    #         MOVES.append((self.position.x - 1, self.position.y - 1))
    #     if board.get_przelot is not None and self.color == 'black' and self.position.y == 4 and self.position.x - column(board.get_przelot) == 1:
    #         MOVES.append((self.position.x + 1, self.position.y + 1))
    #     if board.get_przelot is not None and self.color == 'black' and self.position.y == 4 and self.position.x - column(board.get_przelot) == -1:
    #         MOVES.append((self.position.x - 1, self.position.y + 1))
    #
    #     if isinstance(board.object_at(self.position.up), Figure):
    #         MOVES.append(self.position.up)


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


class Rook(Figure):
    def __init__(self, color, position):
        Figure.__init__(self, position)
        self.color = color
        self.position = position
        self.image = '\u265C' if self.color == 'white' else '\u2656'


class Queen(Figure):
    def __init__(self, color, position):
        Figure.__init__(self, position)
        self.color = color
        self.position = position
        self.image = '\u265B' if self.color == 'white' else '\u2655'


class King(Figure):
    def __init__(self, color, position):
        Figure.__init__(self, position)
        self.color = color
        self.position = position
        self.right_to_castling = 'yes'
        self.image = '\u265A' if self.color == 'white' else '\u2654'

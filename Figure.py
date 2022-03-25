class Figure():
    def __init__(self, board, color, piece, position):
        self.board = board
        self.piece = piece
        self.color = color
        self.position = position
        self.alive = 'yes'

    def move(self):
        pass


class Pawn(Figure):
    def __init__(self, second_row, board, color, piece, position):
        self.second_row = 'yes'
        Figure.__init__(self, board, color, piece, position)

    def promotion(self):
        pass


class Knight(Figure):
    def __init__(self, board, color, piece, position):
        Figure.__init__(self, board, color, piece, position)


class Bishop(Figure):
    def __init__(self, board, color, piece, position):
        Figure.__init__(self, board, color, piece, position)


class Rook(Figure):
    def __init__(self, board, color, piece, position):
        Figure.__init__(self, board, color, piece, position)


class Queen(Figure):
    def __init__(self, board, color, piece, position):
        Figure.__init__(self, board, color, piece, position)


class King(Figure):
    def __init__(self, right_to_castling, board, color, piece, position):
        self.right_to_castling = 'yes'
        Figure.__init__(self, board, color, piece, position)

from backend.Figure import Figure, Element, Pawn, Rook, King, Knight, Bishop, Queen
from backend.Vector import Vector


class Chessboard:
    def __init__(self):
        self.board = [[Element(Vector(i, j)) for i in range(8)] for j in range(8)]
        self.white_king_position = Vector(7, 4)
        self.black_king_position = Vector(0, 4)
        self.knight_moves = [Vector(1, 2), Vector(1, -2), Vector(2, 1), Vector(2, -1), Vector(-1, 2), Vector(-1, -2),
                             Vector(-2, -1), Vector(-2, 1)]
        self.king_moves = [Vector(0, -1), Vector(0, 1), Vector(-1, 0), Vector(1, 0), Vector(-1, 1), Vector(1, -1),
                           Vector(1, 1), Vector(-1, -1)]

        for i in range(8):
            self.board[6][i] = Pawn('white', Vector(6, i))
            self.board[1][i] = Pawn('black', Vector(1, i))

        self.board[7][0] = Rook('white', Vector(7, 0))
        self.board[7][1] = Knight('white', Vector(7, 1))
        self.board[7][2] = Bishop('white', Vector(7, 2))
        self.board[7][3] = Queen('white', Vector(7, 3))
        self.board[7][4] = King('white', Vector(7, 4))
        self.board[7][5] = Bishop('white', Vector(7, 5))
        self.board[7][6] = Knight('white', Vector(7, 6))
        self.board[7][7] = Rook('white', Vector(7, 7))

        self.board[0][0] = Rook('black', Vector(0, 0))
        self.board[0][1] = Knight('black', Vector(0, 1))
        self.board[0][2] = Bishop('black', Vector(0, 2))
        self.board[0][3] = Queen('black', Vector(0, 3))
        self.board[0][4] = King('black', Vector(0, 4))
        self.board[0][5] = Bishop('black', Vector(0, 5))
        self.board[0][6] = Knight('black', Vector(0, 6))
        self.board[0][7] = Rook('black', Vector(0, 7))

    def print_board(self):
        print('   a   b   c  d   e   f  g   h')
        for i in range(8):
            print((-i + 8) % 9, end='| ')
            for j in range(8):
                print(self.board[i][j].print_in_console(), end='  ')
            print()
        print()
        print()

    def object_at(self, position):
        return self.board[position.x][position.y]

    def is_figure(self, position):
        return isinstance(self.board[position.x][position.y], Figure)

    def color_at(self, position):
        return self.board[position.x][position.y].color

    def move_object(self, old_position, element):
        killed, position = False, element.position
        if isinstance(element, Pawn):
            if not self.is_figure(position) and old_position.y != element.position.y:
                if element.color == 'white':
                    self.board[position.x + 1][position.y] = Element(Vector(position.x + 1, position.y))
                else:
                    self.board[position.x - 1][position.y] = Element(Vector(position.x - 1, position.y))
                killed = True

        if isinstance(self.object_at(position), Figure):
            killed = True

        if isinstance(element, King):
            if element.color == 'white':
                self.white_king_position = position
            else:
                self.black_king_position = position

        self.board[position.x][position.y] = element
        self.board[old_position.x][old_position.y] = Element(old_position)

        if isinstance(element, (King, Rook)):
            element.right_to_castling = 'no'

        return killed

    def for_en_passant(self, element, position):
        destination = element.position
        if abs(destination.x - position.x) == 2 and isinstance(element, Pawn):
            if destination.right().in_chessboard():
                figure = self.object_at(destination.right())
                if isinstance(figure, Pawn) and figure.color != element.color:
                    figure.en_passant = destination

            if destination.left().in_chessboard():
                figure = self.object_at(destination.left())
                if isinstance(figure, Pawn) and figure.color != element.color:
                    figure.en_passant = destination

        for i in range(8):
            for j in range(8):
                figure = self.object_at(Vector(i, j))
                if isinstance(figure, Pawn):
                    if figure.color == element.color:
                        figure.en_passant = Vector(20, 20)

    def is_possible_move(self, element, destination):
        if not destination.in_chessboard() or element.position.equal(destination):
            return False

        figure = self.object_at(destination)
        if isinstance(figure, Figure) and figure.color == element.color:
            return False

        match element:
            case Knight():
                for move in self.knight_moves:
                    if element.position.add(move).equal(destination):
                        return True
            case King():
                for move in self.king_moves:
                    if element.position.add(move).equal(destination):
                        return True
            case Pawn():
                if element.color == 'white':
                    if element.position.up().equal(destination) and not isinstance(figure, Figure):
                        return True
                    if element.position.up().right().equal(destination) and isinstance(figure, Figure):
                        return True
                    if element.position.up().left().equal(destination) and isinstance(figure, Figure):
                        return True
                    if element.is_starting_row() and destination.equal(element.position.up().up()):
                        if not self.is_figure(element.position.up()) and not isinstance(figure, Figure):
                            return True
                    if element.en_passant.up().equal(destination):
                        return True
                else:
                    if element.position.down().equal(destination) and not isinstance(figure, Figure):
                        return True
                    if element.position.down().right().equal(destination) and isinstance(figure, Figure):
                        return True
                    if element.position.down().left().equal(destination) and isinstance(figure, Figure):
                        return True
                    if element.is_starting_row() and destination.equal(element.position.down().down()):
                        if not self.is_figure(element.position.down()) and not isinstance(figure, Figure):
                            return True
                    if element.en_passant.down().equal(destination):
                        return True
            case Rook() | Bishop() | Queen():
                if not element.correct_move(destination):
                    return False

                position = element.position
                iterator = element.direction(destination)

                while not position.equal(destination):
                    position = position.add(iterator)
                    if position.equal(destination):
                        return True
                    else:
                        if self.is_figure(position):
                            return False
        return False

    def is_check(self, position, color):
        for move in self.knight_moves:
            if not position.add(move).in_chessboard():
                continue
            element = self.object_at(position.add(move))
            if isinstance(element, Knight) and element.color == color:
                return True

        for move in self.king_moves:
            if not position.add(move).in_chessboard():
                continue
            element = self.object_at(position.add(move))
            if isinstance(element, King) and element.color == color:
                return True

        if color == 'white':
            if position.down().right().in_chessboard():
                element = self.object_at(position.down().right())
                if isinstance(element, Pawn) and element.color == color:
                    return True
            if position.down().left().in_chessboard():
                element = self.object_at(position.down().left())
                if isinstance(element, Pawn) and element.color == color:
                    return True
        else:
            if position.up().right().in_chessboard():
                element = self.object_at(position.up().right())
                if isinstance(element, Pawn) and element.color == color:
                    return True
            if position.up().left().in_chessboard():
                element = self.object_at(position.up().left())
                if isinstance(element, Pawn) and element.color == color:
                    return True

        for i in range(8):
            for j in range(8):
                element = self.object_at(Vector(i, j))
                if isinstance(element, (Rook, Bishop, Queen)) and element.color == color:
                    if not element.correct_move(position):
                        continue

                    attacker_position = element.position
                    iterator = element.direction(position)

                    while not attacker_position.equal(position):
                        attacker_position = attacker_position.add(iterator)
                        if attacker_position.equal(position):
                            return True
                        else:
                            if self.is_figure(attacker_position):
                                break

        return False

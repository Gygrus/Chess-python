from Figure import *
from Figure import Element, Figure
from Vector import Vector


class Chessboard:
    def __init__(self):
        self.board = [[Element(Vector(i, j)) for i in range(8)] for j in range(8)]
        self.take_en_passant = None
        self.knight_moves = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, -1), (-2, 1)]
        self.king_moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]

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

    def move_object(self, old_position, element):
        self.board[element.position.x][element.position.y] = element
        self.board[old_position.x][old_position.y] = Element(old_position)

    def is_check(self, color_of_king):
        check = 0
        position_of_king = Vector(-1, -1)
        opponent_color = 'white' if color_of_king == 'black' else 'black'
        for rows in self.board:
            for piece in rows:
                if isinstance(piece, King) and piece.color == color_of_king:
                    position_of_king = piece.position

        ## skoczki załatwione
        for move in self.knight_moves:
            element = self.object_at(position_of_king.add(Vector(move[0], move[1])))
            if element.position.in_chessboard() and element.color == opponent_color:
                if isinstance(element, Knight):
                    check = 1
                    return 1

        ## król przeciwny załatwiony
        for move in self.king_moves:
            element = self.object_at(position_of_king.add(Vector(move[0], move[1])))
            if element.position.in_chessboard() and element.color == opponent_color:
                if isinstance(element, King):
                    check = 1
                    return 1

        x = position_of_king.x
        y = position_of_king.y


        ## sprawdzamy pionki
        if color_of_king == 'white':
            element = self.object_at(position_of_king.add(Vector(-1, -1)))
            if element.position.in_chessboard() and element.color == opponent_color:
                if isinstance(element, Pawn):
                    check = 1
                    return 1

            element = self.object_at(position_of_king.add(Vector(-1, 1)))
            if element.position.in_chessboard() and element.color == opponent_color:
                if isinstance(element, Pawn):
                    check = 1
                    return 1
        elif color_of_king == 'black':
            element = self.object_at(position_of_king.add(Vector(1, 1)))
            if element.position.in_chessboard() and element.color == opponent_color:
                if isinstance(element, Pawn):
                    check = 1
                    return 1

            element = self.object_at(position_of_king.add(Vector(1, -1)))
            if element.position.in_chessboard() and element.color == opponent_color:
                if isinstance(element, Pawn):
                    check = 1
                    return 1

        ## teraz sprawdzamy wszystkie linie
        for i in range(x + 1, 8):
            position = Vector(i, y)
            element = self.object_at(position)
            if isinstance(element, Figure):
                if element.color == opponent_color:
                    if isinstance(element, Queen) or isinstance(element, Rook):
                        check = 1
                        return 1
                    else:
                        break
                else:
                    break

        for i in range(x - 1, -1, -1):
            position = Vector(i, y)
            element = self.object_at(position)
            if isinstance(element, Figure):
                if element.color == opponent_color:
                    if isinstance(element, Queen) or isinstance(element, Rook):
                        check = 1
                        return 1
                    else:
                        break
                else:
                    break

        for i in range(y - 1, -1, -1):
            position = Vector(x, i)
            element = self.object_at(position)
            if isinstance(element, Figure):
                if element.color == opponent_color:
                    if isinstance(element, Queen) or isinstance(element, Rook):
                        check = 1
                        return 1
                    else:
                        break
                else:
                    break

        for i in range(y + 1, 8):
            position = Vector(x, i)
            element = self.object_at(position)
            if isinstance(element, Figure):
                if element.color == opponent_color:
                    if isinstance(element, Queen) or isinstance(element, Rook):
                        check = 1
                        return 1
                    else:
                        break
                else:
                    break

        ## a teraz przekątne
        for i in range(1, 8):
            position = Vector(x + i, y + i)
            if not position.in_chessboard():
                break
            element = self.object_at(position)
            if element.color == opponent_color:
                if isinstance(element, Bishop):
                    check = 1
                    return 1
                else:
                    break
            else:
                break

        for i in range(1, 8):
            position = Vector(x - i, y - i)
            if not position.in_chessboard():
                break
            element = self.object_at(position)
            if element.color == opponent_color:
                if isinstance(element, Bishop):
                    check = 1
                    return 1
                else:
                    break
            else:
                break

        for i in range(1, 8):
            position = Vector(x + i, y - i)
            if not position.in_chessboard():
                break
            element = self.object_at(position)
            if element.color == opponent_color:
                if isinstance(element, Bishop):
                    check = 1
                    return 1
                else:
                    break
            else:
                break

        for i in range(1, 8):
            position = Vector(x - i, y + i)
            if not position.in_chessboard():
                break
            element = self.object_at(position)
            if element.color == opponent_color:
                if isinstance(element, Bishop):
                    check = 1
                    return 1
                else:
                    break
            else:
                break
        return check

    def get_take_en_passant(self):
        return self.take_en_passant

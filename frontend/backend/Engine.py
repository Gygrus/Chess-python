import copy
from backend.Chessboard import *
from backend.Figure import *


def column(x):
    return {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,}[x]


def row(x):
    return {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7,}[x]


def map(string):
    return Vector(row(string[1]), column(string[0]))


def translate_array(T):
    S = []
    for i in T:
        S.append((i.x, i.y))
    return S


class Engine:
    def __init__(self):
        self.chessboard = Chessboard()
        self.current_player = 'white'
        self.current_figure = None
        self.calculate_possible_moves()

    def choose_figure(self, position):
        self.current_figure = self.chessboard.object_at(position)
        if self.current_player != self.current_figure.color:
            self.current_figure = None


    def move_to_position(self, destination):
        flag = True
        for vector in self.current_figure.moves:
            if vector.equal(destination):
                self.move_and_validate(self.current_figure.position, destination)
                self.current_figure = None
                flag = False
                break
        if flag:
            self.choose_figure(destination)

    def move_and_validate(self, position, destination):
        figure = self.chessboard.object_at(position)
        if self.current_player != figure.color:
            print("You are trying to move opponent's figure")
            print("Try again")
            return
        if self.chessboard.is_possible_move(figure, destination):
            old_chessboard = copy.deepcopy(self.chessboard)
            self.move(figure, destination)
            king_position = self.chessboard.white_king_position if self.current_player == 'white' else self.chessboard.black_king_position
            col = 'white' if self.current_player == 'black' else 'black'
            if self.chessboard.is_check(king_position, col):
                self.chessboard = old_chessboard
                print("Your King is in check")
                print("Try again")
            else:
                self.chessboard.for_en_passant(figure, position)
                self.current_player = 'black' if self.current_player == 'white' else 'white'
        elif isinstance(figure, King):
            if self.is_castle_possible(figure, destination):
                col = 'white' if self.current_player == 'black' else 'black'
                if self.chessboard.is_check(figure.position, col):
                    print("Your King is in check")
                    print("Try again")
                    return
                old_chessboard = copy.deepcopy(self.chessboard)
                if destination.y == 6:
                    self.move(figure, Vector(destination.x, 5))
                    if self.chessboard.is_check(figure.position, col):
                        self.chessboard = old_chessboard
                        print("When castling Your King is in check")
                        print("Try again")
                        return
                    self.move(figure, destination)
                    self.move(self.chessboard.object_at(Vector(destination.x, 7)), Vector(destination.x, 5))
                    if self.chessboard.is_check(figure.position, col):
                        self.chessboard = old_chessboard
                        print("Your King is in check after castling")
                        print("Try again")
                        return
                    self.chessboard.for_en_passant(figure, position)
                    if self.current_player == 'white':
                        self.chessboard.white_king_position = figure.position
                    else:
                        self.chessboard.black_king_position = figure.position
                    self.current_player = 'black' if self.current_player == 'white' else 'white'

                elif destination.y == 2:
                    self.move(figure, Vector(destination.x, 3))
                    if self.chessboard.is_check(figure.position, col):
                        self.chessboard = old_chessboard
                        print("You are trying to move opponent's figure")
                        print("Try again")
                        return
                    self.move(figure, Vector(destination.x, 2))
                    self.move(self.chessboard.object_at(Vector(destination.x, 0)), Vector(destination.x, 3))
                    if self.chessboard.is_check(figure.position, col):
                        self.chessboard = old_chessboard
                        print("You are trying to move opponent's figure")
                        print("Try again")
                        return
                    self.chessboard.for_en_passant(figure, position)
                    if self.current_player == 'white':
                        self.chessboard.white_king_position = figure.position
                    else:
                        self.chessboard.black_king_position = figure.position
                    self.current_player = 'black' if self.current_player == 'white' else 'white'


            else:
                print("It is not a chess move")
                print("Try again")

        else:
            print("It is not a chess move")
            print("Try again")

        self.clear_moves_in_figures()
        self.calculate_possible_moves()
        if self.is_checkmate():
            print("CHECKMATE")
            return

        king_position = self.chessboard.white_king_position if self.current_player == 'white' else self.chessboard.black_king_position
        col = 'white' if self.current_player == 'black' else 'black'
        if self.chessboard.is_check(king_position, col):
            ## sprawdz czy mat
            print("CHECK")
        self.chessboard.print_board()
        print("White turn") if self.current_player == 'white' else print("Black turn")


    def play(self):
        while True:
            self.clear_moves_in_figures()
            self.calculate_possible_moves()
            if self.is_checkmate():
                print("CHECKMATE")
                break
            self.print_possible_moves()

            king_position = self.chessboard.white_king_position if self.current_player == 'white' else self.chessboard.black_king_position
            col = 'white' if self.current_player == 'black' else 'black'
            if self.chessboard.is_check(king_position, col):
                ## sprawdz czy mat
                print("CHECK")
            self.chessboard.print_board()
            print("White turn") if self.current_player == 'white' else print("Black turn")
            string = input("Write your move: ")
            if len(string) != 5:
                print("White right move")
                print("Try again")
                continue
            position = map(string[0:2])
            destination = map(string[3:5])
            figure = self.chessboard.object_at(position)
            if self.current_player != figure.color:
                print("You are trying to move opponent's figure")
                print("Try again")
                continue
            if self.chessboard.is_possible_move(figure, destination):
                old_chessboard = copy.deepcopy(self.chessboard)
                self.move(figure, destination)
                king_position = self.chessboard.white_king_position if self.current_player == 'white' else self.chessboard.black_king_position
                col = 'white' if self.current_player == 'black' else 'black'
                if self.chessboard.is_check(king_position, col):
                    self.chessboard = old_chessboard
                    print("Your King is in check")
                    print("Try again")
                else:
                    self.chessboard.for_en_passant(figure, position)
                    self.current_player = 'black' if self.current_player == 'white' else 'white'
            elif isinstance(figure, King):
                if self.is_castle_possible(figure, destination):
                    col = 'white' if self.current_player == 'black' else 'black'
                    if self.chessboard.is_check(figure.position, col):
                        print("Your King is in check")
                        print("Try again")
                        continue
                    old_chessboard = copy.deepcopy(self.chessboard)
                    if destination.y == 6:
                        self.move(figure, Vector(destination.x, 5))
                        if self.chessboard.is_check(figure.position, col):
                            self.chessboard = old_chessboard
                            print("When castling Your King is in check")
                            print("Try again")
                            continue
                        self.move(figure, destination)
                        self.move(self.chessboard.object_at(Vector(destination.x, 7)), Vector(destination.x, 5))
                        if self.chessboard.is_check(figure.position, col):
                            self.chessboard = old_chessboard
                            print("Your King is in check after castling")
                            print("Try again")
                            continue
                        self.chessboard.for_en_passant(figure, position)
                        if self.current_player == 'white':
                            self.chessboard.white_king_position = figure.position
                        else:
                            self.chessboard.black_king_position = figure.position
                        self.current_player = 'black' if self.current_player == 'white' else 'white'

                    elif destination.y == 2:
                        self.move(figure, Vector(destination.x, 3))
                        if self.chessboard.is_check(figure.position, col):
                            self.chessboard = old_chessboard
                            print("You are trying to move opponent's figure")
                            print("Try again")
                            continue
                        self.move(figure, Vector(destination.x, 2))
                        self.move(self.chessboard.object_at(Vector(destination.x, 0)), Vector(destination.x, 3))
                        if self.chessboard.is_check(figure.position, col):
                            self.chessboard = old_chessboard
                            print("You are trying to move opponent's figure")
                            print("Try again")
                            continue
                        self.chessboard.for_en_passant(figure, position)
                        if self.current_player == 'white':
                            self.chessboard.white_king_position = figure.position
                        else:
                            self.chessboard.black_king_position = figure.position
                        self.current_player = 'black' if self.current_player == 'white' else 'white'
                else:
                    print("It is not a chess move")
                    print("Try again")

            else:
                print("It is not a chess move")
                print("Try again")

    def move(self, element, destination):
        old_position = element.position
        element.position = destination
        self.chessboard.move_object(old_position, element)

    def is_castle_possible(self, element, destination):
        if element.right_to_castling == 'no':
            return False
        row = 7 if element.color == 'white' else 0
        if destination.equal(Vector(row, 6)) and isinstance(self.chessboard.object_at(Vector(row, 7)), Rook):
            if self.chessboard.object_at(Vector(row, 7)).right_to_castling == 'yes':
                if not isinstance(self.chessboard.object_at(Vector(row, 6)), Figure):
                    if not isinstance(self.chessboard.object_at(Vector(row, 5)), Figure):
                        return True

        if destination.equal(Vector(row, 2)) and isinstance(self.chessboard.object_at(Vector(row, 0)), Rook):
            if self.chessboard.object_at(Vector(row, 0)).right_to_castling == 'yes':
                if not isinstance(self.chessboard.object_at(Vector(row, 3)), Figure):
                    if not isinstance(self.chessboard.object_at(Vector(row, 2)), Figure):
                        if not isinstance(self.chessboard.object_at(Vector(row, 1)), Figure):
                            return True

        return False

    def calculate_possible_moves(self):
        for i in range(8):
            for j in range(8):
                element = self.chessboard.object_at(Vector(i, j))
                if element.color == self.current_player and isinstance(element, Figure):
                    element.calculate(self)

        row = 7 if self.current_player == 'white' else 0
        figure = self.chessboard.object_at(Vector(row, 4))
        if isinstance(figure, King) and figure.color == self.current_player:
            if self.is_castle_possible(figure, Vector(row, 6)): ## krótka
                old_eng = copy.deepcopy(self)
                king = old_eng.chessboard.object_at(Vector(row, 4))
                col = 'white' if old_eng.current_player == 'black' else 'black'
                if not old_eng.chessboard.is_check(king.position, col):
                    old_eng.move(king, Vector(row, 5))
                    if not old_eng.chessboard.is_check(king.position, col):
                        old_eng.move(king, Vector(row, 6))
                        old_eng.move(old_eng.chessboard.object_at(Vector(row, 7)), Vector(row, 5))
                        if not old_eng.chessboard.is_check(king.position, col):
                            figure.moves.append(Vector(row, 6))
                            old_eng.chessboard.board[row][6] = figure

            if self.is_castle_possible(figure, Vector(row, 2)):
                old_eng = copy.deepcopy(self)
                king = old_eng.chessboard.object_at(Vector(row, 4))
                col = 'white' if old_eng.current_player == 'black' else 'black'
                if not old_eng.chessboard.is_check(king.position, col):
                    old_eng.move(king, Vector(row, 3))
                    if not old_eng.chessboard.is_check(king.position, col):
                        old_eng.move(king, Vector(row, 2))
                        old_eng.move(old_eng.chessboard.object_at(Vector(row, 0)), Vector(row, 3))
                        if not old_eng.chessboard.is_check(king.position, col):
                            figure.moves.append(Vector(row, 2))
                            old_eng.chessboard.board[row][2] = figure

    def print_possible_moves(self):
        for i in range(8):
            for j in range(8):
                element = self.chessboard.object_at(Vector(i, j))
                if element.color == self.current_player and isinstance(element, Figure):
                    print(element.print_in_console(), translate_array(element.moves))

    def clear_moves_in_figures(self):
        for i in range(8):
            for j in range(8):
                element = self.chessboard.object_at(Vector(i, j))
                if element.color == self.current_player and isinstance(element, Figure):
                    element.moves = []

    def is_checkmate(self):
        for i in range(8):
            for j in range(8):
                element = self.chessboard.object_at(Vector(i, j))
                if element.color == self.current_player and isinstance(element, Figure):
                    if len(element.moves) > 0:
                        return False
        return True
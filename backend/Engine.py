import copy
from backend.Chessboard import *
from backend.Figure import *
import time


def column(x):
    return {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,}[x]


def row(x):
    return {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7,}[x]


def reverse_column(x):
    return {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h',}[x]


def reverse_row(x):
    return {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1,}[x]


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
        # self.frontend_modal = None
        self.current_player = 'white'
        self.current_figure = None
        self.game_record = []
        # self.history = []
        self.piece = []
        self.state = None
        self.calculate_possible_moves()

    # def register_frontend_modal(self, frontend_modal):
    #     self.frontend_modal = frontend_modal

    # def invoke_frontend_promotion(self, current_player, element, position):
    #     self.frontend_modal.pop_up(current_player, element, position)

    def choose_figure(self, position):
        self.current_figure = self.chessboard.object_at(position)
        if self.current_player != self.current_figure.color:
            self.current_figure = None

    def move_to_position(self, destination):
        response = None
        flag = True
        for vector in self.current_figure.moves:
            if vector.equal(destination):
                response = self.move_and_validate(self.current_figure.position, destination)
                self.current_figure = None
                flag = False
                break
        if flag:
            self.choose_figure(destination)

        return response

    def move_and_validate(self, position, destination):
        print("-------")
        figure = self.chessboard.object_at(position)
        self.move(position, destination)
        self.chessboard.for_en_passant(figure, position)
        response = self.promotion() ## tu trzeba obsłużyć podmianę pionka na figure
        self.convert_record()
        self.game_record.append(self.piece)
        self.piece = []
        self.print_game_record()
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        self.clear_moves_in_figures()
        self.calculate_possible_moves()
        # self.print_possible_moves()
        king_position = self.chessboard.white_king_position if self.current_player == 'white' else self.chessboard.black_king_position
        col = 'white' if self.current_player == 'black' else 'black'
        if self.chessboard.is_check(king_position, col):
            self.state = "check"
            print("CHECK") ## tu trzeba obsłużyć szacha
            if self.is_opponent_has_no_moves():
                print("CHECKMATE") ## tu trzeba obsłużyć mata i zakończyć
                self.state = "checkmate"
                return
        else:
            if self.is_opponent_has_no_moves():
                print("DRAW") ## tu trzeba obsłużyć pata i zakończyć
                self.state = "draw"
                return
        print("White turn") if self.current_player == 'white' else print("Black turn")
        return response

    def move(self, position, destination):
        figure = self.chessboard.object_at(position)
        row = position.x
        if isinstance(figure, King):
            if figure.is_castle_move(destination):
                if destination.y == 2:
                    rook = self.chessboard.object_at(Vector(row, 0))
                    rook.position = Vector(row, 3)
                    self.chessboard.move_object(Vector(row, 0), rook)
                    self.piece.append(["Rook", Vector(row, 0), Vector(row, 3), False, ""])
                else:
                    rook = self.chessboard.object_at(Vector(row, 7))
                    rook.position = Vector(row, 5)
                    self.chessboard.move_object(Vector(row, 7), rook)
                    self.piece.append(["Rook", Vector(row, 7), Vector(row, 5), False, ""])

        figure.position = destination
        killed = self.chessboard.move_object(position, figure)

        if isinstance(figure, Pawn):
            self.piece.append(["Pawn", position, destination, killed, ""])
        if isinstance(figure, Rook):
            self.piece.append(["Rook", position, destination, killed, ""])
        if isinstance(figure, Knight):
            self.piece.append(["Knight", position, destination, killed, ""])
        if isinstance(figure, Bishop):
            self.piece.append(["Bishop", position, destination, killed, ""])
        if isinstance(figure, Queen):
            self.piece.append(["Queen", position, destination, killed, ""])
        if isinstance(figure, King):
            self.piece.append(["King", position, destination, killed, ""])

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
                if isinstance(element, Figure) and element.color == self.current_player:
                    element.calculate(self)

        row = 7 if self.current_player == 'white' else 0
        figure = self.chessboard.object_at(Vector(row, 4))
        if isinstance(figure, King) and figure.color == self.current_player:
            if self.is_castle_possible(figure, Vector(row, 6)):
                old_eng = copy.deepcopy(self)
                king = old_eng.chessboard.object_at(Vector(row, 4))
                col = 'white' if old_eng.current_player == 'black' else 'black'
                if not old_eng.chessboard.is_check(king.position, col):
                    old_eng.move(king.position, Vector(row, 5))
                    if not old_eng.chessboard.is_check(king.position, col):
                        old_eng.move(king.position, Vector(row, 6))
                        old_eng.move(Vector(row, 7), Vector(row, 5))
                        if not old_eng.chessboard.is_check(king.position, col):
                            figure.moves.append(Vector(row, 6))
                            old_eng.chessboard.board[row][6] = figure

            if self.is_castle_possible(figure, Vector(row, 2)):
                old_eng = copy.deepcopy(self)
                king = old_eng.chessboard.object_at(Vector(row, 4))
                col = 'white' if old_eng.current_player == 'black' else 'black'
                if not old_eng.chessboard.is_check(king.position, col):
                    old_eng.move(king.position, Vector(row, 3))
                    if not old_eng.chessboard.is_check(king.position, col):
                        old_eng.move(king.position, Vector(row, 2))
                        old_eng.move(Vector(row, 0), Vector(row, 3))
                        if not old_eng.chessboard.is_check(king.position, col):
                            figure.moves.append(Vector(row, 2))
                            old_eng.chessboard.board[row][2] = figure

    def print_possible_moves(self):
        for i in range(8):
            for j in range(8):
                element = self.chessboard.object_at(Vector(i, j))
                if element.color == self.current_player and isinstance(element, Figure):
                    print(element.print_in_console(), translate_array(element.moves))
                    pass

    def clear_moves_in_figures(self):
        for i in range(8):
            for j in range(8):
                element = self.chessboard.object_at(Vector(i, j))
                if isinstance(element, Figure) and element.color == self.current_player:
                    element.moves = []

    def is_opponent_has_no_moves(self):
        for i in range(8):
            for j in range(8):
                element = self.chessboard.object_at(Vector(i, j))
                if element.color == self.current_player and isinstance(element, Figure):
                    if len(element.moves) > 0:
                        return False
        return True

    def promotion(self):
        if self.current_player == 'white':
            row1 = 0
        else:
            row1 = 7
        for i in range(8):
            element = self.chessboard.object_at(Vector(row1, i))
            position = element.position


            if isinstance(element, Pawn) and (position.x == 7 or position.x == 0):
                return ["promotion", self.current_player, element, position]


    def test_promotion(self, type, element, position):
        figure = self.chessboard.object_at(position)
        self.move(position, position)
        self.chessboard.for_en_passant(figure, position)
        if type == "q":
            figure = Queen(element.color, position)
            self.game_record[len(self.game_record) - 1][0] = self.game_record[len(self.game_record) - 1][0][0: 11] + ' ' + "Queen"
        elif type == "r":
            figure = Rook(element.color, position)
            self.game_record[len(self.game_record) - 1][0] = self.game_record[len(self.game_record) - 1][0][0: 12] + ' ' + "Rook"
        elif type == "b":
            figure = Bishop(element.color, position)
            self.game_record[len(self.game_record) - 1][0] = self.game_record[len(self.game_record) - 1][0][0: 12] + ' ' + "Bishop"
        else:
            figure = Knight(element.color, position)
            self.game_record[len(self.game_record) - 1][0] = self.game_record[len(self.game_record) - 1][0][0: 12] + ' ' + "Knight"
        self.chessboard.board[position.x][position.y] = figure

        self.print_game_record()
        self.piece = []
        self.clear_moves_in_figures()
        self.calculate_possible_moves()
        king_position = self.chessboard.white_king_position if self.current_player == 'white' else self.chessboard.black_king_position
        col = 'white' if self.current_player == 'black' else 'black'
        if self.chessboard.is_check(king_position, col):
            print("CHECK") ## tu trzeba obsłużyć szacha
            self.state = "check"
            if self.is_opponent_has_no_moves():
                print("CHECKMATE") ## tu trzeba obsłużyć mata i zakończyć
                self.state = "checkmate"
                return
        else:
            if self.is_opponent_has_no_moves():
                self.state = "draw"
                print("DRAW") ## tu trzeba obsłużyć pata i zakończyć
                return
        print("White turn") if self.current_player == 'white' else print("Black turn")

    def print_game_record(self):
        print(self.game_record)
        # counter = 1
        # for object in self.game_record:
        #     for move in object:
        #         print(move)
        #         # print(counter, "|", move[0], "(", move[1].x, move[1].y, ")", "(", move[2].x, move[2].y, ")", move[3], move[4], "|", end=" ")
        #     counter += 1
        # print()

    def convert_record(self):
        if len(self.piece) == 2:
            if self.piece[1][2].y == 6:
                rec = 'O-O'
            else:
                rec = 'O-O-O'

        else:
            T = self.piece[0]
            rec = T[0]
            rec += ' ' + str(reverse_column(T[1].y)) + str(reverse_row(T[1].x))
            if T[3] == True:
                rec += 'x'
            else:
                rec += ' '
            rec += str(reverse_column(T[2].y)) + str(reverse_row(T[2].x))

            if T[1].equal(T[2]):
                rec += ' ' + T[4]

        self.piece = [rec]


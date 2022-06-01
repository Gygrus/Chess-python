import copy
from backend.Chessboard import Chessboard
from backend.Figure import Figure, Pawn, Rook, King, Knight, Bishop, Queen
from backend.Translator import from_column, from_row
from backend.Vector import Vector


class Engine:
    def __init__(self):
        self.chessboard = Chessboard()
        self.current_player = 'white'
        self.current_figure = None
        self.game_record = []
        self.piece = []
        self.state = ""
        self.calculate_possible_moves()

    def switch_players(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def choose_figure(self, position):
        self.current_figure = self.chessboard.object_at(position)
        if isinstance(self.current_figure, Figure) and self.current_player != self.current_figure.color:
            self.current_figure = None

    def move_to_position(self, destination):
        response, flag = None, True
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
        print("--- MOVE ---")
        self.state = ""
        figure = self.chessboard.object_at(position)
        self.move(position, destination)
        self.chessboard.for_en_passant(figure, position)
        response = self.promotion()
        self.convert_record()
        self.game_record.append(self.piece)
        self.piece = []
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        self.clear_moves_in_figures()
        self.calculate_possible_moves()
        king_position = self.chessboard.white_king_position if self.current_player == 'white' \
            else self.chessboard.black_king_position
        col = 'white' if self.current_player == 'black' else 'black'
        if self.chessboard.is_check(king_position, col):
            self.state = "check"
            if self.is_opponent_has_no_moves():
                self.state = "checkmate"
                return
        else:
            if self.no_mate_possible():
                self.state = "draw"
                return
            if self.is_opponent_has_no_moves():
                self.state = "draw"
                return
        return response

    def move(self, position, destination):
        figure, row = self.chessboard.object_at(position), position.x
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

    def no_mate_possible(self):
        white_counter, black_counter = 0, 0
        white_figure, black_figure = None, None
        for i in range(8):
            for j in range(8):
                element = self.chessboard.object_at(Vector(i, j))
                if not isinstance(element, King) and isinstance(element, Figure):
                    if element.color == 'white':
                        white_figure = element
                        white_counter += 1
                    else:
                        black_figure = element
                        black_counter += 1
                if black_counter + white_counter > 1:
                    return False

        if black_counter == 0 and white_counter == 0:
            return True

        if black_counter == 1 and white_counter == 0 and isinstance(black_figure, (Bishop, Knight)):
            return True

        if black_counter == 0 and white_counter == 1 and isinstance(white_figure, (Bishop, Knight)):
            return True

    def promotion(self):
        row = 0 if self.current_player == 'white' else 7
        for i in range(8):
            element = self.chessboard.object_at(Vector(row, i))
            position = element.position

            if isinstance(element, Pawn) and (position.x == 7 or position.x == 0):
                return ["promotion", self.current_player, element, position]

        return ["move"]

    def test_promotion(self, new_figure_type, element, position):
        figure = self.chessboard.object_at(position)
        self.move(position, position)
        self.chessboard.for_en_passant(figure, position)
        length = len(self.game_record) - 1
        if new_figure_type == "q":
            figure = Queen(element.color, position)
            self.game_record[length][0] = self.game_record[length][0][0: 11] + ' ' + "Queen"
        elif new_figure_type == "r":
            figure = Rook(element.color, position)
            self.game_record[length][0] = self.game_record[length][0][0: 11] + ' ' + "Rook"
        elif new_figure_type == "b":
            figure = Bishop(element.color, position)
            self.game_record[length][0] = self.game_record[length][0][0: 11] + ' ' + "Bishop"
        else:
            figure = Knight(element.color, position)
            self.game_record[length][0] = self.game_record[length][0][0: 11] + ' ' + "Knight"
        self.chessboard.board[position.x][position.y] = figure

        self.piece = []
        self.clear_moves_in_figures()
        self.calculate_possible_moves()
        king_position = self.chessboard.white_king_position if self.current_player == 'white' else \
            self.chessboard.black_king_position
        col = 'white' if self.current_player == 'black' else 'black'
        if self.chessboard.is_check(king_position, col):
            self.state = "check"
            if self.is_opponent_has_no_moves():
                self.state = "checkmate"
                return
            return
        else:
            if self.is_opponent_has_no_moves():
                self.state = "draw"
                return

        self.state = ""

    def convert_record(self):
        if len(self.piece) == 2:
            rec = 'O-O' if self.piece[1][2].y == 6 else 'O-O-O'
        else:
            temp = self.piece[0]
            rec = temp[0]
            rec += ' ' + str(from_column(temp[1].y)) + str(from_row(temp[1].x))
            rec += 'x' if temp[3] else ' '
            rec += str(from_column(temp[2].y)) + str(from_row(temp[2].x))

            if temp[1].equal(temp[2]):
                rec += ' ' + temp[4]

        self.piece = [rec]

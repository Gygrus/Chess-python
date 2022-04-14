from Chessboard import *

def column(x):
    return {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,}[x]


def row(x):
    return {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7,}[x]


def map(string):
    return Vector(row(string[1]), column(string[0]))


class Engine:
    def __init__(self):
        self.chessboard = Chessboard()
        self.current_player = 'white'

    def play(self):
        while True:
            self.chessboard.print_board()
            print("White turn") if self.current_player == 'white' else print("Black turn")
            string = input("Write your move:")
            position = map(string[0:2])
            destination = map(string[3:5])
            figure = self.chessboard.object_at(position)
            if self.current_player != figure.color:
                print("You are trying to move opponent's figure")
                print("Try again")
                continue
            if self.chessboard.is_possible_move(figure, destination):
                self.move(figure, destination)
            else:
                print("It is not a chess move")
                print("Try again")

    def move(self, figure, destination):
        old_position = figure.position
        figure.position = destination
        self.chessboard.move_object(old_position, figure)
        self.current_player = 'black' if self.current_player == 'white' else 'white'

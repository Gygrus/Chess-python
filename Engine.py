from Chessboard import *
from Figure import Figure


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
            ## valitadion for input
            self.move(map(string[0:2]), map(string[3:5]))

    def move(self, position, destination):
        figure = self.chessboard.object_at(position)
        if isinstance(figure, Figure) and self.current_player == figure.color:
            figure.position = destination
            self.chessboard.move_object(position, figure)
            self.current_player = 'black' if self.current_player == 'white' else 'white'
        else:
            print("You are trying to move opponent's figure or empty place")
            print("Try again")



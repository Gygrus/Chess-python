class History:
    def __init__(self):
        self.hist = []

    def add_move(self, chessboard):
        self.hist.append(chessboard)

    def delete_move(self):
        self.hist.pop()

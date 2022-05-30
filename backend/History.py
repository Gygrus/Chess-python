import copy


class History:
    def __init__(self):
        self.hist = []

    def add_move(self, chessboard, game_status):
        to_append = copy.deepcopy(chessboard)
        self.hist.append([to_append, game_status])

    def delete_move(self):
        self.hist.pop()
        return self.hist[-1]

    def is_undo_possible(self):
        return len(self.hist) > 1

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.image import Image
from backend import Engine as en
from backend import Vector as v
from backend import Figure as f


# kv = Builder.load_file("chessboard.kv")

class Cell(Label):
    cell_id = StringProperty()
    img_source = StringProperty()


    def __init__(self, cell_id, chessboard, engine, figure, **kwargs):
        super().__init__(**kwargs)
        self.cell_id = cell_id
        self.text = ""
        self.engine = engine
        self.chessboard = chessboard
        self.num_mode = ((int(cell_id[0]) + int(cell_id[1])) % 2)/1
        self.img_source = figure.image
        self.figure = figure
        self.board_representation = figure.image
        self.position = v.Vector(int(self.cell_id[0]), int(self.cell_id[1]))

        with self.canvas.before:
            Color(self.num_mode/2 + 1/8, self.num_mode/4 + 1/5, self.num_mode/3, 1)

            self.rect = Rectangle(pos=self.center,
                                  size=(self.width / 2.,
                                        self.height / 2.))

            self.bind(pos=self.update_rect,
                      size=self.update_rect)

            if isinstance(self.engine.current_figure, f.Figure) and self.engine.current_figure.check_if_in_moves(self.position):
                Color(0, 0, 0, 0.2)

                self.circ = Ellipse(angle_start = 0,
                                    angle_end=360,
                                    pos = self.center,
                                    size = (self.width,
                                            self.height),)

                self.bind(pos=self.update_circ,
                          size=self.update_circ)



    def update_circ(self, *args):
        self.circ.pos = self.pos
        self.circ.size = self.size

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.touch_handler()

            return True

    # def on_touch_move(self, touch):
    #     if touch.grab_current is self:
    #         self.pos = [touch.x - 25, touch.y - 25]
    # # now we only handle moves which we have grabbed
    #
    # def on_touch_up(self, touch):
    #     if touch.grab_current is self:
    #         touch.ungrab(self)
    #         # and finish up here

    def touch_handler(self):
        if self.engine.chessboard.is_figure(self.position) and \
                not isinstance(self.engine.current_figure, f.Figure):
            self.engine.choose_figure(self.position)
            self.chessboard.update_chessboard()
        elif isinstance(self.engine.current_figure, f.Figure):
            self.engine.move_to_position(self.position)
            self.chessboard.update_chessboard()
        else:
            self.engine.current_figure = None



        # if self.chessboard.board_positions[int(self.cell_id[0])][int(self.cell_id[1])] != "xx" and \
        #         not self.chessboard.current_clicked:
        #     self.chessboard.set_current_clicked(self)
        # elif self.chessboard.current_clicked:
        #     self.chessboard.update_positions(self)
        # else:
        #     self.chessboard.set_current_clicked(None)


class DemoUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ChessBoard(GridLayout):
    engine = en.Engine()
    cells = []

    initial_positions_v2 = engine.chessboard.board

    initial_positions = [["rb", "kb", "bb", "qb", "kingb", "bb", "kb", "rb"],
                       ["pb", "pb", "pb", "pb", "pb", "pb", "pb", "pb"],
                       ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                       ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                       ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                       ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                       ["pw", "pw", "pw", "pw", "pw", "pw", "pw", "pw"],
                       ["rw", "kw", "bw", "qw", "kingw", "bw", "kw", "rw"]]

    board_positions = engine.chessboard.board



    figures_dict = {"rb": "./assets/rb.png",
                    "kb": "./assets/kb.png",
                    "bb": "./assets/bb.png",
                    "kingb": "./assets/kingb.png",
                    "qb": "./assets/qb.png",
                    "pb": "./assets/pb.png",
                    "rw": "./assets/rw.png",
                    "kw": "./assets/kw.png",
                    "bw": "./assets/bw.png",
                    "kingw": "./assets/kingw.png",
                    "qw": "./assets/qw.png",
                    "pw": "./assets/pw.png",
                    "xx": "./assets/blank.png"
                    }


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_clicked = None
        self.fill_chessboard()
        self.cells = []



    def set_current_clicked(self, cell):
        self.current_clicked = cell
        print("New clicked cell had been just set")
        if self.current_clicked:
            print(self.current_clicked.cell_id)

    def fill_chessboard(self):
        for x in range(8):
            for y in range(8):
                text_to_print = str(x) + str(y)
                lab = Cell(text_to_print, self, self.engine, self.board_positions[x][y])
                self.cells.append(lab)

                self.add_widget(lab)
                self.ids[text_to_print] = lab

    def update_positions(self, cell):
        self.board_positions[int(self.current_clicked.cell_id[0])][int(self.current_clicked.cell_id[1])] = "xx"
        self.board_positions[int(cell.cell_id[0])][int(cell.cell_id[1])] = self.current_clicked.board_representation
        self.set_current_clicked(None)
        self.update_chessboard()

    def update_chessboard(self):
        while self.children:
            for cell in self.children:
                self.remove_widget(cell)

        self.fill_chessboard()

    def reset_chessboard(self):
        while self.children:
            for cell in self.children:
                self.remove_widget(cell)

        for x in range(8):
            for y in range(8):
                self.board_positions[x][y] = self.initial_positions[x][y]

        self.fill_chessboard()

# class ChessBoardDemo(App):
#     def build(self):
#         return DemoUI()
#
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     ChessBoardDemo().run()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
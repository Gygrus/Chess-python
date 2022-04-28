from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.image import Image
from kivy.clock import Clock
from functools import partial
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



class GameLayout(BoxLayout):
    chessboard_object = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_times(self, time_value_in_sec, increment_value):
        self.chessboard_object.set_clocks(time_value_in_sec, increment_value)



class ChessBoard(GridLayout):
    engine = en.Engine()
    cells = []
    white_time_as_str_seconds = StringProperty()
    white_time_as_str_minutes = StringProperty()
    black_time_as_str_seconds = StringProperty()
    black_time_as_str_minutes = StringProperty()
    increment_value = 0
    initial_positions_v2 = engine.chessboard.board.copy()
    board_positions = engine.chessboard.board


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_clicked = None
        self.fill_chessboard()
        self.cells = []
        self.times = [3600, 3600]
        self.clocks = [0, 0]


    def set_clocks(self, time_value_in_min, increment_value):
        if len(time_value_in_min) == 0 or time_value_in_min[0] == "-":
            time_value_in_min = 0

        if len(increment_value) == 0:
            increment_value = 0

        self.times = [int(time_value_in_min)*60, int(time_value_in_min)*60]
        self.clocks = [0, 0]
        self.clocks[0] = Clock.schedule_interval(partial(self.decrement_time, self.times, 0), 1)
        self.current_timer = self.clocks[0]
        self.increment_value = int(increment_value)
        print(self.increment_value)

    def decrement_time(self, time_remaining, index, *largs):
        time_remaining[index] -= 1
        self.update_current_time_counters()
        if time_remaining[0] <= 0:
            if self.engine.current_player == "white":
                self.clocks[0].cancel()
                print("Black won")
            else:
                self.clocks[1].cancel()
                print("Black won")

        elif time_remaining[1] <= 0:
            if self.engine.current_player == "white":
                self.clocks[0].cancel()
                print("White won")
            else:
                self.clocks[1].cancel()
                print("White won")



    def increment_time(self, curr_counter, increment_value):
        self.times[curr_counter] += increment_value
        self.update_current_time_counters()


    def change_current_timer(self, clocks, last_counter, curr_counter):
        clocks[last_counter].cancel()
        clocks[curr_counter] = Clock.schedule_interval(partial(self.decrement_time, self.times, curr_counter), 1)
        self.increment_time(last_counter, self.increment_value)

    def update_current_time_counters(self):
        self.white_time_as_str_minutes = str(self.times[0] // 60)
        self.white_time_as_str_seconds = str(self.times[0] % 60)
        self.black_time_as_str_minutes = str(self.times[1] // 60)
        self.black_time_as_str_seconds = str(self.times[1] % 60)


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
        if self.engine.current_figure is None:
            if self.engine.current_player == "white":
                self.change_current_timer(self.clocks, 1, 0)
            else:
                self.change_current_timer(self.clocks, 0, 1)


    def reset_chessboard(self):
        while self.children:
            for cell in self.children:
                self.remove_widget(cell)

        for x in range(8):
            for y in range(8):
                self.board_positions[x][y] = self.initial_positions_v2[x][y]

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

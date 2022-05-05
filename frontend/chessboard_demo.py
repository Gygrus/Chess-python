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
import time
from functools import partial
from backend import Engine as en
from backend import Vector as v
from backend import Figure as f
import Cell

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
    reversed = False
    paused = False
    finished = False


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_clicked = None
        self.fill_chessboard_initial()
        # self.cells = []
        self.times = [3600, 3600]
        self.clocks = [0, 0]

    def reverse_chessboard(self):
        self.reversed = not self.reversed

    def switch_pause(self):
        if self.finished:
            return

        if self.paused:
            if self.engine.current_player == "white":
                self.clocks[0] = Clock.schedule_interval(partial(self.decrement_time, self.times, 0), 0.1)
            else:
                self.clocks[1] = Clock.schedule_interval(partial(self.decrement_time, self.times, 1), 0.1)
        else:
            if self.engine.current_player == "white":
                self.clocks[0].cancel()
            else:
                self.clocks[1].cancel()

        self.paused = not self.paused


    def set_clocks(self, time_value_in_min, increment_value):
        if len(time_value_in_min) == 0 or time_value_in_min[0] == "-":
            time_value_in_min = 0

        if len(increment_value) == 0:
            increment_value = 0

        self.times = [int(time_value_in_min)*600, int(time_value_in_min)*600]
        self.clocks = [0, 0]
        self.clocks[0] = Clock.schedule_interval(partial(self.decrement_time, self.times, 0), 0.1)
        self.increment_value = int(increment_value)


    def decrement_time(self, time_remaining, index, *largs):
        if self.paused or (index == 0 and self.engine.current_player == "black") or (index == 1 and self.engine.current_player == "white"):
            return False

        time_remaining[index] -= 1

        if time_remaining[0] <= 0:
            time_remaining[0] = 0
            self.finished = True
            if self.engine.current_player == "white":
                self.clocks[0].cancel()
                print("Black won")
            else:
                self.clocks[1].cancel()
                print("Black won")

        elif time_remaining[1] <= 0:
            time_remaining[1] = 0
            self.finished = True
            if self.engine.current_player == "white":
                self.clocks[0].cancel()
                print("White won")
            else:
                self.clocks[1].cancel()
                print("White won")

        self.update_current_time_counters()


    def increment_time(self, curr_counter, increment_value):
        self.times[curr_counter] += increment_value*10
        self.update_current_time_counters()


    def change_current_timer(self, clocks, last_counter, curr_counter):
        clocks[last_counter].cancel()
        clocks[curr_counter] = Clock.schedule_interval(partial(self.decrement_time, self.times, curr_counter), 0.1)
        self.increment_time(last_counter, self.increment_value)

    def update_current_time_counters(self):
        self.white_time_as_str_minutes = str(self.times[0] // 600) if len(str(self.times[0] // 600)) > 1 else str(0)+str(self.times[0] // 600)
        self.white_time_as_str_seconds = str(self.times[0] % 600 // 10) + ":" + str(self.times[0] % 10) if len(str(self.times[0] % 600 // 10)) > 1 else str(0)+str(self.times[0] % 600 // 10) + ":" + str(self.times[0] % 10)
        self.black_time_as_str_minutes = str(self.times[1] // 600) if len(str(self.times[1] // 600)) > 1 else str(0)+str(self.times[1] // 600)
        self.black_time_as_str_seconds = str(self.times[1] % 600 // 10) + ":" + str(self.times[1] % 10) if len(str(self.times[1] % 600 // 10)) > 1 else str(0)+str(self.times[1] % 600 // 10) + ":" + str(self.times[1] % 10)

    def fill_chessboard_initial(self):
        for x in range(8):
            for y in range(8):
                text_to_print = str(7-x) + str(7-y) if self.reversed else str(x)+str(y)
                lab = Cell.Cell(text_to_print, self, self.engine, self.board_positions[7-x][7-y] if self.reversed else self.board_positions[x][y])

                self.add_widget(lab)
                self.ids[text_to_print] = lab

    def fill_chessboard(self):
        for x in range(8):
            for y in range(8):
                text_to_print = str(7-x) + str(7-y) if self.reversed else str(x)+str(y)
                self.ids[text_to_print].update_content(self.board_positions[7-x][7-y] if self.reversed else self.board_positions[x][y])


    def update_chessboard(self):
        if self.engine.current_figure is None:
            if self.engine.current_player == "white":
                self.change_current_timer(self.clocks, 1, 0)
            else:
                self.change_current_timer(self.clocks, 0, 1)
        self.fill_chessboard()


    def revert_chessboard(self):
        while self.children:
            for cell in self.children:
                self.remove_widget(cell)

        self.fill_chessboard_initial()







from kivy.clock import Clock
from functools import partial

class TimerManager:
    increment_value = 0
    chessboard_widget = None

    def __init__(self):
        self.times = [3600, 3600]
        self.clocks = [0, 0]


    def set_chessboard_widget(self, chessboard_widget):
        self.chessboard_widget = chessboard_widget

    def switch_pause(self):
        if self.chessboard_widget.finished:
            return

        if self.chessboard_widget.paused:
            if self.chessboard_widget.engine.current_player == "white":
                self.clocks[0] = Clock.schedule_interval(partial(self.decrement_time, self.times, 0), 0.1)
            else:
                self.clocks[1] = Clock.schedule_interval(partial(self.decrement_time, self.times, 1), 0.1)
        else:
            if not isinstance(self.clocks[0], int):
                self.clocks[0].cancel()
            if not isinstance(self.clocks[1], int):
                self.clocks[1].cancel()

        self.chessboard_widget.paused = not self.chessboard_widget.paused

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
        if self.chessboard_widget.finished:
            self.chessboard_widget.paused = True

        if self.chessboard_widget.paused or (index == 0 and self.chessboard_widget.engine.current_player == "black") or \
                (index == 1 and self.chessboard_widget.engine.current_player == "white") \
                or self.chessboard_widget.finished:
            return False

        time_remaining[index] -= 1


        if time_remaining[0] <= 0:
            time_remaining[0] = 0

        if time_remaining[1] <= 0:
            time_remaining[1] = 0

        if time_remaining[0] <= 0:
            self.finished = True
            if self.chessboard_widget.engine.current_player == "white":
                self.clocks[0].cancel()
                self.chessboard_widget.engine.state = "Czarny wygrał!"
                print("Black won")
            else:
                self.clocks[1].cancel()
                self.chessboard_widget.engine.state = "Czarny wygrał!"
                print("Black won")
            self.chessboard_widget.timer_manager.switch_pause()
            self.chessboard_widget.fill_chessboard()


        elif time_remaining[1] <= 0:
            self.chessboard_widget.finished = True
            if self.chessboard_widget.engine.current_player == "white":
                self.clocks[0].cancel()
                self.chessboard_widget.engine.state = "Biały wygrał!"
                print("White won")
            else:
                self.clocks[1].cancel()
                self.chessboard_widget.engine.state = "Biały wygrał!"
                print("White won")
            self.chessboard_widget.timer_manager.switch_pause()
            self.chessboard_widget.fill_chessboard()

        self.update_current_time_counters()


    def increment_time(self, curr_counter, increment_value):
        self.times[curr_counter] += increment_value*10
        self.update_current_time_counters()


    def change_current_timer(self, clocks, last_counter, curr_counter):
        print(last_counter, curr_counter)
        if not isinstance(clocks[last_counter], int):
            clocks[last_counter].cancel()
        if not isinstance(clocks[curr_counter], int):
            clocks[curr_counter].cancel()

        clocks[last_counter] = 0
        clocks[curr_counter] = Clock.schedule_interval(partial(self.decrement_time, self.times, curr_counter), 0.1)
        self.increment_time(last_counter, self.increment_value)

    def update_current_time_counters(self):
        self.chessboard_widget.white_time_as_str_minutes = str(self.times[0] // 600) if len(str(self.times[0] // 600)) > 1 else str(0)+str(self.times[0] // 600)
        self.chessboard_widget.white_time_as_str_seconds = str(self.times[0] % 600 // 10) + ":" + str(self.times[0] % 10) if len(str(self.times[0] % 600 // 10)) > 1 else str(0)+str(self.times[0] % 600 // 10) + ":" + str(self.times[0] % 10)
        self.chessboard_widget.black_time_as_str_minutes = str(self.times[1] // 600) if len(str(self.times[1] // 600)) > 1 else str(0)+str(self.times[1] // 600)
        self.chessboard_widget.black_time_as_str_seconds = str(self.times[1] % 600 // 10) + ":" + str(self.times[1] % 10) if len(str(self.times[1] % 600 // 10)) > 1 else str(0)+str(self.times[1] % 600 // 10) + ":" + str(self.times[1] % 10)

    def handle_clock_change_after_promotion(self):

        if self.chessboard_widget.engine.current_player == "white":
            self.times[1] -= self.increment_value*10
            self.change_current_timer(self.clocks, 1, 0)
        else:
            self.times[0] -= self.increment_value*10
            self.change_current_timer(self.clocks, 0, 1)

    def switch_clocks(self):
        if isinstance(self.clocks[0], int):
            self.change_current_timer(self.clocks, 1, 0)
        else:
            self.change_current_timer(self.clocks, 0, 1)
import copy

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from backend import Engine as en
from backend import History as h
from backend import TimerManager as tm
import PromotionModal
import Cell


def game_status_switcher(status):
    return {
        "check": "Szach",
        "checkmate": "Szach-mat",
        "draw": "Remis"
    }.get(status, status)


class GameLayout(BoxLayout):
    chessboard_object = ObjectProperty()
    history_object = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_times_and_initiate(self, time_value_in_sec, increment_value):
        self.chessboard_object.initiate_configuration(time_value_in_sec, increment_value, self.history_object)


class ChessBoard(GridLayout):
    engine = en.Engine()
    history_widget = ObjectProperty()
    previous_states = h.History()
    timer_manager = tm.TimerManager()
    white_time_as_str_seconds = StringProperty()
    white_time_as_str_minutes = StringProperty()
    black_time_as_str_seconds = StringProperty()
    black_time_as_str_minutes = StringProperty()
    game_status = StringProperty()
    reversed = False
    paused = False
    finished = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.promotion_modal = PromotionModal.PromotionManager(self)
        self.timer_manager.set_chessboard_widget(self)

    def initiate_configuration(self, time_value_in_sec, increment_value, history_object):
        self.reversed = False
        self.paused = False
        self.finished = False
        self.timer_manager.set_clocks(time_value_in_sec, increment_value)
        self.history_widget = history_object
        self.history_widget.remove_all()
        self.engine = en.Engine()
        self.previous_states = h.History()
        self.store_chessboard_state()
        self.board_positions = self.engine.chessboard.board
        self.clear_widgets()
        self.fill_chessboard_initial()
        self.fill_chessboard()

    def reverse_chessboard(self):
        self.reversed = not self.reversed

    def fill_chessboard_initial(self):
        for x in range(8):
            for y in range(8):
                text_to_print = str(7 - x) + str(7 - y) if self.reversed else str(x) + str(y)
                lab = Cell.Cell(text_to_print, self, self.engine,
                                self.board_positions[7 - x][7 - y] if self.reversed else self.board_positions[x][y])

                self.add_widget(lab)
                self.ids[text_to_print] = lab

    def fill_chessboard(self):
        for x in range(8):
            for y in range(8):
                text_to_print = str(7 - x) + str(7 - y) if self.reversed else str(x) + str(y)
                self.ids[text_to_print].update_content(
                    self.board_positions[7 - x][7 - y] if self.reversed else self.board_positions[x][y])

        self.game_status = game_status_switcher(self.engine.state)
        if self.engine.state in ("checkmate", "draw"):
            self.finished = True
            self.paused = True

    def store_chessboard_state(self):
        self.previous_states.add_move(self.engine.chessboard, self.game_status)

    def restore_chessboard_state(self):
        if (self.previous_states.is_undo_possible()):
            self.finished = False
            chessboard_to_replace, status = self.previous_states.delete_move()
            self.engine.chessboard = copy.deepcopy(chessboard_to_replace)
            self.board_positions = self.engine.chessboard.board
            self.engine.state = status
            self.timer_manager.switch_clocks()
            self.engine.switch_players()
            self.history_widget.remove_last()
            self.engine.calculate_possible_moves()
            self.fill_chessboard()

    def update_chessboard(self):
        if self.engine.current_figure is None:
            if self.engine.current_player == "white":
                self.timer_manager.change_current_timer(self.timer_manager.clocks, 1, 0)
            else:
                self.timer_manager.change_current_timer(self.timer_manager.clocks, 0, 1)
        self.fill_chessboard()
        self.store_chessboard_state()

    def revert_chessboard(self):
        while self.children:
            for cell in self.children:
                self.remove_widget(cell)

        self.fill_chessboard_initial()

    def handle_promotion(self, response):
        if isinstance(response, list) and response[0] == "promotion":
            if self.engine.current_player == "black":
                self.timer_manager.change_current_timer(self.timer_manager.clocks, 1, 0)
            else:
                self.timer_manager.change_current_timer(self.timer_manager.clocks, 0, 1)

            self.promotion_modal.pop_up(response[1], response[2], response[3])

    def concede(self):
        self.finished = True
        self.game_status = "Biały wygrał!" if self.engine.current_player == "black" else "Czarny wygrał!"

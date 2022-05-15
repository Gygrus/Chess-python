from kivy.graphics import Rectangle, Color, Ellipse
from kivy.properties import StringProperty
from kivy.uix.label import Label
from backend import Vector as v
from backend import Figure as f
import chessboard_demo as cd

class Cell(Label):
    cell_id = StringProperty()
    img_source = StringProperty()


    def __init__(self, cell_id, chessboard, engine, figure, **kwargs):
        super().__init__(**kwargs)
        self.cell_id = cell_id
        self.text = ""
        self.engine = engine
        self.chessboard = chessboard
        self.num_mode = ((int(cell_id[0]) + int(cell_id[1])) % 2) / 1
        self.img_source = figure.image
        self.figure = figure
        self.board_representation = figure.image
        self.position = v.Vector(int(self.cell_id[0]), int(self.cell_id[1]))

        with self.canvas.before:
            self.create_rect()

            if isinstance(self.engine.current_figure, f.Figure) and self.engine.current_figure.check_if_in_moves(
                    self.position):
                self.create_circ()


    def update_content(self, figure):
        self.img_source = figure.image
        self.figure = figure
        self.board_representation = figure.image
        with self.canvas.before:
            if isinstance(self.engine.current_figure, f.Figure) and self.engine.current_figure.check_if_in_moves(
                    self.position):
                self.create_circ()

            else:
                self.canvas.before.clear()
                self.create_rect()

    def create_rect(self):
        Color(self.num_mode / 2 + 1 / 8, self.num_mode / 4 + 1 / 5, self.num_mode / 3, 1)
        self.rect = Rectangle(pos=self.pos,
                              size=(self.width,
                                    self.height))

        self.bind(pos=self.update_rect,
                  size=self.update_rect)

    def create_circ(self):
        Color(0, 0, 0, 0.2)
        self.circ = Ellipse(angle_start=0,
                            angle_end=360,
                            pos=self.pos,
                            size=(self.width,
                                  self.height), )

        self.bind(pos=self.update_circ,
                  size=self.update_circ)

    def clean_up(self):
        self.rect = None
        self.circ = None


    def update_circ(self, *args):
        self.circ.pos = self.pos
        self.circ.size = self.size

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not self.chessboard.paused:
            self.touch_handler()

            return True

    def touch_handler(self):

        if self.engine.chessboard.is_figure(self.position) and \
                not isinstance(self.engine.current_figure, f.Figure) and self.figure.color == self.engine.current_player and \
                self.figure is not self.engine.current_figure:
            self.engine.choose_figure(self.position)
            # self.chessboard.update_chessboard()
            self.chessboard.fill_chessboard()
        elif self.figure is self.engine.current_figure:
            self.engine.current_figure = None
            self.chessboard.fill_chessboard()
        elif isinstance(self.engine.current_figure, f.Figure):
            response = self.engine.move_to_position(self.position)
            if response:
                self.chessboard.update_chessboard()
                self.chessboard.history_widget.display_move_on_history_tab(self.engine.game_record[-1][0],
                                                                           self.engine.current_player)
            else:
                self.chessboard.fill_chessboard()
            self.chessboard.handle_promotion(response)

        else:
            self.engine.current_figure = None

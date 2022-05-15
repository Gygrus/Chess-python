from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ObjectProperty
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

class PromotionModal(Popup):
    text = StringProperty()
    manager = ObjectProperty()
    frontend_chessboard = ObjectProperty()

    rook_img = StringProperty()
    queen_img = StringProperty()
    bishop_img = StringProperty()
    knight_img = StringProperty()

    def __init__(self, manager, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.manager = manager

        if self.text == "white":
            self.rook_img = "./assets/rw.png"
            self.queen_img = "./assets/qw.png"
            self.bishop_img = "./assets/bw.png"
            self.knight_img = "./assets/kw.png"
        else:
            self.rook_img = "./assets/rb.png"
            self.queen_img = "./assets/qb.png"
            self.bishop_img = "./assets/bb.png"
            self.knight_img = "./assets/kb.png"

    def submit_promotion(self, type):
        self.manager.forward_submission(type)
        self.dismiss()
        return True



class PromotionManager():
    engine = None
    element = None
    position = None

    def __init__(self, frontend_chessboard):
        self.frontend_chessboard = frontend_chessboard


    def pop_up(self, player, element, position):
        self.element = element
        self.position = position
        self.engine = self.frontend_chessboard.engine
        modal = PromotionModal(self, player)
        modal.open()

    def forward_submission(self, type):
        self.engine.test_promotion(type, self.element, self.position)
        self.frontend_chessboard.previous_states.hist.pop()
        self.frontend_chessboard.store_chessboard_state()
        self.frontend_chessboard.fill_chessboard()
        self.frontend_chessboard.timer_manager.handle_clock_change_after_promotion()



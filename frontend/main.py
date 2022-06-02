from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from ctypes import windll, c_int64
windll.user32.SetProcessDpiAwarenessContext(c_int64(-4))

from frontend import ChessboardLayout as cbd
from frontend import HistoryView as hv
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.button import Button


class HoverButton(Button):

    def __init__(self, *args, **kwargs):
        super(HoverButton, self).__init__(*args, **kwargs)
        Window.bind(mouse_pos=self.pos_check)

    def pos_check(self, inst, pos):
        if self.collide_point(*pos):
             self.background_color = (0, 0, 1, 1)
        else:
             self.background_color = (.52, .43, .57, 1)


class MainMenu(Screen):

    def quit_application(self):
        App.get_running_app().stop()
        Window.close()
    pass

class ChessBoardView(Screen):
    game_layout_object = ObjectProperty()

    def init_chess_game(self, time_value_in_sec, increment_value):
        self.game_layout_object.set_times_and_initiate(time_value_in_sec, increment_value)

class Options(Screen):
    pass

class WindowManager(ScreenManager):
    pass


Builder.load_file("frontend/HistoryView.kv")
Builder.load_file("frontend/Chessboard.kv")
Builder.load_file("frontend/GameConfig.kv")
Builder.load_file("frontend/PromotionModal.kv")

kv = Builder.load_file("frontend/Screens.kv")


class MyMainApp(App):
    def build(self):
        return kv

def run_app():
    Window.fullscreen = 'auto'
    MyMainApp().run()

if __name__ == "__main__":
    Window.fullscreen = 'auto'
    MyMainApp().run()
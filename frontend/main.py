from kivy.config import Config
# Config.set('graphics', 'resizable', False)


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget

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

class Options(Screen):
    pass

class WindowManager(ScreenManager):
    pass


Builder.load_file("config-panel.kv")
kv = Builder.load_file("options.kv")


class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    # Window.fullscreen = 'auto'
    MyMainApp().run()
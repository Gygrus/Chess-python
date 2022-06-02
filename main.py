from frontend import run_app
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from ctypes import windll, c_int64
windll.user32.SetProcessDpiAwarenessContext(c_int64(-4))


if __name__ == '__main__':
    run_app()



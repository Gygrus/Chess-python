from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color

class HistoryItem(Label):
    def __init__(self, content, color, **kwargs):
        super().__init__(**kwargs)
        self.text = content
        self.size_hint_y = None
        self.height = 40

        with self.canvas.before:
            if color == "white":
                Color(0, 0, 0, 0.10)
            else:
                Color(1, 1, 1, 0.10)
            self.rect = Rectangle(pos=self.pos,
                                  size=(self.width,
                                        self.height))

            self.bind(pos=self.update_rect,
                      size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class HistoryView(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def display_move_on_history_tab(self, content, color):
        move_to_append = HistoryItem(content, color)
        self.children[0].add_widget(move_to_append)

    def remove_last(self):
        self.children[0].remove_widget(self.children[0].children[0])

    def remove_all(self):
        self.children[0].clear_widgets()

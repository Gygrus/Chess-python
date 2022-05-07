from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label


class HistoryView(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def display_move_on_history_tab(self, content):
        move_to_append = Label(text = content,
                               size_hint_y = None)

        self.children[0].add_widget(move_to_append)
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineIconListItem, IconRightWidget
from kivymd.uix.button import MDRaisedButton

from backend.reflection import get_all_reflections, delete_reflection


class SavedThoughtsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)

        title = MDLabel(text="Saved Thoughts", halign="center", font_style="H5")
        self.layout.add_widget(title)

        self.scroll = MDScrollView()
        self.list_container = MDList()
        self.scroll.add_widget(self.list_container)
        self.layout.add_widget(self.scroll)

        back_btn = MDRaisedButton(text="Back", pos_hint={"center_x": 0.5}, on_release=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.load_thoughts()

    def load_thoughts(self):
        self.list_container.clear_widgets()
        thoughts = get_all_reflections()
        if thoughts:
            for text, timestamp in thoughts:
                item = OneLineIconListItem(text=text)
                delete_btn = IconRightWidget(icon="delete", on_release=lambda x, t=text: self.delete_thought(t))
                item.add_widget(delete_btn)
                self.list_container.add_widget(item)
        else:
            self.list_container.add_widget(MDLabel(text="No saved thoughts found.", halign="center"))

    def delete_thought(self, thought_text):
        delete_reflection(thought_text)
        self.load_thoughts()

    def go_back(self, instance):
        self.manager.current = "home"

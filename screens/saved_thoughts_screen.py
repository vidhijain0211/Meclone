from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconRightWidget, IconLeftWidget
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from backend.reflection import get_all_reflections, delete_reflection
from backend.session_manager import SessionManager
from functools import partial
from kivymd.uix.card import MDCard

class SavedThoughtsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.build_ui()

    def build_ui(self):
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)

        title_card = MDCard(
            orientation='vertical',
            padding=18,
            size_hint_y=None,
            radius=[20, 20, 20, 20],
        )
        title = MDLabel(text="Saved Thoughts", halign="center", font_style="H5")
        title_card.add_widget(title)
        self.layout.add_widget(title_card)

        self.scroll = MDScrollView()
        self.list_container = MDList()
        self.scroll.add_widget(self.list_container)
        self.layout.add_widget(self.scroll)

        back_card = MDCard(
            orientation='vertical',
            padding=12,
            size_hint_y=None,
            radius=[12, 12, 12, 12],
        )
        back_btn = MDRaisedButton(text="Back", pos_hint={"center_x": 0.5}, on_release=self.go_back)
        back_card.add_widget(back_btn)
        self.layout.add_widget(back_card)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.load_thoughts()

    def load_thoughts(self):
        self.list_container.clear_widgets()
        user_id = SessionManager().get_logged_in_user()
        thoughts = get_all_reflections(user_id)
        if thoughts:
            for text, timestamp in thoughts:
                item = OneLineAvatarIconListItem(text=text)
                left_icon = IconLeftWidget(icon="bookmark-outline")
                item.add_widget(left_icon)
                delete_btn = IconRightWidget(icon="delete")
                delete_btn.on_release = partial(self.delete_thought, text)
                item.add_widget(delete_btn)
                self.list_container.add_widget(item)
        else:
            self.list_container.add_widget(MDLabel(text="No saved thoughts found.", halign="center"))

    def delete_thought(self, thought_text, *args):
        user_id = SessionManager().get_logged_in_user()
        delete_reflection(thought_text, user_id)
        self.load_thoughts()

    def go_back(self, instance):
        self.manager.current = "home"
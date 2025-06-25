from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from backend.auth import register_user
from kivymd.toast import toast
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView

class RegisterScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        from kivymd.uix.boxlayout import MDBoxLayout
        self.clear_widgets()
        scroll = MDScrollView()
        layout = MDBoxLayout(orientation='vertical', padding=[24, 40, 24, 24], spacing=24, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        self.username_input = MDTextField(hint_text="Create Username", size_hint_y=None, height=48)
        self.password_input = MDTextField(hint_text="Create Password", password=True, size_hint_y=None, height=48)
        register_btn = MDRaisedButton(text="Create Account", on_release=self.register, size_hint_y=None, height=48)
        back_btn = MDRaisedButton(text="Back to Login", on_release=lambda x: setattr(self.manager, "current", "login"), size_hint_y=None, height=48)
        card = MDCard(orientation='vertical', padding=24, spacing=18, size_hint=(1, None), height=280, radius=[20, 20, 20, 20])
        card.add_widget(MDLabel(text="Register", halign="center", font_style="H4", size_hint_y=None, height=40))
        card.add_widget(self.username_input)
        card.add_widget(self.password_input)
        card.add_widget(register_btn)
        card.add_widget(back_btn)
        layout.add_widget(card)
        scroll.add_widget(layout)
        self.add_widget(scroll)

    def register(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        toast("Registered Successfully! Please Login.")

        if register_user(username, password):
            self.manager.current = "login"
            
    def on_pre_enter(self):
        self.build_ui()

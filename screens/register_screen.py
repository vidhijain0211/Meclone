from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from backend.auth import register_user
from kivymd.toast import toast

class RegisterScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        from kivymd.uix.boxlayout import MDBoxLayout

        layout = MDBoxLayout(orientation='vertical', padding=50, spacing=20)

        self.username_input = MDTextField(hint_text="New Username")
        self.password_input = MDTextField(hint_text="New Password", password=True)
        register_btn = MDRaisedButton(text="Register", on_release=self.register)
        back_btn = MDRaisedButton(text="Back to Login", on_release=lambda x: setattr(self.manager, "current", "login"))

        layout.add_widget(MDLabel(text="Register", halign="center", font_style="H4"))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(register_btn)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def register(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        toast("Registered Successfully! Please Login.")

        if register_user(username, password):
            self.manager.current = "login"

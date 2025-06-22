from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from backend.auth import login_user
from kivymd.uix.button import MDFlatButton
from backend.session_manager import SessionManager

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = SessionManager()
        self.build_ui()

    def build_ui(self):
        from kivymd.uix.boxlayout import MDBoxLayout

        layout = MDBoxLayout(orientation='vertical', padding=50, spacing=20)

        self.username_input = MDTextField(hint_text="Username")
        self.password_input = MDTextField(hint_text="Password", password=True)
        login_btn = MDRaisedButton(text="Login", on_release=self.login) 
        back_btn = MDFlatButton(text="Back", on_release=lambda x: setattr(self.manager,"current" , "entry"))
       

        layout.add_widget(MDLabel(text="Login", halign="center", font_style="H4"))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_btn)
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        user_id = login_user(username, password)

        if user_id:
            self.session.set_logged_in_user(user_id)

            # ✅ Check if "home" screen is already added or not
            if not self.manager.has_screen("home"):
                from screens.home_screen import HomeScreen
                self.manager.add_widget(HomeScreen(name="home"))

            # If app lock is enabled for this user, go to lock screen first
            if self.session.is_app_lock_enabled():
                self.manager.current = "lock"
            else:
                self.manager.current = "home"
        else:
            from kivymd.toast import toast
            toast("Invalid username or password")


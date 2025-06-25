from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from backend.auth import login_user, get_security_question, validate_security_answer, update_password
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from backend.session_manager import SessionManager

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = SessionManager()
        self.dialog = None
        self.build_ui()

    def build_ui(self):
        from kivymd.uix.boxlayout import MDBoxLayout

        layout = MDBoxLayout(orientation='vertical', padding=50, spacing=20)

        self.username_input = MDTextField(hint_text="Username")
        self.password_input = MDTextField(hint_text="Password", password=True)
        login_btn = MDRaisedButton(text="Login", on_release=self.login) 
        back_btn = MDFlatButton(text="Back", on_release=lambda x: setattr(self.manager,"current" , "entry"))
        forgot_btn = MDFlatButton(text="Forgot Password?", on_release=self.forgot_password)

        layout.add_widget(MDLabel(text="Login", halign="center", font_style="H4"))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_btn)
        layout.add_widget(forgot_btn)
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

    def forgot_password(self, instance):
        # Ask for username first
        username_field = MDTextField(hint_text="Enter your username")
        def ask_question(dialog, field):
            username = field.text.strip()
            question = get_security_question(username)
            if not question:
                self.show_dialog("No security question set for this user.")
                return
            self.dialog.dismiss()
            self.ask_security_answer(username, question)
        self.dialog = MDDialog(
            title="Forgot Password",
            type="custom",
            content_cls=username_field,
            buttons=[MDRaisedButton(text="Next", on_release=lambda x: ask_question(self.dialog, username_field))]
        )
        self.dialog.open()

    def ask_security_answer(self, username, question):
        answer_field = MDTextField(hint_text="Answer", password=True)
        def check_answer(dialog, field):
            answer = field.text.strip()
            if validate_security_answer(username, answer):
                self.dialog.dismiss()
                self.show_reset_password_dialog(username)
            else:
                self.show_dialog("Incorrect answer.")
        self.dialog = MDDialog(
            title="Security Question",
            text=question,
            type="custom",
            content_cls=answer_field,
            buttons=[MDRaisedButton(text="Submit", on_release=lambda x: check_answer(self.dialog, answer_field))]
        )
        self.dialog.open()

    def show_reset_password_dialog(self, username):
        new_pass_field = MDTextField(hint_text="New Password", password=True)
        def do_reset(dialog, field):
            new_pass = field.text.strip()
            if new_pass:
                update_password(username, "", new_pass)
                self.dialog.dismiss()
                self.show_dialog("Password reset successfully.")
            else:
                self.show_dialog("Enter a new password.")
        self.dialog = MDDialog(
            title="Reset Password",
            type="custom",
            content_cls=new_pass_field,
            buttons=[MDRaisedButton(text="Reset", on_release=lambda x: do_reset(self.dialog, new_pass_field))]
        )
        self.dialog.open()

    def show_dialog(self, message):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            text=message,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()


from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton 
from backend.session_manager import SessionManager
from kivymd.toast import toast
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton

class AppLockScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = SessionManager()
        self.build_ui()

    def build_ui(self):
        from kivymd.uix.boxlayout import MDBoxLayout
        layout = MDBoxLayout(
            orientation='vertical',
            padding=40,
            spacing=20,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.8, None),
            height="200dp"
        )
        # App Lock UI

        self.code_input = MDTextField(hint_text="Enter App Lock Code", password=True)
        unlock_btn = MDRaisedButton (text="Unlock", on_release=self.unlock)
        reset_btn = MDFlatButton(text="Forgot Code?", on_release=self.reset_code)

        layout.add_widget(MDLabel(
            text="Enter App Lock Code",
            halign="center",
            font_style="H5",
            theme_text_color="Primary"
        ))
        layout.add_widget(self.code_input)
        layout.add_widget(unlock_btn)
        self.add_widget(layout)
        layout.add_widget(reset_btn)


    def unlock(self, instance):
        entered_code = self.code_input.text.strip()
        if self.session.validate_app_lock(entered_code):
            self.session.unlock()
            toast("Unlocked Successfully!")
            self.manager.current = "login"
        else:
            toast("Incorrect Code. Try again.")

    def reset_code(self, instance):
        from backend.session_manager import SessionManager
        self.session.reset_app_lock()
        toast("App Lock Code has been reset. Please set a new code.")
        self.manager.current = "login"  

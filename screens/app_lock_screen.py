from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton 
from backend.session_manager import SessionManager
from kivymd.toast import toast
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView

class AppLockScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = SessionManager()
        self.mode = "lock"  # default mode is lock (for app start)
        self.build_ui()

    def build_ui(self):
        from kivymd.uix.boxlayout import MDBoxLayout
        self.clear_widgets()
        scroll = MDScrollView()
        layout = MDBoxLayout(
            orientation='vertical',
            padding=[24, 40, 24, 24],  # uniform padding
            spacing=24,
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter('height'))
        self.layout = layout
        if self.mode == "lock":
            if self.session.is_app_lock_enabled():
                card = MDCard(orientation='vertical', padding=24, spacing=18, size_hint=(1, None), height=260, radius=[20, 20, 20, 20], pos_hint={"center_x": 0.5})
                self.code_input = MDTextField(hint_text="Enter App Lock Code", password=True, size_hint_y=None, height=48)
                unlock_btn = MDRaisedButton(text="Unlock", on_release=self.unlock, size_hint_y=None, height=48)
                reset_btn = MDFlatButton(text="Forgot Code?", on_release=self.show_forgot_lock_ui, size_hint_y=None, height=36)
                card.add_widget(MDLabel(
                    text="Enter App Lock Code",
                    halign="center",
                    font_style="H5",
                    theme_text_color="Primary",
                    size_hint_y=None,
                    height=40
                ))
                card.add_widget(self.code_input)
                card.add_widget(unlock_btn)
                card.add_widget(reset_btn)
                layout.add_widget(card)
            else:
                card = MDCard(orientation='vertical', padding=24, spacing=18, size_hint=(1, None), height=180, radius=[20, 20, 20, 20], pos_hint={"center_x": 0.5})
                card.add_widget(MDLabel(
                    text="App Lock is Disabled",
                    halign="center",
                    font_style="H5",
                    theme_text_color="Primary",
                    size_hint_y=None,
                    height=40
                ))
                enable_btn = MDRaisedButton(text="Enable App Lock", on_release=self.show_set_lock_ui, size_hint_y=None, height=48)
                card.add_widget(enable_btn)
                layout.add_widget(card)
        elif self.mode == "settings":
            card = MDCard(orientation='vertical', padding=24, spacing=18, size_hint=(1, None), height=320, radius=[20, 20, 20, 20], pos_hint={"center_x": 0.5})
            if self.session.is_app_lock_enabled():
                update_btn = MDRaisedButton(text="Update App Lock Code", on_release=self.show_update_lock_ui, size_hint_y=None, height=48)
                disable_btn = MDRaisedButton(text="Disable App Lock", on_release=self.show_disable_lock_ui, size_hint_y=None, height=48)
                reset_btn = MDRaisedButton(text="Forgot Code?", on_release=self.show_forgot_lock_ui, size_hint_y=None, height=48)
                back_btn = MDRaisedButton(text="Back", on_release=self.go_back, size_hint_y=None, height=48)
                card.add_widget(MDLabel(
                    text="App Lock Settings",
                    halign="center",
                    font_style="H5",
                    theme_text_color="Primary",
                    size_hint_y=None,
                    height=40
                ))
                card.add_widget(update_btn)
                card.add_widget(disable_btn)
                card.add_widget(reset_btn)
                card.add_widget(back_btn)
            else:
                enable_btn = MDRaisedButton(text="Enable App Lock", on_release=self.show_set_lock_ui, size_hint_y=None, height=48)
                back_btn = MDRaisedButton(text="Back", on_release=self.go_back, size_hint_y=None, height=48)
                card.add_widget(MDLabel(
                    text="App Lock is Disabled",
                    halign="center",
                    font_style="H5",
                    theme_text_color="Primary",
                    size_hint_y=None,
                    height=40
                ))
                card.add_widget(enable_btn)
                card.add_widget(back_btn)
            layout.add_widget(card)
        scroll.add_widget(layout)
        self.add_widget(scroll)

    def on_pre_enter(self):
        self.build_ui()

    def open_settings_mode(self):
        self.mode = "settings"
        self.build_ui()

    def open_lock_mode(self):
        self.mode = "lock"
        self.build_ui()

    def disable_app_lock(self, instance):
        self.session.disable_app_lock()
        toast("App Lock Disabled!")
        self.build_ui()

    def enter_settings_mode(self):
        self.settings_mode = True
        self.build_ui()

    def exit_settings_mode(self):
        self.settings_mode = False
        self.build_ui()

    def show_set_lock_ui(self, instance):
        self.layout.clear_widgets()
        self.new_code_input = MDTextField(hint_text="Set New App Lock Code", password=True)
        # Only show security question if not already set
        if not self.session.get_security_question():
            self.security_question_input = MDTextField(hint_text="Set Security Question")
            self.security_answer_input = MDTextField(hint_text="Set Security Answer")
        else:
            self.security_question_input = None
            self.security_answer_input = None
        confirm_btn = MDRaisedButton(text="Set App Lock", on_release=self.set_new_lock)
        back_btn = MDRaisedButton(text="Back", on_release=lambda x: self.build_ui())
        self.layout.add_widget(MDLabel(
            text="Create App Lock Code",
            halign="center",
            font_style="H5",
            theme_text_color="Primary"
        ))
        self.layout.add_widget(self.new_code_input)
        if self.security_question_input:
            self.layout.add_widget(self.security_question_input)
        if self.security_answer_input:
            self.layout.add_widget(self.security_answer_input)
        self.layout.add_widget(confirm_btn)
        self.layout.add_widget(back_btn)

    def set_new_lock(self, instance):
        code = self.new_code_input.text.strip()
        if self.security_question_input and self.security_answer_input:
            question = self.security_question_input.text.strip()
            answer = self.security_answer_input.text.strip()
        else:
            question = self.session.get_security_question()
            answer = None
        if code and (question or not self.security_question_input):
            if self.security_question_input and self.security_answer_input:
                self.session.set_app_lock("pin", code, str(question), str(answer))
            else:
                self.session.set_app_lock("pin", code)
            toast("App Lock Enabled!")
            self.build_ui()
        else:
            toast("Please fill all fields.")

    def show_disable_lock_ui(self, instance):
        self.layout.clear_widgets()
        self.disable_code_input = MDTextField(hint_text="Enter App Lock Code to Disable", password=True)
        confirm_btn = MDRaisedButton(text="Disable App Lock", on_release=self.disable_app_lock_with_code)
        back_btn = MDRaisedButton(text="Back", on_release=lambda x: self.build_ui())
        self.layout.add_widget(MDLabel(
            text="Disable App Lock",
            halign="center",
            font_style="H5",
            theme_text_color="Primary"
        ))
        self.layout.add_widget(self.disable_code_input)
        self.layout.add_widget(confirm_btn)
        self.layout.add_widget(back_btn)

    def disable_app_lock_with_code(self, instance):
        code = self.disable_code_input.text.strip()
        if self.session.validate_app_lock(code):
            self.session.disable_app_lock()
            toast("App Lock Disabled!")
            self.build_ui()
        else:
            toast("Incorrect Code.")

    def show_forgot_lock_ui(self, instance):
        self.layout.clear_widgets()
        question = self.session.get_security_question()
        self.security_answer_input = MDTextField(hint_text="Enter Security Answer")
        confirm_btn = MDRaisedButton(text="Reset App Lock", on_release=self.reset_app_lock_with_answer)
        back_btn = MDRaisedButton(text="Back", on_release=lambda x: self.build_ui())
        self.layout.add_widget(MDLabel(
            text=f"Security Question: {question}",
            halign="center",
            font_style="H6",
            theme_text_color="Primary"
        ))
        self.layout.add_widget(self.security_answer_input)
        self.layout.add_widget(confirm_btn)
        self.layout.add_widget(back_btn)

    def reset_app_lock_with_answer(self, instance):
        answer = self.security_answer_input.text.strip()
        if self.session.validate_security_answer(answer):
            self.show_set_lock_ui(instance)
            toast("Correct answer! Set a new app lock.")
        else:
            toast("Incorrect answer.")

    def show_update_lock_ui(self, instance):
        self.layout.clear_widgets()
        self.old_code_input = MDTextField(hint_text="Enter Old App Lock Code", password=True)
        self.new_code_input = MDTextField(hint_text="Enter New App Lock Code", password=True)
        confirm_btn = MDRaisedButton(text="Update App Lock", on_release=self.update_app_lock)
        back_btn = MDRaisedButton(text="Back", on_release=lambda x: self.build_ui())
        self.layout.add_widget(MDLabel(
            text="Update App Lock",
            halign="center",
            font_style="H5",
            theme_text_color="Primary"
        ))
        self.layout.add_widget(self.old_code_input)
        self.layout.add_widget(self.new_code_input)
        self.layout.add_widget(confirm_btn)
        self.layout.add_widget(back_btn)

    def update_app_lock(self, instance):
        old_code = self.old_code_input.text.strip()
        new_code = self.new_code_input.text.strip()
        if old_code and new_code:
            if self.session.update_app_lock(old_code, new_code):
                toast("App Lock Updated!")
                self.build_ui()
            else:
                toast("Old code incorrect.")
        else:
            toast("Please fill all fields.")

    def unlock(self, instance):
        entered_code = self.code_input.text.strip()
        if self.session.validate_app_lock(entered_code):
            self.session.unlock()
            toast("Unlocked Successfully!")
            # Only go to home if user is logged in, otherwise go to login
            if self.session.is_logged_in():
                self.manager.current = "home"
            else:
                # If not logged in, skip app lock and go to login
                self.manager.current = "login"
                
        else:
            toast("Incorrect Code. Try again.")

    def reset_code(self, instance):
        from backend.session_manager import SessionManager
        self.session.reset_app_lock()
        toast("App Lock Code has been reset. Please set a new code.")
        self.manager.current = "login"

    def go_back(self, instance):
        self.manager.current = "home"

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivymd.uix.card import MDCard
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.scrollview import MDScrollView
from backend.session_manager import SessionManager
from backend.auth import (
    update_password, update_username, save_user_info, load_user_info, delete_user_account,
    set_security_question, get_security_question, validate_security_answer
)

class ProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = SessionManager()
        self.dialog = None
        self.state = "main"  # main, info, update, update_username, update_password
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        scroll = MDScrollView()
        self.layout = MDBoxLayout(orientation='vertical', padding=[24, 32, 24, 24], spacing=16, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        if self.state == "main":
            self.layout.add_widget(Widget(size_hint_y=None, height=40))
            self.layout.add_widget(MDLabel(text="Profile", font_style="H4", halign="center", size_hint_y=None, height=48))
            info_btn = MDRaisedButton(text="User Information", pos_hint={"center_x": 0.5}, size_hint=(None, None), width=220, on_release=self.show_info)
            update_btn = MDRaisedButton(text="Update Username & Password", pos_hint={"center_x": 0.5}, size_hint=(None, None), width=220, on_release=self.show_update)
            back_btn = MDRaisedButton(text="Back", pos_hint={"center_x": 0.5}, size_hint=(None, None), width=220, on_release=self.go_back)
            self.layout.add_widget(info_btn)
            self.layout.add_widget(update_btn)
            self.layout.add_widget(back_btn)
        elif self.state == "info":
            # Profile Photo Card
            photo_card = MDCard(orientation='vertical', padding=16, spacing=10, size_hint_y=None)
            photo_card.bind(minimum_height=photo_card.setter('height'))
            photo_card.add_widget(MDLabel(text="Profile Photo", font_style="H6", halign="center", size_hint_y=None, height=32))
            photo_box = MDBoxLayout(orientation='vertical', size_hint_y=None, height=160, spacing=8)
            self.profile_img = Image(source="assets/default_profile.png", size_hint=(None, None), size=(120, 120), allow_stretch=True)
            self.profile_img_circle = MDCard(
                size_hint=(None, None),
                size=(130, 130),
                radius=[65, 65, 65, 65],
                pos_hint={"center_x": 0.5},
                padding=0
            )
            self.profile_img_circle.add_widget(self.profile_img)
            photo_box.add_widget(Widget(size_hint_y=None, height=8))
            photo_box.add_widget(self.profile_img_circle)
            change_photo_btn = MDRaisedButton(text="Update Profile Photo", pos_hint={"center_x": 0.5}, size_hint=(None, None), width=180, on_release=self.open_file_chooser)
            remove_photo_btn = MDRaisedButton(text="Remove Profile Photo", pos_hint={"center_x": 0.5}, size_hint=(None, None), width=180, on_release=self.remove_profile_photo)
            photo_box.add_widget(change_photo_btn)
            photo_box.add_widget(remove_photo_btn)
            photo_card.add_widget(photo_box)
            self.layout.add_widget(photo_card)
            self.layout.add_widget(Widget(size_hint_y=None, height=8))
            # Info Card
            info_card = MDCard(orientation='vertical', padding=16, spacing=10, size_hint_y=None)
            info_card.bind(minimum_height=info_card.setter('height'))
            info_card.add_widget(MDLabel(text="Personal Information", font_style="H6", halign="center", size_hint_y=None, height=32))
            self.name_input = MDTextField(hint_text="Full Name", size_hint_y=None, height=48)
            self.age_input = MDTextField(hint_text="Age", input_filter="int", size_hint_y=None, height=48)
            self.country_input = MDTextField(hint_text="Country", size_hint_y=None, height=48)
            self.language_input = MDTextField(hint_text="Language", size_hint_y=None, height=48)
            save_info_btn = MDRaisedButton(text="Save Info", pos_hint={"center_x": 0.5}, size_hint=(None, None), width=180, on_release=self.save_info)
            info_card.add_widget(self.name_input)
            info_card.add_widget(self.age_input)
            info_card.add_widget(self.country_input)
            info_card.add_widget(self.language_input)
            info_card.add_widget(save_info_btn)
            self.layout.add_widget(info_card)
            self.layout.add_widget(Widget(size_hint_y=None, height=8))
            # Security Question Card
            secq_card = MDCard(orientation='vertical', padding=16, spacing=10, size_hint_y=None)
            secq_card.bind(minimum_height=secq_card.setter('height'))
            secq_card.add_widget(MDLabel(text="Security Question", font_style="H6", halign="center", size_hint_y=None, height=32))
            self.security_question_input = MDTextField(hint_text="Security Question", size_hint_y=None, height=48)
            self.security_answer_input = MDTextField(hint_text="Security Answer", password=True, size_hint_y=None, height=48)
            set_secq_btn = MDRaisedButton(text="Set/Update Security Question", pos_hint={"center_x": 0.5}, size_hint=(None, None), width=220, on_release=self.set_security_question)
            secq_card.add_widget(self.security_question_input)
            secq_card.add_widget(self.security_answer_input)
            secq_card.add_widget(set_secq_btn)
            self.layout.add_widget(secq_card)
            self.layout.add_widget(Widget(size_hint_y=None, height=8))
            back_btn = MDRaisedButton(text="Back", pos_hint={"center_x": 0.5}, size_hint=(None, None), width=180, on_release=self.show_main)
            self.layout.add_widget(back_btn)
        elif self.state == "update":
            self.layout.add_widget(MDLabel(text="Update Username & Password", font_style="H5", halign="center", size_hint_y=None, height=48))
            username_btn = MDRaisedButton(text="Update Username", pos_hint={"center_x": 0.5}, size_hint=(None, None), width=220, on_release=self.show_update_username)
            password_btn = MDRaisedButton(text="Update Password", pos_hint={"center_x": 0.5}, size_hint=(None, None), width=220, on_release=self.show_update_password)
            back_btn = MDRaisedButton(text="Back", pos_hint={"center_x": 0.5}, size_hint=(None, None), width=220, on_release=self.show_main)
            self.layout.add_widget(username_btn)
            self.layout.add_widget(password_btn)
            self.layout.add_widget(back_btn)
        elif self.state == "update_username":
            self.layout.add_widget(MDLabel(text="Update Username", font_style="H6", halign="center", size_hint_y=None, height=32))
            self.old_username_input = MDTextField(hint_text="Old Username", size_hint_y=None, height=48)
            self.new_username_input = MDTextField(hint_text="New Username", size_hint_y=None, height=48)
            change_username_btn = MDRaisedButton(text="Update Username", pos_hint={"center_x": 0.5}, size_hint=(None, None), width=180, on_release=self.change_username)
            back_btn = MDRaisedButton(text="Back", pos_hint={"center_x": 0.5}, size_hint=(None, None), width=180, on_release=self.show_update)
            self.layout.add_widget(self.old_username_input)
            self.layout.add_widget(self.new_username_input)
            self.layout.add_widget(change_username_btn)
            self.layout.add_widget(back_btn)
        elif self.state == "update_password":
            self.layout.add_widget(MDLabel(text="Update Password", font_style="H6", halign="center", size_hint_y=None, height=32))
            self.old_pass_input = MDTextField(hint_text="Old Password", password=True, size_hint_y=None, height=48)
            self.new_pass_input = MDTextField(hint_text="New Password", password=True, size_hint_y=None, height=48)
            change_pass_btn = MDRaisedButton(text="Update Password", pos_hint={"center_x": 0.5}, size_hint=(None, None), width=180, on_release=self.update_password)
            forgot_pass_btn = MDFlatButton(text="Forgot Password?", pos_hint={"center_x": 0.5}, on_release=self.forgot_password)
            back_btn = MDRaisedButton(text="Back", pos_hint={"center_x": 0.5}, size_hint=(None, None), width=180, on_release=self.show_update)
            self.layout.add_widget(self.old_pass_input)
            self.layout.add_widget(self.new_pass_input)
            self.layout.add_widget(change_pass_btn)
            self.layout.add_widget(forgot_pass_btn)
            self.layout.add_widget(back_btn)
        scroll.add_widget(self.layout)
        self.add_widget(scroll)

    def show_main(self, *args):
        self.state = "main"
        self.build_ui()

    def show_info(self, *args):
        self.state = "info"
        self.build_ui()
        # Load user info after widgets are created
        user = self.session.get_logged_in_user()
        if user:
            info = load_user_info(user)
            self.name_input.text = info.get("name", "")
            self.age_input.text = info.get("age", "")
            self.country_input.text = info.get("country", "")
            self.language_input.text = info.get("language", "")
            img_path = info.get("image")
            if img_path:
                self.profile_img.source = img_path
            self.security_question_input.text = info.get("security_question", "")
            self.security_answer_input.text = info.get("security_answer", "")

    def show_update(self, *args):
        self.state = "update"
        self.build_ui()

    def show_update_username(self, *args):
        self.state = "update_username"
        self.build_ui()

    def show_update_password(self, *args):
        self.state = "update_password"
        self.build_ui()

    def on_pre_enter(self):
        # Only update info if in 'info' state and widgets exist
        if getattr(self, 'state', None) == "info" and hasattr(self, 'name_input'):
            user = self.session.get_logged_in_user()
            if user:
                info = load_user_info(user)
                self.name_input.text = info.get("name", "")
                self.age_input.text = info.get("age", "")
                self.country_input.text = info.get("country", "")
                self.language_input.text = info.get("language", "")
                img_path = info.get("image")
                if img_path:
                    self.profile_img.source = img_path
                self.security_question_input.text = info.get("security_question", "")
                self.security_answer_input.text = info.get("security_answer", "")

    def save_info(self, instance):
        name = self.name_input.text.strip()
        age = self.age_input.text.strip()
        country = self.country_input.text.strip()
        language = self.language_input.text.strip()
        user = self.session.get_logged_in_user()
        if not all([name, age, country, language]):
            self.show_dialog("All fields must be filled.")
            return
        save_user_info(user, name, age, country, language)
        self.show_dialog("Information saved successfully.")

    def set_security_question(self, instance):
        user = self.session.get_logged_in_user()
        question = self.security_question_input.text.strip()
        answer = self.security_answer_input.text.strip()
        if not question or not answer:
            self.show_dialog("Both question and answer are required.")
            return
        set_security_question(user, question, answer)
        self.show_dialog("Security question updated.")

    def update_password(self, instance):
        old_pass = self.old_pass_input.text.strip()
        new_pass = self.new_pass_input.text.strip()
        user = self.session.get_logged_in_user()
        if not old_pass or not new_pass:
            self.show_dialog("Please fill in both password fields.")
        elif update_password(user, old_pass, new_pass):
            self.old_pass_input.text = ""
            self.new_pass_input.text = ""
            self.show_dialog("Password updated successfully.")
        else:
            self.show_dialog("Old password incorrect or update failed.")

    def change_username(self, instance):
        old_username = self.old_username_input.text.strip()
        new_username = self.new_username_input.text.strip()
        user = self.session.get_logged_in_user()
        if not old_username or not new_username:
            self.show_dialog("Both old and new username required.")
        elif old_username != user:
            self.show_dialog("Old username does not match current user.")
        elif update_username(old_username, new_username, None):
            self.session.set_logged_in_user(new_username)
            self.old_username_input.text = ""
            self.new_username_input.text = ""
            self.show_dialog("Username updated successfully.")
        else:
            self.show_dialog("Username change failed.")

    def forgot_password(self, instance):
        user = self.session.get_logged_in_user()
        question = get_security_question(user)
        if not question:
            self.show_dialog("No security question set for this user.")
            return
        def check_answer(dialog, answer_field):
            answer = answer_field.text.strip()
            if validate_security_answer(user, answer):
                self.dialog.dismiss()
                self.show_reset_password_dialog(user)
            else:
                self.show_dialog("Incorrect answer.")
        answer_field = MDTextField(hint_text="Answer", password=True)
        self.dialog = MDDialog(
            title="Security Question",
            text=question,
            type="custom",
            content_cls=answer_field,
            buttons=[MDRaisedButton(text="Submit", on_release=lambda x: check_answer(self.dialog, answer_field))]
        )
        self.dialog.open()

    def show_reset_password_dialog(self, user):
        new_pass_field = MDTextField(hint_text="New Password", password=True)
        def do_reset(dialog, field):
            new_pass = field.text.strip()
            if new_pass:
                from backend.auth import update_password
                update_password(user, "", new_pass)
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

    def go_back(self, instance):
        self.manager.current = "home"

    def open_file_chooser(self, instance):
        filechooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])
        box = BoxLayout(orientation='vertical')
        box.add_widget(filechooser)
        def select_file(inst):
            selected = filechooser.selection
            if selected:
                self.profile_img.source = selected[0]
                user = self.session.get_logged_in_user()
                save_user_info(
                    user,
                    self.name_input.text, self.age_input.text, self.country_input.text, self.language_input.text,
                    selected[0]
                )
                popup.dismiss()
        select_btn = MDRaisedButton(text="Select", on_release=select_file)
        box.add_widget(select_btn)
        popup = Popup(title="Choose Profile Photo", content=box, size_hint=(0.9, 0.9))
        popup.open()

    def remove_profile_photo(self, instance):
        self.profile_img.source = "assets/default_profile.png"
        user = self.session.get_logged_in_user()
        save_user_info(
            user,
            self.name_input.text, self.age_input.text, self.country_input.text, self.language_input.text,
            "assets/default_profile.png"
        )
        self.show_dialog("Profile photo removed and set to default.")

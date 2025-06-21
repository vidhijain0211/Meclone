from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from backend.session_manager import SessionManager
from backend.auth import update_password, update_username, save_user_info, load_user_info, delete_user_account
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

class ProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = SessionManager()
        self.dialog = None
        self.build_ui()

    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=40, spacing=20)

        # Logged in user label
        self.user_label = MDLabel(
            text=f"Logged in as: {self.session.get_logged_in_user()}",
            halign="center", font_style="H6"
        )

        # Personal info fields
        self.name_input = MDTextField(hint_text="Full Name")
        self.age_input = MDTextField(hint_text="Age", input_filter="int")
        self.country_input = MDTextField(hint_text="Country")

        # Profile image
        self.profile_img = Image(source="assets/default_profile.png", size_hint=(1, 0.4))

        upload_btn = MDRaisedButton(
            text="Upload Profile Photo", pos_hint={"center_x": 0.5},
            on_release=self.open_file_chooser
        )

        save_info_btn = MDRaisedButton(
            text="Save Info", pos_hint={"center_x": 0.5}, on_release=self.save_info
        )

        # Change username
        self.new_username_input = MDTextField(hint_text="Change Username")
        change_username_btn = MDRaisedButton(
            text="Change Username", pos_hint={"center_x": 0.5}, on_release=self.change_username
        )

        # Change password
        self.new_pass_input = MDTextField(hint_text="New Password", password=True)
        self.confirm_pass_input = MDTextField(hint_text="Confirm Password", password=True)
        change_pass_btn = MDRaisedButton(
            text="Update Password", pos_hint={"center_x": 0.5}, on_release=self.update_password
        )

        # Delete account
        delete_btn = MDRaisedButton(
            text="Delete Account", pos_hint={"center_x": 0.5}, md_bg_color=(1, 0, 0, 1),
            on_release=self.confirm_delete
        )

        # Back button
        back_btn = MDRaisedButton(text="Back", pos_hint={"center_x": 0.5}, on_release=self.go_back)

        # Add to layout
        layout.add_widget(self.user_label)
        layout.add_widget(self.name_input)
        layout.add_widget(self.age_input)
        layout.add_widget(self.country_input)
        layout.add_widget(save_info_btn)

        layout.add_widget(self.profile_img)
        layout.add_widget(upload_btn)

        layout.add_widget(self.new_username_input)
        layout.add_widget(change_username_btn)
        layout.add_widget(self.new_pass_input)
        layout.add_widget(self.confirm_pass_input)
        layout.add_widget(change_pass_btn)
        layout.add_widget(delete_btn)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def on_pre_enter(self):
        user = self.session.get_logged_in_user()
        if user:
            self.user_label.text = f"Logged in as: {user}"
            info = load_user_info(user)
            self.name_input.text = info.get("name", "")
            self.age_input.text = info.get("age", "")
            self.country_input.text = info.get("country", "")
            img_path = info.get("image")
            if img_path:
                self.profile_img.source = img_path

    def show_dialog(self, message):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            text=message,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()

    def save_info(self, instance):
        name = self.name_input.text.strip()
        age = self.age_input.text.strip()
        country = self.country_input.text.strip()
        user = self.session.get_logged_in_user()
        if not all([name, age, country]):
            self.show_dialog("All fields must be filled.")
            return
        save_user_info(user, name, age, country)
        self.show_dialog("Information saved successfully.")

    def update_password(self, instance):
        new_pass = self.new_pass_input.text.strip()
        confirm = self.confirm_pass_input.text.strip()
        user = self.session.get_logged_in_user()
        if not new_pass or not confirm:
            self.show_dialog("Please fill in both password fields.")
        elif new_pass != confirm:
            self.show_dialog("Passwords do not match.")
        elif update_password(user, new_pass):
            self.new_pass_input.text = ""
            self.confirm_pass_input.text = ""
            self.show_dialog("Password updated successfully.")
        else:
            self.show_dialog("Password update failed.")

    def change_username(self, instance):
        new_username = self.new_username_input.text.strip()
        old_username = self.session.get_logged_in_user()
        if not new_username:
            self.show_dialog("Username cannot be empty.")
        elif update_username(old_username, new_username):
            self.session.set_logged_in_user(new_username)
            self.user_label.text = f"Logged in as: {new_username}"
            self.new_username_input.text = ""
            self.show_dialog("Username updated successfully.")
        else:
            self.show_dialog("Username change failed.")

    def confirm_delete(self, instance):
        user = self.session.get_logged_in_user()
        if user:
            delete_user_account(user)
            self.session.clear_session()
            self.manager.current = "entry"
            self.show_dialog("Account deleted successfully.")

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
                save_user_info(
                    self.session.get_logged_in_user(),
                    self.name_input.text, self.age_input.text, self.country_input.text,
                    selected[0]
                )
                popup.dismiss()

        select_btn = MDRaisedButton(text="Select", on_release=select_file)
        box.add_widget(select_btn)

        popup = Popup(title="Choose Profile Photo", content=box, size_hint=(0.9, 0.9))
        popup.open()

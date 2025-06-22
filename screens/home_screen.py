from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget
from kivymd.toast import toast
from backend.session_manager import SessionManager
from kivy.clock import Clock


class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = SessionManager()
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        self.nav_layout = MDNavigationLayout()

        # Drawer setup
        self.nav_drawer = MDNavigationDrawer()
        drawer_list = MDList()

        def add_nav_item(text, icon_name, screen_target):
            item = OneLineIconListItem(
                text=text,
                on_release=lambda x: self.delayed_navigate(screen_target)
            )
            item.add_widget(IconLeftWidget(icon=icon_name))
            drawer_list.add_widget(item)

        add_nav_item("Reflection", "lightbulb-outline", "reflect")
        add_nav_item("Profile", "account-circle-outline", "profile")
        add_nav_item("Saved Thoughts", "bookmark-outline", "saved_thoughts")
        add_nav_item("App Lock", "lock-outline", "lock")
        add_nav_item("Logout", "logout", "logout")

        self.nav_drawer.add_widget(drawer_list)
        self.nav_layout.add_widget(self.nav_drawer)

        # Main Screen Content
        self.screen_manager = MDScreenManager()
        main_screen = MDScreen(name="main_home")
        main_layout = MDBoxLayout(orientation='vertical')

        toolbar = MDTopAppBar(
            title="MeClone Home",
            left_action_items=[["menu", lambda x: self.nav_drawer.set_state("toggle")]],
        )
        main_layout.add_widget(toolbar)

        self.layout = MDBoxLayout(
            orientation='vertical',
            padding=50,
            spacing=30,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.8, 0.7)
        )

        self.welcome_label = MDLabel(
            text="Welcome!",
            halign="center",
            theme_text_color="Primary",
            font_style="H6",
        )

        self.layout.add_widget(self.welcome_label)
        main_layout.add_widget(self.layout)
        main_screen.add_widget(main_layout)
        self.screen_manager.add_widget(main_screen)
        self.nav_layout.add_widget(self.screen_manager)
        self.add_widget(self.nav_layout)

    def delayed_navigate(self, screen_name):
        self.nav_drawer.set_state("close")
        Clock.schedule_once(lambda dt: self._navigate(screen_name), 0.3)

    def _navigate(self, screen_name):
        if screen_name == "logout":
            self.session.clear_session()
            toast("Logged out successfully!")
            self.manager.current = "entry"
        elif screen_name == "lock":
            lock_screen = self.manager.get_screen("lock")
            lock_screen.open_settings_mode()
            self.manager.current = "lock"
        else:
            self.manager.current = screen_name

    def on_pre_enter(self):
        if not self.session.is_logged_in():
            self.manager.current = "login"
        else:
            current_user_id = self.session.get_logged_in_user()
            if current_user_id:
                from backend.auth import get_username_by_id
                username = get_username_by_id(current_user_id)
                if username:
                    self.welcome_label.text = f"Welcome {username}! What's on your MIND ?"
                else:
                    self.welcome_label.text = "Welcome to MeClone!"
            else:
                self.welcome_label.text = "Welcome to MeClone!"

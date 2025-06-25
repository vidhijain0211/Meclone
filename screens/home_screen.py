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
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView


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
        self.drawer_list = drawer_list

        # Add nav items in new order: Reflection, Routine, Profile, Saved Thoughts, App Lock, Logout
        def add_nav_item(text, icon_name, screen_target):
            def nav_callback(x, target=screen_target):
                print(f"[DEBUG] Drawer item clicked: {target}")
                self.delayed_navigate(target)
            item = OneLineIconListItem(
                text=text,
                on_release=nav_callback
            )
            item.add_widget(IconLeftWidget(icon=icon_name))
            drawer_list.add_widget(item)

        add_nav_item("Reflection", "lightbulb-outline", "reflect")
        add_nav_item("Routine", "calendar-clock", "routine")
        add_nav_item("Profile", "account-circle-outline", "profile")
        add_nav_item("Saved Thoughts", "bookmark-outline", "saved_thoughts")
        add_nav_item("App Lock", "lock-outline", "lock")
        add_nav_item("Logout", "logout", "logout")

        self.nav_drawer.add_widget(drawer_list)

        # Main Screen Content
        self.screen_manager = MDScreenManager()
        main_screen = MDScreen(name="main_home")
        main_layout = MDBoxLayout(orientation='vertical')

        toolbar = MDTopAppBar(
            title="MeClone Home",
            left_action_items=[["menu", lambda x: self.nav_drawer.set_state("toggle")]],
        )
        main_layout.add_widget(toolbar)

        # Modernized scrollable card layout
        scroll = MDScrollView()
        scroll_layout = MDBoxLayout(orientation='vertical', padding=30, spacing=30, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        # Welcome Card
        welcome_card = MDCard(
            orientation='vertical',
            padding=30,
            spacing=20,
            size_hint_y=None,
            radius=[20, 20, 20, 20],
            size_hint=(None, None),
            size=(400, 100),
            pos_hint={"center_x": 0.5}
        )
        self.welcome_label = MDLabel(
            text="Welcome!",
            halign="center",
            theme_text_color="Primary",
            font_style="H5",
            size_hint_y=None,
            height=40
        )
        welcome_card.add_widget(self.welcome_label)
        scroll_layout.add_widget(welcome_card)

        # Quick Actions Card
        actions_card = MDCard(
            orientation='vertical',
            padding=18,
            spacing=10,
            size_hint=(None, None),
            size=(400, 140),
            radius=[16, 16, 16, 16],
            pos_hint={"center_x": 0.5}
        )
        actions_label = MDLabel(
            text="Quick Actions",
            halign="center",
            theme_text_color="Secondary",
            font_style="H6",
            size_hint_y=None,
            height=32
        )
        actions_card.add_widget(actions_label)
        from kivymd.uix.button import MDRaisedButton
        btn_layout = MDBoxLayout(orientation='horizontal', spacing=12, size_hint_y=None, height=48, padding=[0, 0, 0, 0])
        btn_reflect = MDRaisedButton(text="Reflect", on_release=lambda x: self.delayed_navigate("reflect"), size_hint=(1, None), height=48)
        btn_routine = MDRaisedButton(text="Save Routine", on_release=lambda x: self.delayed_navigate("routine"), size_hint=(1, None), height=48)
        btn_saved = MDRaisedButton(text="Saved", on_release=lambda x: self.delayed_navigate("saved_thoughts"), size_hint=(1, None), height=48)
        btn_layout.add_widget(btn_reflect)
        btn_layout.add_widget(btn_routine)
        btn_layout.add_widget(btn_saved)
        actions_card.add_widget(btn_layout)
        scroll_layout.add_widget(actions_card)

        # Info Card
        info_card = MDCard(
            orientation='vertical',
            padding=18,
            spacing=10,
            size_hint_y=None,
            radius=[12, 12, 12, 12],
            size_hint=(None, None),
            size=(400, 80),
            pos_hint={"center_x": 0.5}
        )
        info_label = MDLabel(
            text="Tip: Use the menu to access all features!",
            halign="center",
            theme_text_color="Hint",
            font_style="Body2",
            size_hint_y=None,
            height=28
        )
        info_card.add_widget(info_label)
        scroll_layout.add_widget(info_card)

        scroll.add_widget(scroll_layout)
        main_layout.add_widget(scroll)
        main_screen.add_widget(main_layout)
        self.screen_manager.add_widget(main_screen)

        # Add both to nav_layout in correct order
        self.nav_layout.add_widget(self.screen_manager)
        self.nav_layout.add_widget(self.nav_drawer)
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
        elif screen_name == "routine":
            if not self.manager.has_screen("routine"):
                from screens.routine_screen import RoutineScreen
                self.manager.add_widget(RoutineScreen(name="routine"))
            self.manager.current = "routine"
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

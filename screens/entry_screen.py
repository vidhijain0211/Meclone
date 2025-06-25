from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.image import Image
from kivy.metrics import dp
from kivymd.uix.scrollview import MDScrollView


class EntryScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        # Toolbar
        toolbar = MDTopAppBar(
            title="MeClone App",
            pos_hint={"top": 1},
            elevation=10
        )
        self.add_widget(toolbar)

        # Main layout
        scroll = MDScrollView()
        root_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            size_hint_y=None
        )
        root_layout.bind(minimum_height=root_layout.setter('height'))

        # Card container
        card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(320), dp(500)),
            padding=dp(24),
            spacing=dp(20),
            elevation=12,
            radius=[20, 20, 20, 20],
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        # App Logo
        card.add_widget(Image(
            source="assets/icon.png",
            size_hint=(1, 0.4),
            allow_stretch=True
        ))

        # Welcome Label
        card.add_widget(MDLabel(
            text="Welcome to MeClone",
            halign="center",
            theme_text_color="Primary",
            font_style="H5",
            size_hint_y=None,
            height=40
        ))

        # Login Button
        login_btn = MDRaisedButton(
            text="Login",
            pos_hint={"center_x": 0.5},
            size_hint=(1, None),
            height=dp(48),
            on_release=self.go_to_login
        )

        # Register Button
        register_btn = MDRaisedButton(
            text="Create Account",
            pos_hint={"center_x": 0.5},
            size_hint=(1, None),
            height=dp(48),
            on_release=self.go_to_register
        )

        # Add buttons to card
        card.add_widget(login_btn)
        card.add_widget(register_btn)

        # Add card to root layout
        root_layout.add_widget(card)
        scroll.add_widget(root_layout)
        self.add_widget(scroll)

    def go_to_login(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = "login"

    def go_to_register(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = "register"

    def on_pre_enter(self):
        for child in self.walk():
            if isinstance(child, MDCard):
                child.canvas.ask_update()

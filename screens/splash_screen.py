from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.animation import Animation
from kivymd.uix.spinner import MDSpinner


class SplashScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        Clock.schedule_once(self.animate_ui, 0.5)
        Clock.schedule_once(self.switch_to_entry, 3.5)

    def build_ui(self):
        self.layout = MDBoxLayout(
            orientation="vertical",
            spacing=25,
            padding=50,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(None, None),
            size=(320, 400),
        )

        # App Icon
        self.icon = Image(
            source="assets/icon.png",
            size_hint=(None, None),
            size=(100, 100),
            opacity=0,
        )

        # Label
        self.label = MDLabel(
            text="Welcome to MeClone",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.1, 0.1, 0.1, 1),
            font_style="H5",
            opacity=0,
        )

        # Spinner Loader
        self.spinner = MDSpinner(
            size_hint=(None, None),
            size=(46, 46),
            line_width=2.5,
            color=(0.1, 0.5, 1, 1),
            opacity=0,
        )

        self.layout.add_widget(self.icon)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.spinner)

        self.add_widget(self.layout)

    def animate_ui(self, dt):
        Animation(opacity=1, size=(200, 200), duration=1.5, t='out_elastic').start(self.icon)
        Animation(opacity=1, duration=1.2).start(self.label)
        Animation(opacity=1, duration=1.5).start(self.spinner)

    def switch_to_entry(self, dt):
        self.manager.transition.direction = 'left'
        self.manager.current = "entry"

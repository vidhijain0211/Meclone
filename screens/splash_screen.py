from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.animation import Animation
from kivymd.uix.spinner import MDSpinner
from backend.session_manager import SessionManager
from threading import Thread
import logging


logging.getLogger("transformers").setLevel(logging.WARNING)
logging.getLogger("sentence_transformers").setLevel(logging.WARNING)


class SplashScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        Clock.schedule_once(self.animate_ui, 0.2)  # ✅ Animate immediately
        Clock.schedule_once(self.start_heavy_work, 0.3)
        Clock.schedule_once(self.switch_to_entry, 3.5)
        self.model = None  # Placeholder for the model

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
            opacity=0,  # 🔘 Start hidden
        )

        # Welcome Label
        self.label = MDLabel(
            text="Welcome to MeClone",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.1, 0.1, 0.1, 1),
            font_style="H5",
            opacity=0,  # 🔘 Start hidden
        )

        # Spinner
        self.spinner = MDSpinner(
            size_hint=(None, None),
            size=(46, 46),
            line_width=2.5,
            color=(0.1, 0.5, 1, 1),
            opacity=0,  # 🔘 Start hidden
        )

        self.layout.add_widget(self.icon)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.spinner)

        self.add_widget(self.layout)

    def animate_ui(self, dt):
        Animation(opacity=1, size=(200, 200), duration=1.5, t='out_elastic').start(self.icon)
        Animation(opacity=1, duration=2.2).start(self.label)
        Animation(opacity=1, duration=2.5).start(self.spinner)

    def start_heavy_work(self, dt):
        Thread(target=self.load_heavy_resources).start()

    def load_heavy_resources(self):
        from backend.memory_engine import init_memory_table
        init_memory_table()
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"[ERROR] Could not load sentence-transformers model: {e}")

    def switch_to_entry(self, dt):
        session = SessionManager()
        if session.is_logged_in():
            if session.is_app_lock_enabled():
                self.manager.transition.direction = 'left'
                self.manager.current = "lock"
            else:
                self.manager.transition.direction = 'left'
                self.manager.current = "home"
        else:
            self.manager.transition.direction = 'left'
            self.manager.current = "entry"

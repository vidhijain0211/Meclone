from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from screens.splash_screen import SplashScreen
from screens.entry_screen import EntryScreen
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.home_screen import HomeScreen
from screens.reflection_screen import ReflectionScreen
from screens.app_lock_screen import AppLockScreen
from screens.profile_screen import ProfileScreen
from screens.saved_thoughts_screen import SavedThoughtsScreen
from backend.session_manager import SessionManager
from kivymd.app import MDApp

class MeCloneApp(MDApp):
    def build(self):
        # Theme setup
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        # Screen Manager and Session
        self.screen_manager = MDScreenManager()
        self.session = SessionManager()

        # ⚠️ Remove this in production
        # self.session.clear_session()

        # Add all screens
        self.screen_manager.add_widget(SplashScreen(name="splash"))
        self.screen_manager.add_widget(EntryScreen(name="entry"))
        self.screen_manager.add_widget(LoginScreen(name="login"))
        self.screen_manager.add_widget(RegisterScreen(name="register"))
        self.screen_manager.add_widget(ReflectionScreen(name="reflect"))
        self.screen_manager.add_widget(HomeScreen(name="home"))
        self.screen_manager.add_widget(AppLockScreen(name="lock"))
        self.screen_manager.add_widget(ProfileScreen(name="profile"))
        self.screen_manager.add_widget(SavedThoughtsScreen(name="saved_thoughts"))

        # Initial screen (splash will auto-navigate later)
        self.screen_manager.current = "splash"

        return self.screen_manager

if __name__ == '__main__':
    MeCloneApp().run()

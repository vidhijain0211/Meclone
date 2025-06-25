from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from screens.splash_screen import SplashScreen
from backend.session_manager import SessionManager

from kivy.clock import Clock
import threading
from screens.routine_screen import RoutineScreen
from backend.routine_manager import get_due_routines
from kivymd.toast import toast
import datetime
from plyer import notification
from kivy.utils import platform

class MeCloneApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.screen_manager = MDScreenManager()
        self.session = SessionManager()
        # Only add splash screen initially
        self.screen_manager.add_widget(SplashScreen(name="splash"))
        self.screen_manager.current = "splash"
        # Load remaining screens in background
        threading.Thread(target=self.load_remaining_screens).start()
        # Start routine reminder checker (for in-app toasts/notifications)
        Clock.schedule_interval(self.check_routine_reminders, 60)  # check every minute
        # Start Android background service for offline reminders
        if platform == "android":
            try:
                from jnius import autoclass
                PythonService = autoclass('org.kivy.android.PythonService')
                service = PythonService.mService
                if service is None:
                    from android import AndroidService
                    service = AndroidService('RoutineService', 'running')
                    service.start('Service started')
            except Exception as e:
                print(f"[RoutineService] Could not start background service: {e}")
        return self.screen_manager

    def check_routine_reminders(self, dt):
        user_id = self.session.get_logged_in_user()
        if not user_id:
            print("[Routine Reminder] No user logged in.")
            return
        now = datetime.datetime.now().strftime("%I:%M %p").lower().strip()
        print(f"[Routine Reminder] Current time: '{now}'")
        due = get_due_routines(user_id, now)
        print(f"[Routine Reminder] Routines due at this time: {due}")
        for r in due:
            # Show system notification
            notification.notify(
                title="Routine Reminder",
                message=f"{r['time']}: {r['text']}",
                timeout=10
            )
            toast(f"{r['time']}: {r['text']}")

    def load_remaining_screens(self):
        from screens.entry_screen import EntryScreen
        from screens.login_screen import LoginScreen
        from screens.register_screen import RegisterScreen
        from screens.home_screen import HomeScreen
        from screens.reflection_screen import ReflectionScreen
        from screens.app_lock_screen import AppLockScreen
        from screens.profile_screen import ProfileScreen
        from screens.saved_thoughts_screen import SavedThoughtsScreen

        # Add all other screens
        Clock.schedule_once(lambda dt: self.screen_manager.add_widget(EntryScreen(name="entry")))
        Clock.schedule_once(lambda dt: self.screen_manager.add_widget(LoginScreen(name="login")))
        Clock.schedule_once(lambda dt: self.screen_manager.add_widget(RegisterScreen(name="register")))
        Clock.schedule_once(lambda dt: self.screen_manager.add_widget(ReflectionScreen(name="reflect")))
        Clock.schedule_once(lambda dt: self.screen_manager.add_widget(HomeScreen(name="home")))
        Clock.schedule_once(lambda dt: self.screen_manager.add_widget(AppLockScreen(name="lock")))
        Clock.schedule_once(lambda dt: self.screen_manager.add_widget(ProfileScreen(name="profile")))
        Clock.schedule_once(lambda dt: self.screen_manager.add_widget(SavedThoughtsScreen(name="saved_thoughts")))
        Clock.schedule_once(lambda dt: self.screen_manager.add_widget(RoutineScreen(name="routine")))

        # After a short delay, switch to the actual start screen
        Clock.schedule_once(lambda dt: setattr(self.screen_manager, "current", "entry"), 2.5)

if __name__ == '__main__':
    MeCloneApp().run()

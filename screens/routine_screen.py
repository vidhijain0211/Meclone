from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.toast import toast
from backend.session_manager import SessionManager
from backend.routine_manager import save_routine, load_routines
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty

class RoutineScreen(MDScreen):
    edit_index = NumericProperty(-1)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        root = MDBoxLayout(orientation='vertical')

        # Scrollable content area
        scroll = MDScrollView(size_hint=(1, 1))
        layout = MDBoxLayout(orientation='vertical', padding=30, spacing=24, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Add Routine Card
        add_card = MDCard(orientation='vertical', padding=18, spacing=12, size_hint=(1, None), height=300, radius=[20, 20, 20, 20], pos_hint={"center_x": 0.5})
        add_card.add_widget(MDLabel(text="Add Routine", font_style="H6", halign="center", size_hint_y=None, height=32))
        self.routine_input = MDTextField(hint_text="Routine (e.g. I brush my teeth)", size_hint_y=None, height=48)
        self.routine_time_input = MDTextField(hint_text="Time (e.g. 08:00 am)", size_hint_y=None, height=48)
        add_card.add_widget(self.routine_input)
        add_card.add_widget(self.routine_time_input)
        add_card.add_widget(Widget(size_hint_y=None, height=12))
        save_btn = MDRaisedButton(text="Save Routine", on_release=self.save_routine, size_hint=(1, None), height=48)
        add_card.add_widget(save_btn)
        back_btn = MDRaisedButton(text="Back", on_release=self.go_back, size_hint=(1, None), height=44)
        add_card.add_widget(back_btn)
        layout.add_widget(add_card)
        layout.add_widget(Widget(size_hint_y=None, height=24))

        # Saved Routines Card
        self.saved_card = MDCard(orientation='vertical', padding=18, spacing=12, size_hint=(1, None), radius=[20, 20, 20, 20], pos_hint={"center_x": 0.5})
        self.saved_card.add_widget(MDLabel(text="Saved Routines", font_style="H6", halign="center", size_hint_y=None, height=32))
        self.routine_list = MDBoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        self.routine_list.bind(minimum_height=self.routine_list.setter('height'))
        self.saved_card.add_widget(self.routine_list)
        layout.add_widget(self.saved_card)
        layout.add_widget(Widget(size_hint_y=None, height=24))

        scroll.add_widget(layout)
        root.add_widget(scroll)
        self.add_widget(root)
        self.load_routines()

    def save_routine(self, instance):
        user_id = SessionManager().get_logged_in_user()
        routine_text = self.routine_input.text.strip()
        routine_time = self.routine_time_input.text.strip().replace(' ', '').lower()
        if not routine_text or not routine_time:
            toast("Please enter both routine and time.")
            return
        routines = load_routines(user_id)
        if self.edit_index != -1 and 0 <= self.edit_index < len(routines):
            routines[self.edit_index] = {"text": routine_text, "time": routine_time}
            self.edit_index = -1
            toast("Routine updated!")
        else:
            routines.append({"text": routine_text, "time": routine_time})
            toast("Routine saved!")
        # Save updated routines
        from backend.routine_manager import ROUTINE_FILE
        import json
        with open(ROUTINE_FILE, "r") as f:
            data = json.load(f)
        data[str(user_id)] = routines
        with open(ROUTINE_FILE, "w") as f:
            json.dump(data, f, indent=4)
        self.routine_input.text = ""
        self.routine_time_input.text = ""
        self.load_routines()

    def load_routines(self):
        self.routine_list.clear_widgets()
        user_id = SessionManager().get_logged_in_user()
        routines = load_routines(user_id)
        if not routines:
            self.routine_list.add_widget(MDLabel(text="No routines saved.", halign="center"))
        else:
            for idx, r in enumerate(routines):
                row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=8)
                row.add_widget(MDLabel(text=f"{r['time']} - {r['text']}", halign="left", size_hint_x=0.7))
                edit_btn = MDIconButton(icon="pencil", on_release=lambda x, i=idx: self.edit_routine(i), theme_text_color="Custom", text_color=(0,0.5,1,1))
                delete_btn = MDIconButton(icon="delete", on_release=lambda x, i=idx: self.delete_routine(i), theme_text_color="Custom", text_color=(1,0,0,1))
                row.add_widget(edit_btn)
                row.add_widget(delete_btn)
                self.routine_list.add_widget(row)

    def edit_routine(self, idx):
        user_id = SessionManager().get_logged_in_user()
        routines = load_routines(user_id)
        if 0 <= idx < len(routines):
            routine = routines[idx]
            self.routine_input.text = routine['text']
            self.routine_time_input.text = routine['time']
            self.edit_index = idx
            toast("Edit the routine and press Save Routine.")

    def delete_routine(self, idx, reload_list=True):
        user_id = SessionManager().get_logged_in_user()
        routines = load_routines(user_id)
        if 0 <= idx < len(routines):
            routines.pop(idx)
            from backend.routine_manager import ROUTINE_FILE
            import json
            with open(ROUTINE_FILE, "r") as f:
                data = json.load(f)
            data[str(user_id)] = routines
            with open(ROUTINE_FILE, "w") as f:
                json.dump(data, f, indent=4)
            if reload_list:
                self.load_routines()
            toast("Routine deleted.")
        self.edit_index = -1

    def go_back(self, instance):
        self.manager.current = "home"

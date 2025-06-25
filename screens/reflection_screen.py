from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

from backend.reflection import save_reflection, get_relevant_reflection
from backend.voice_handler import speak, listen
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView


class ReflectionScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        scroll = MDScrollView()
        scroll_layout = MDBoxLayout(orientation='vertical', padding=30, spacing=30, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        # Input Card
        input_card = MDCard(
            orientation='vertical',
            padding=24,
            spacing=18,
            size_hint=(1, None),
            height=120,
            radius=[20, 20, 20, 20],
            pos_hint={"center_x": 0.5}
        )
        input_label = MDLabel(
            text="What's on your mind?",
            halign="left",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=32
        )
        self.input = MDTextField(hint_text="Type your thought here", size_hint_y=None, height=48)
        input_card.add_widget(input_label)
        input_card.add_widget(self.input)
        scroll_layout.add_widget(input_card)

        # Actions Card
        actions_card = MDCard(
            orientation='horizontal',
            padding=18,
            spacing=14,
            size_hint=(1, None),
            height=60,
            radius=[16, 16, 16, 16],
            pos_hint={"center_x": 0.5}
        )
        save_btn = MDRaisedButton(
            text="Save",
            on_release=self.save_thought,
            size_hint=(1, None),
            height=48
        )
        voice_btn = MDRaisedButton(
            text="Voice",
            on_release=self.get_voice_input,
            size_hint=(1, None),
            height=48
        )
        reflect_btn = MDRaisedButton(
            text="Reflect",
            on_release=self.reflect,
            size_hint=(1, None),
            height=48
        )
        actions_card.add_widget(save_btn)
        actions_card.add_widget(voice_btn)
        actions_card.add_widget(reflect_btn)
        scroll_layout.add_widget(actions_card)

        # Reflection Output Card
        output_card = MDCard(
            orientation='vertical',
            padding=18,
            spacing=10,
            size_hint=(1, None),
            height=120,
            radius=[12, 12, 12, 12],
            pos_hint={"center_x": 0.5}
        )
        output_label = MDLabel(
            text="Reflection Output:",
            halign="left",
            theme_text_color="Secondary",
            font_style="Body1",
            size_hint_y=None,
            height=28
        )
        self.reflection_label = MDLabel(
            text="Your reflection will appear here.",
            halign="left",
            valign="middle",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=60,
            padding=(12, 0)
        )
        output_card.add_widget(output_label)
        output_card.add_widget(self.reflection_label)
        scroll_layout.add_widget(output_card)

        # Back Button
        back_btn = MDRaisedButton(
            text="Back",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(120, 48),
            on_release=self.go_back
        )
        scroll_layout.add_widget(back_btn)

        scroll.add_widget(scroll_layout)
        self.add_widget(scroll)

    def save_thought(self, instance):
        text = self.input.text.strip()
        if text:
            save_reflection(text)
            speak("Thought saved to memory.")
            toast("Saved to memory.")
            self.input.text = ""

    def get_voice_input(self, instance):
        text = listen()
        if text:
            self.input.text = text
            self.save_thought(instance)
        else:
            speak("Sorry, I could not understand.")
            toast("Could not understand voice.")

    def reflect(self, instance):
        query = self.input.text.strip()
        if not query:
            speak("Please type or say what you want to reflect on.")
            toast("Please type or speak a reflection query.")
            return
        response = get_relevant_reflection(query)
        if response:
            self.reflection_label.text = response  # Show in black strip at bottom BEFORE speaking
            # Force UI update before speaking
            Clock.schedule_once(lambda dt: speak(response), 0.01)
            toast("Relevant thought found.")
        else:
            self.reflection_label.text = "No relevant reflection found."
            Clock.schedule_once(lambda dt: speak("Sorry, no relevant reflection found."), 0.01)
            toast("No relevant thought found.")

    def go_back(self, instance):
        if self.manager:
            self.manager.current = "home"

    def on_pre_enter(self):
        # Force canvas update for all MDCard children to restore shadow
        for child in self.walk():
            if isinstance(child, MDCard):
                child.canvas.ask_update()

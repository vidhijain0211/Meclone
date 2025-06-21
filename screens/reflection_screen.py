from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout

from backend.reflection import save_reflection, get_relevant_reflection
from backend.voice_handler import speak, listen


class ReflectionScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=40, spacing=20)

        self.input = MDTextField(hint_text="What's on your mind?")

        save_btn = MDRaisedButton(
            text="Save Thought",
            pos_hint={"center_x": 0.5},
            on_release=self.save_thought
        )
        voice_btn = MDRaisedButton(
            text="Voice Input",
            pos_hint={"center_x": 0.5},
            on_release=self.get_voice_input
        )
        reflect_btn = MDRaisedButton(
            text="Reflect",
            pos_hint={"center_x": 0.5},
            on_release=self.reflect
        )
        back_btn = MDRaisedButton(
            text="Back",
            pos_hint={"center_x": 0.5},
            on_release=self.go_back
        )

        layout.add_widget(self.input)
        layout.add_widget(save_btn)
        layout.add_widget(voice_btn)
        layout.add_widget(reflect_btn)
        layout.add_widget(back_btn)

        self.add_widget(layout)

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
            speak(response)
            toast("Relevant thought found.")
        else:
            speak("Sorry, no relevant reflection found.")
            toast("No relevant thought found.")

    def go_back(self, instance):
        if self.manager:
            self.manager.current = "home"

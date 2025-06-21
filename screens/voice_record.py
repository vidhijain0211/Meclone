from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.slider import MDSlider
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock

from backend.voice_io import record_voice, speak_text
from backend.reflection_manager import save_thought
import speech_recognition as sr
import os
import playsound


class VoiceRecordScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.duration = 5
        self.filename = "assets/sounds/recorded.wav"
        self.build_ui()

    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15)

        layout.add_widget(MDLabel(
            text="🎙️ Voice Recorder", halign="center", theme_text_color="Custom",
            text_color=(1, 1, 1, 1), font_style="H5"
        ))

        self.duration_label = MDLabel(text=f"Duration: {self.duration} sec", halign="center")
        layout.add_widget(self.duration_label)

        duration_slider = MDSlider(min=1, max=20, value=self.duration, step=1)
        duration_slider.bind(value=self.on_slider_change)
        layout.add_widget(duration_slider)

        record_button = MDRaisedButton(
            text="Start Recording", pos_hint={"center_x": 0.5}, on_release=self.start_recording
        )
        layout.add_widget(record_button)

        play_button = MDRaisedButton(
            text="Play Last Recording", pos_hint={"center_x": 0.5}, on_release=self.play_recording
        )
        layout.add_widget(play_button)

        back_button = MDRaisedButton(
            text="Back to Home", pos_hint={"center_x": 0.5}, on_release=self.go_home
        )
        layout.add_widget(back_button)

        self.status_label = MDLabel(
            text="", halign="center", theme_text_color="Custom", text_color=(0.8, 0.8, 0.8, 1)
        )
        layout.add_widget(self.status_label)

        self.transcription_label = MDLabel(
            text="", halign="center", theme_text_color="Custom", text_color=(1, 1, 1, 1)
        )
        layout.add_widget(self.transcription_label)

        self.add_widget(layout)

    def on_slider_change(self, instance, value):
        self.duration = int(value)
        self.duration_label.text = f"Duration: {self.duration} sec"

    def start_recording(self, instance):
        try:
            os.makedirs("assets/sounds", exist_ok=True)
            record_voice(self.filename, self.duration)
            self.status_label.text = "Recording done. Transcribing..."
            Clock.schedule_once(self.transcribe_and_save, 0.5)
        except Exception as e:
            MDDialog(text="Recording failed: " + str(e)).open()

    def transcribe_and_save(self, dt):
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(self.filename) as source:
                audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            self.transcription_label.text = f"📝 Transcription: {text}"
        except Exception as e:
            text = ""
            self.transcription_label.text = "⚠️ Could not transcribe the audio."

        save_thought(text, self.filename)
        speak_text("Voice thought saved to memory.")
        MDDialog(text="Voice thought saved to memory.").open()
        self.status_label.text = f"Saved as: {self.filename}"

    def play_recording(self, instance):
        try:
            playsound.playsound(self.filename)
        except Exception as e:
            MDDialog(text="Playback failed: " + str(e)).open()

    def go_home(self, instance):
        self.manager.current = "home"

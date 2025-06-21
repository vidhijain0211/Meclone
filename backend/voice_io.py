import sounddevice as sd
import wavio

def record_voice(filename, duration=5, rate=44100):
    print("Recording...")
    recording = sd.rec(int(duration * rate), samplerate=rate, channels=2)
    sd.wait()
    wavio.write(filename, recording, rate, sampwidth=2)
    print("Recording saved to", filename)
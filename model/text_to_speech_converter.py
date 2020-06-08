import pyttsx3

class TextToSpeechConverter:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)

    def convert_text_to_speech(self, text):
        self.engine.say(text)
        try:
            self.engine.runAndWait()
        except RuntimeError:
            return
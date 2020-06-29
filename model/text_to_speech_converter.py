import pyttsx3

class TextToSpeechConverter:
    """
    Class used to convert a written prediction in a vocal prediction.
    """
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)

    def convert_text_to_speech(self, text):
        """
        This method 'says' the prediction and it is meant to be launched in a different thread.
        """
        self.engine.say(text)
        try:
            self.engine.runAndWait()
        except RuntimeError:
            return

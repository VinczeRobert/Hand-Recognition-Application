import pickle
from base_constants.constants import HAND, IMAGE_TYPE


class Settings:
    _instance = None

    def __init__(self):

        self.hand = HAND[0]
        self.image_type = IMAGE_TYPE[0]
        self.vocal_mode = False
        self.android_server_url = ''
        self.h5_path = ''
        self.intermediary_steps = {
            "Filtered Image": False,
            "Grayscale Image": False,
            "Binary Image": False,
            "Extracted Hand Image": False,
            "Opened Hand Image": False,
            "Contoured Image": False,
            "Final Image": False
        }

        self.deserialize()

    @staticmethod
    def get_instance():
        if Settings._instance is None:
            if Settings.deserialize() != 0:
                Settings._instance = Settings()
        return Settings._instance

    def switch_vocal_mode(self):
        self.vocal_mode = not self.vocal_mode

    def switch_image_type(self):
        self.image_type = IMAGE_TYPE[IMAGE_TYPE.index(self.image_type) ^ 1]

    def switch_hand(self):
        self.hand = HAND[HAND.index(self.hand) ^ 1]

    def set_android_server_url(self, android_server_url):
        self.android_server_url = android_server_url

    def set_h5_path(self, h5_path):
        self.h5_path = h5_path

    def set_intermediary_step(self, field):
        self.intermediary_steps[field.text()] = field.isChecked()

    def serialize(self):
        with open('settings', 'wb') as f:
            pickle.dump(self, f)
        return 0

    #TODO: Serialization-Deserialization has some issues. First we should see if it's worth doing it at all and if yes, then correct it
    @staticmethod
    def deserialize():
        try:
            with open('settings', 'rb') as f:
                Settings._instance = pickle.load(f)
            return 0
        except FileNotFoundError:
            return -1

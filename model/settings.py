import pickle

HAND = ['RIGHT', 'LEFT']
IMAGE_TYPE = ['RGB', 'BINARY']

class Settings:
    _instance = None

    def __init__(self):
        self.classes = ['A', 'B', 'C', 'D', 'Delete', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'NewLine', 'O',
                        'P', 'Q', 'R', 'S', 'Space', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        self.hand = HAND[0]
        self.image_type = IMAGE_TYPE[0]
        self.android_server_url = ''
        self.intermediary_steps = {
            "Filtered Image": False,
            "Background Difference Image": False,
            "Extracted Binary Hand Image": False,
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

    def switch_image_type(self):
        if self.image_type == IMAGE_TYPE[0]:
            self.image_type = IMAGE_TYPE[1]
        else:
            self.image_type = IMAGE_TYPE[0]
        return Settings._instance

    def switch_hand(self):
        if self.hand == HAND[0]:
            self.hand = HAND[1]
        else:
            self.hand = HAND[0]

    def set_android_server_url(self, android_server_url):
        self.android_server_url = android_server_url

    def set_intermediary_step(self, field):
        self.intermediary_steps[field.text()] = field.isChecked()

    def serialize(self):
        with open('settings', 'wb') as f:
            pickle.dump(self, f)
        return 0

    @staticmethod
    def deserialize():
        try:
            with open('settings', 'rb') as f:
                Settings._instance = pickle.load(f)
            return 0
        except FileNotFoundError:
            return -1

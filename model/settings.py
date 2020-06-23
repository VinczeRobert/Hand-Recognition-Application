import pickle

HAND = ['RIGHT', 'LEFT']
IMAGE_TYPE = ['RGB', 'BINARY']


class Settings:
    _instance = None

    def __init__(self):
        self._classes = ['A', 'B', 'C', 'D', 'Delete', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'NewLine', 'O',
                         'P', 'Q', 'R', 'S', 'Space', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        self._hand = HAND[0]
        self._image_type = IMAGE_TYPE[0]
        self._android_server_url = ''
        self._intermediary_steps = {
            "Filtered Image": False,
            "Background Difference Image": False,
            "Extracted Binary Hand Image": False,
            "Opened Hand Image": False,
            "Contoured Image": False,
            "Final Image": False
        }

    @staticmethod
    def get_instance():
        if Settings._instance is None:
            if Settings._deserialize() != 0:
                Settings._instance = Settings()
        return Settings._instance

    def get_classes(self):
        return self._classes

    def switch_image_type(self):
        if self._image_type == IMAGE_TYPE[0]:
            self._image_type = IMAGE_TYPE[1]
        else:
            self._image_type = IMAGE_TYPE[0]
        return Settings._instance

    def get_image_type(self):
        return self._image_type

    def switch_hand(self):
        if self._hand == HAND[0]:
            self._hand = HAND[1]
        else:
            self._hand = HAND[0]

    def get_hand(self):
        return self._hand

    def set_android_server_url(self, android_server_url):
        self._android_server_url = android_server_url

    def get_android_server_url(self):
        return self._android_server_url

    def set_intermediary_step(self, field):
        self._intermediary_steps[field.text()] = field.isChecked()

    def get_intermediary_steps(self):
        return self._intermediary_steps

    def serialize(self):
        with open('settings', 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def _deserialize():
        try:
            with open('settings', 'rb') as f:
                Settings._instance = pickle.load(f)
            return 0
        except FileNotFoundError:
            return -1

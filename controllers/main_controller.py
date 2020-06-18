from model.settings import Settings
from view.main_view import MainView


class MainController:
    def __init__(self):

        self.main_view = MainView.get_instance()
        self.settings = Settings.get_instance()
        self.main_view.closed.connect(lambda: self.serialize())
        self.main_view.show()

    def serialize(self):
        self.settings.serialize()


import sys

from view.main_view import MainView


class MainController:
    def __init__(self):

        self.main_view = MainView.get_instance()
        self.main_view.show()



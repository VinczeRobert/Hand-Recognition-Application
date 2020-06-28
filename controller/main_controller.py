from model.frame_captor import FrameCaptor
from model.settings import Settings
from view.main_view import MainView
import tensorflow as tf


class MainController:
    def __init__(self):
        self.settings = Settings.get_instance()

        main_view = MainView.get_instance()
        main_view.closed.connect(lambda: self.prepare_for_closing())
        main_view.show()

    def prepare_for_closing(self):
        FrameCaptor.get_instance().pause_and_restart_camera(False)
        FrameCaptor.get_instance().close_camera()
        self.settings.serialize()


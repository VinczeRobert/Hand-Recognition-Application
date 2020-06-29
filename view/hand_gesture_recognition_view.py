from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QCheckBox
from view.dialogs import choose_file_to_load, choose_file_to_save
from view.hand_graphics_view import HandGraphicsView
from view.style_sheets.main_view_stylesheet import BUTTON_STYLE_SHEET


# noinspection PyArgumentList
class HandGestureRecognitionView(HandGraphicsView):
    """
    View class used for displaying the Hand Gesture Recognition submenu
    """

    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self):
        super(HandGestureRecognitionView, self).__init__()

        self.load_text_button = QPushButton("Load text", self)
        self.save_text_button = QPushButton("Save text", self)
        self.save_background_button = QPushButton("Set Background", self)

        self.vocal_mode_checkbox = QCheckBox('Vocal Mode', self)

        self.setup_view()

    def setup_view(self):
        super(HandGestureRecognitionView, self).setup_view()

        self.load_text_button.setGeometry(QtCore.QRect(1340, 50, 150, 60))
        self.save_text_button.setGeometry(QtCore.QRect(1340, 170, 150, 60))
        self.save_background_button.setGeometry(QtCore.QRect(1340, 290, 150, 60))

        self.vocal_mode_checkbox.setGeometry(QtCore.QRect(1350, 410, 150, 70))
        self.vocal_mode_checkbox.setStyleSheet("font-size: 20px;")

        self.setStyleSheet(BUTTON_STYLE_SHEET)

    @staticmethod
    def choose_text_file_to_load():
        text_file_path = choose_file_to_load('Select Text File', "txt(*.txt)")
        return text_file_path

    @staticmethod
    def choose_text_file_to_save():
        text_file_path = choose_file_to_save('Select Path', "txt(*.txt)")
        return text_file_path
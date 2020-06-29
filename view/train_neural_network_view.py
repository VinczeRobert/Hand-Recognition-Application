import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QPlainTextEdit
from view.dialogs import choose_folder
from view.style_sheets.main_view_stylesheet import BUTTON_STYLE_SHEET, LABEL_STYLE_SHEET


# noinspection PyArgumentList
class TrainNeuralNetworkView(QtWidgets.QWidget):
    """
    View class used for displaying the Train Neural Network submenu
    """

    def __init__(self, parent=None):
        super(TrainNeuralNetworkView, self).__init__(parent)

        self.load_dataset_button = QtWidgets.QPushButton("Select Dataset path", self)
        self.load_dataset_label = QtWidgets.QLabel("No path has been chosen.", self)

        self.start_training_button = QtWidgets.QPushButton("Start Training", self)

        self.message_plain_text = QPlainTextEdit(self)

        self.setup_view()

    def setup_view(self):
        self.load_dataset_button.setGeometry(QtCore.QRect(1240, 260, 150, 60))
        self.load_dataset_button.setStyleSheet(BUTTON_STYLE_SHEET)

        self.start_training_button.setGeometry(QtCore.QRect(1240, 470, 150, 60))
        self.start_training_button.setStyleSheet(BUTTON_STYLE_SHEET)

        self.load_dataset_label.setGeometry(QtCore.QRect(1240, 330, 240, 35))
        self.load_dataset_label.setStyleSheet(LABEL_STYLE_SHEET)

        self.message_plain_text.setGeometry(QtCore.QRect(320, 110, 770, 460))
        self.message_plain_text.setPlainText('')
        self.message_plain_text.setStyleSheet('background-color: white;')

    def choose_dataset_folder(self):
        folder_path = choose_folder('Select Dataset Folder')
        if folder_path != '':
            self.load_dataset_label.setText(os.path.basename(folder_path))
            return folder_path
        return None

    def appendText(self, message):
        self.message_plain_text.appendPlainText(message)

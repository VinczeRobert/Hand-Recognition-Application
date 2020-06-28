import os
from PyQt5 import QtCore, QtWidgets

from view.dialogs import choose_folder
from view.style_sheets.main_view_stylesheet import BUTTON_STYLE_SHEET, LABEL_STYLE_SHEET


# noinspection PyArgumentList
class ScrollMessageBox(QtWidgets.QMessageBox):
    def __init__(self):
        QtWidgets.QMessageBox.__init__(self)
        scroll = QtWidgets.QScrollArea(self)
        scroll.setWidgetResizable(True)
        self.content = QtWidgets.QWidget()
        scroll.setWidget(self.content)
        self.vertical_layout = QtWidgets.QVBoxLayout(self.content)
        self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())


# noinspection PyArgumentList
class TrainNeuralNetworkView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(TrainNeuralNetworkView, self).__init__(parent)

        self.load_dataset_button = QtWidgets.QPushButton("Select Dataset path", self)
        self.load_dataset_label = QtWidgets.QLabel("No path has been chosen.", self)

        self.start_training_button = QtWidgets.QPushButton("Start Training", self)

        self.status_message_label = QtWidgets.QLabel(self)

        self.setup_view()

    def setup_view(self):
        self.load_dataset_button.setGeometry(QtCore.QRect(1240, 260, 150, 60))
        self.load_dataset_button.setStyleSheet(BUTTON_STYLE_SHEET)

        self.start_training_button.setGeometry(QtCore.QRect(1240, 470, 150, 60))
        self.start_training_button.setStyleSheet(BUTTON_STYLE_SHEET)

        self.load_dataset_label.setGeometry(QtCore.QRect(1240, 330, 240, 35))
        self.load_dataset_label.setStyleSheet(LABEL_STYLE_SHEET)

        self.status_message_label.setGeometry(QtCore.QRect(320, 110, 770, 460))
        self.status_message_label.setText("")

    def choose_dataset_folder(self):
        folder_path = choose_folder('Select Dataset Folder')
        if folder_path is not None:
            self.load_dataset_label.setText(os.path.basename(folder_path))
        return folder_path

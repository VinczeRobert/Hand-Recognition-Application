from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QStackedWidget, QGroupBox, QHBoxLayout, QSizePolicy, QPushButton, QMainWindow, \
    QLabel, QWidget
from view.hand_gesture_recognition_view import HandGestureRecognitionView
from view.add_new_sign_view import AddNewSignView
from view.train_neural_network_view import TrainNeuralNetworkView
from view.settings_view import SettingsView
from view.style_sheets.main_view_stylesheet import FIRST_LETTER_LABEL_STYLE_SHEET, REST_LETTERS_LABEL_STYLE_SHEET, \
    BUTTON_STYLE_SHEET


# noinspection PyArgumentList
class MainView(QMainWindow):
    _instance = None

    closed = pyqtSignal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.home_view = HomeView()
        self.settings_view = SettingsView()
        self.hand_gesture_recognition_view = HandGestureRecognitionView()
        self.add_new_sign_view = AddNewSignView()
        self.train_neural_network_view = TrainNeuralNetworkView()

        self.central_widget.addWidget(self.home_view)
        self.central_widget.addWidget(self.settings_view)
        self.central_widget.addWidget(self.hand_gesture_recognition_view)
        self.central_widget.addWidget(self.add_new_sign_view)
        self.central_widget.addWidget(self.train_neural_network_view)

        self.central_widget.setCurrentWidget(self.home_view)

        self.horizontal_group_box = QGroupBox(self)
        self.horizontal_group_box.setGeometry(QtCore.QRect(90, 750, 1440, 180))
        self.horizontal_layout = QHBoxLayout(self.horizontal_group_box)

        self.size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.hand_gesture_recognition_button = QPushButton("Sign Recognition", self.horizontal_group_box)
        self.hand_gesture_recognition_icon = QIcon()

        self.new_gesture_button = QPushButton("New Sign", self.horizontal_group_box)
        self.new_gesture_icon = QIcon()

        self.train_neural_network_button = QPushButton("Train Neural Network", self.horizontal_group_box)
        self.train_neural_network_icon = QIcon()

        self.settings_button = QPushButton("Settings", self.horizontal_group_box)
        self.settings_icon = QIcon()

        self.help_button = QPushButton("Help", self.horizontal_group_box)
        self.help_icon = QIcon()

        self.setup_view()
        self.hand_gesture_recognition_button.clicked.connect(
            lambda: self.change_view(self.hand_gesture_recognition_view, "Sign Recognition"))
        self.new_gesture_button.clicked.connect(lambda: self.change_view(self.add_new_sign_view, "Add New Sign"))
        self.train_neural_network_button.clicked.connect(
            lambda: self.change_view(self.train_neural_network_view, "Train Neural Network"))
        self.settings_button.clicked.connect(lambda: self.change_view(self.settings_view, "Settings"))

    def change_view(self, current_widget, window_title):
        self.setWindowTitle(window_title)
        self.central_widget.setCurrentWidget(current_widget)

    def setup_view(self):
        self.resize(1600, 900)
        self.setWindowTitle("Hand Recognition Application")
        self.setWindowIcon(QIcon("data/icons/hand_icon"))

        self.size_policy.setHorizontalStretch(50)
        self.size_policy.setVerticalStretch(0)
        self.size_policy.setHeightForWidth(self.horizontal_group_box.sizePolicy().hasHeightForWidth())

        self.horizontal_group_box.setSizePolicy(self.size_policy)
        self.horizontal_group_box.setSizeIncrement(QtCore.QSize(40, 1))
        self.horizontal_group_box.setFlat(False)
        self.horizontal_group_box.setStyleSheet("border: none;")
        self.horizontal_layout.setSpacing(40)

        self.hand_gesture_recognition_icon.addPixmap(QPixmap("data/icons/hand_icon"), QIcon.Normal, QIcon.Off)
        self.hand_gesture_recognition_button.setIcon(self.hand_gesture_recognition_icon)
        self.hand_gesture_recognition_button.setIconSize(QtCore.QSize(50, 50))
        self.hand_gesture_recognition_button.setStyleSheet(BUTTON_STYLE_SHEET)
        self.horizontal_layout.addWidget(self.hand_gesture_recognition_button)

        self.new_gesture_icon.addPixmap(QPixmap("data/icons/add_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.new_gesture_button.setIcon(self.new_gesture_icon)
        self.new_gesture_button.setIconSize(QtCore.QSize(50, 50))
        self.new_gesture_button.setStyleSheet(BUTTON_STYLE_SHEET)
        self.horizontal_layout.addWidget(self.new_gesture_button)

        self.train_neural_network_icon.addPixmap(QPixmap("data/icons/neurons_icon.png"), QIcon.Normal, QIcon.Off)
        self.train_neural_network_button.setIcon(self.train_neural_network_icon)
        self.train_neural_network_button.setIconSize(QtCore.QSize(50, 50))
        self.train_neural_network_button.setStyleSheet(BUTTON_STYLE_SHEET)
        self.horizontal_layout.addWidget(self.train_neural_network_button)

        self.settings_icon.addPixmap(QPixmap("data/icons/settings_icon.png"), QIcon.Normal, QIcon.Off)
        self.settings_button.setIcon(self.settings_icon)
        self.settings_button.setIconSize(QtCore.QSize(50, 50))
        self.settings_button.setStyleSheet(BUTTON_STYLE_SHEET)
        self.horizontal_layout.addWidget(self.settings_button)

        self.help_icon.addPixmap(QPixmap("data/icons/help_icon.png"), QIcon.Normal, QIcon.Off)
        self.help_button.setIcon(self.help_icon)
        self.help_button.setIconSize(QtCore.QSize(50, 50))
        self.help_button.setStyleSheet(BUTTON_STYLE_SHEET)
        self.horizontal_layout.addWidget(self.help_button)

        self.setStyleSheet("background-color: #493fda;")

    @staticmethod
    def get_instance():
        if MainView._instance is None:
            MainView._instance = MainView()
        return MainView._instance

    def closeEvent(self, event):
        self.closed.emit()
        QMainWindow.closeEvent(self, event)


# noinspection PyArgumentList
class HomeView(QWidget):

    def __init__(self, parent=None):
        super(HomeView, self).__init__(parent)

        self.h_picture = QLabel(self)
        self.r_picture = QLabel(self)
        self.a_picture = QLabel(self)

        self.h_first = QLabel("H", self)
        self.h_rest = QLabel("and", self)
        self.r_first = QLabel("R", self)
        self.r_rest = QLabel("ecognition", self)
        self.a_first = QLabel("A", self)
        self.a_rest = QLabel("pplication", self)

        self.setup_view()

    def setup_view(self):
        self.h_first.setGeometry(QtCore.QRect(310, 520, 51, 61))
        self.h_first.setStyleSheet(FIRST_LETTER_LABEL_STYLE_SHEET)
        self.h_rest.setGeometry(QtCore.QRect(360, 520, 121, 61))
        self.h_rest.setStyleSheet(REST_LETTERS_LABEL_STYLE_SHEET)

        self.r_first.setGeometry(QtCore.QRect(700, 520, 51, 61))
        self.r_first.setStyleSheet(FIRST_LETTER_LABEL_STYLE_SHEET)
        self.r_rest.setGeometry(QtCore.QRect(740, 510, 351, 81))
        self.r_rest.setStyleSheet(REST_LETTERS_LABEL_STYLE_SHEET)

        self.a_first.setGeometry(QtCore.QRect(1130, 520, 51, 61))
        self.a_first.setStyleSheet(FIRST_LETTER_LABEL_STYLE_SHEET)
        self.a_rest.setGeometry(QtCore.QRect(1170, 500, 351, 91))
        self.a_rest.setStyleSheet(REST_LETTERS_LABEL_STYLE_SHEET)

        self.h_picture.setGeometry(QtCore.QRect(161, 280, 432, 230))

        self.h_picture.setPixmap(QPixmap("D:/Hand Gesture Datasets/Training/Only_Letters/Only_Letters/H/H.png"))

        self.r_picture.setGeometry(QtCore.QRect(754, 10, 242, 500))
        self.r_picture.setPixmap(QPixmap(
            "D:/Hand Gesture Datasets/Training/Only_Letters/Only_Letters/R/hand1_r_bot_seg_2_cropped.png"))

        self.a_picture.setGeometry(QtCore.QRect(1160, 130, 282, 370))
        self.a_picture.setPixmap(QPixmap("D:/Hand Gesture Datasets/Training/Only_Letters/Only_Letters/A/A.png"))



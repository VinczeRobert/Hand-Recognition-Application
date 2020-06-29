from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QStackedWidget, QGroupBox, QHBoxLayout, QSizePolicy, QPushButton, QMainWindow
from view.hand_gesture_recognition_view import HandGestureRecognitionView
from view.add_new_sign_view import AddNewSignView
from view.home_view import HomeView
from view.train_neural_network_view import TrainNeuralNetworkView
from view.settings_view import SettingsView
from view.style_sheets.main_view_stylesheet import BUTTON_STYLE_SHEET, BACKGROUND_COLOR


WINDOW_ICON = "data/icons/hand_icon"


# noinspection PyArgumentList
class MainView(QMainWindow):
    """
    Main View class of the application which containt all other views.
    """
    _instance = None

    closed = pyqtSignal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # A stacked widget is being used to switch between HomeView, HandGestureRecognitionView, AddNewGestureView,
        # TrainNeuralNetworkView and SettingsView
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.home_view = HomeView(WINDOW_ICON)
        self.settings_view = SettingsView()
        self.hand_gesture_recognition_view = HandGestureRecognitionView()
        self.add_new_sign_view = AddNewSignView()
        self.train_neural_network_view = TrainNeuralNetworkView()

        # Add the mentioned views
        self.central_widget.addWidget(self.home_view)
        self.central_widget.addWidget(self.settings_view)
        self.central_widget.addWidget(self.hand_gesture_recognition_view)
        self.central_widget.addWidget(self.add_new_sign_view)
        self.central_widget.addWidget(self.train_neural_network_view)

        # Home View is seen by default when the application opens
        self.central_widget.setCurrentWidget(self.home_view)

        self.horizontal_group_box = QGroupBox(self)
        self.horizontal_layout = QHBoxLayout(self.horizontal_group_box)

        self.size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.home_button = QPushButton("Home")
        self.home_icon = QIcon()

        self.hand_gesture_recognition_button = QPushButton("Sign Recognition")
        self.hand_gesture_recognition_icon = QIcon()

        self.new_gesture_button = QPushButton("New Sign")
        self.new_gesture_icon = QIcon()

        self.train_neural_network_button = QPushButton("Train Neural Network")
        self.train_neural_network_icon = QIcon()

        self.settings_button = QPushButton("Settings")
        self.settings_icon = QIcon()

        self.setup_view()
        self.home_button.clicked.connect(lambda: self.change_view(self.home_view, "Home"))
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
        self.setWindowIcon(QIcon(WINDOW_ICON))

        self.size_policy.setHorizontalStretch(50)
        self.size_policy.setVerticalStretch(0)
        self.size_policy.setHeightForWidth(self.horizontal_group_box.sizePolicy().hasHeightForWidth())

        self.horizontal_group_box.setGeometry(QtCore.QRect(90, 750, 1440, 180))
        self.horizontal_group_box.setSizePolicy(self.size_policy)
        self.horizontal_group_box.setSizeIncrement(QtCore.QSize(40, 1))
        self.horizontal_group_box.setFlat(False)
        self.horizontal_group_box.setStyleSheet("border: none;")
        self.horizontal_layout.setSpacing(40)

        self.home_icon.addPixmap(QPixmap("data/icons/home_icon.png"), QIcon.Normal, QIcon.Off)
        self.home_button.setIcon(self.home_icon)
        self.home_button.setIconSize(QtCore.QSize(50, 50))
        self.home_button.setStyleSheet(BUTTON_STYLE_SHEET)
        self.horizontal_layout.addWidget(self.home_button)

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

        self.setStyleSheet(BACKGROUND_COLOR)

    @staticmethod
    def get_instance():
        if MainView._instance is None:
            MainView._instance = MainView()
        return MainView._instance

    def closeEvent(self, event):
        self.closed.emit()
        QMainWindow.closeEvent(self, event)
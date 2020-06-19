from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction

from view.add_new_sign_view import AddNewSignView
from view.hand_gesture_recognition_view import HandGestureRecognitionView
from view.settings_view import SettingsView
from view.style_sheets.main_view_stylesheet import MAIN_WINDOW_STYLE_SHEET, MAIN_BUTTON_STYLE_SHEET, \
    MAIN_PICTURE_STYLE_SHEET, REST_LETTERS_LABEL_STYLE_SHEET, FIRST_LETTERS_LABEL_STYLE_SHEET, NO_BORDER_STYLE_SHEET, \
    HOVER_ON_BUTTONS_STYLE_SHEET


# noinspection PyArgumentList
from view.train_neural_network_view import TrainNeuralNetworkView


class MainView(QtWidgets.QMainWindow):
    _instance = None

    closed = pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.central_widget = QtWidgets.QStackedWidget()
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

        self.horizontal_group_box = QtWidgets.QGroupBox(self)
        self.horizontal_group_box.setGeometry(QtCore.QRect(90, 750, 1440, 180))
        self.horizontal_layout = QtWidgets.QHBoxLayout(self.horizontal_group_box)

        self.size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.hand_gesture_recognition_button = QtWidgets.QPushButton(self.horizontal_group_box)
        self.hand_gesture_recognition_icon = QtGui.QIcon()

        self.settings_button = QtWidgets.QPushButton(self.horizontal_group_box)
        self.settings_icon = QtGui.QIcon()

        self.train_neural_network_button = QtWidgets.QPushButton(self.horizontal_group_box)
        self.train_neural_network_icon = QtGui.QIcon()

        self.new_gesture_button = QtWidgets.QPushButton(self.horizontal_group_box)
        self.new_gesture_icon = QtGui.QIcon()

        self.help_button = QtWidgets.QPushButton(self.horizontal_group_box)
        self.help_icon = QtGui.QIcon()

        self.setup_window()
        self.settings_button.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.settings_view))
        self.hand_gesture_recognition_button.clicked.connect(lambda: self.central_widget.setCurrentWidget(
            self.hand_gesture_recognition_view))
        self.new_gesture_button.clicked.connect(lambda: self.central_widget.setCurrentWidget(
            self.add_new_sign_view
        ))
        self.train_neural_network_button.clicked.connect(lambda: self.central_widget.setCurrentWidget(
            self.train_neural_network_view))

    def setup_window(self):
        self.setObjectName("main_window")
        self.resize(1600, 900)
        self.setStyleSheet(MAIN_WINDOW_STYLE_SHEET)

        self.central_widget.setObjectName("central_widget")

        self.size_policy.setHorizontalStretch(50)
        self.size_policy.setVerticalStretch(0)
        self.size_policy.setHeightForWidth(self.horizontal_group_box.sizePolicy().hasHeightForWidth())
        self.horizontal_group_box.setSizePolicy(self.size_policy)
        self.horizontal_group_box.setStyleSheet(HOVER_ON_BUTTONS_STYLE_SHEET)
        self.horizontal_group_box.setSizeIncrement(QtCore.QSize(40, 1))
        self.horizontal_group_box.setFlat(False)
        self.horizontal_group_box.setObjectName("horizontal_group_box")
        self.horizontal_layout.setSpacing(40)
        self.horizontal_layout.setObjectName("horizontal_layout")

        self.hand_gesture_recognition_button.setAutoFillBackground(False)
        self.hand_gesture_recognition_button.setStyleSheet(MAIN_BUTTON_STYLE_SHEET)
        self.hand_gesture_recognition_icon.addPixmap(QtGui.QPixmap("data/icons/hand_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hand_gesture_recognition_button.setIcon(self.hand_gesture_recognition_icon)
        self.hand_gesture_recognition_button.setIconSize(QtCore.QSize(50, 50))
        self.hand_gesture_recognition_button.setObjectName("hand_gesture_recognition_button")
        self.hand_gesture_recognition_button.setFlat(False)
        self.horizontal_layout.addWidget(self.hand_gesture_recognition_button)

        self.new_gesture_button.setAutoFillBackground(False)
        self.new_gesture_button.setStyleSheet(MAIN_BUTTON_STYLE_SHEET)
        self.new_gesture_icon.addPixmap(QtGui.QPixmap("data/icons/add_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.new_gesture_button.setIcon(self.new_gesture_icon)
        self.new_gesture_button.setIconSize(QtCore.QSize(50, 50))
        self.new_gesture_button.setFlat(False)
        self.new_gesture_button.setObjectName("new_gesture_button")
        self.horizontal_layout.addWidget(self.new_gesture_button)

        self.train_neural_network_button.setAutoFillBackground(False)
        self.train_neural_network_button.setStyleSheet(MAIN_BUTTON_STYLE_SHEET)
        self.train_neural_network_icon.addPixmap(QtGui.QPixmap("data/icons/neurons_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.train_neural_network_button.setIcon(self.train_neural_network_icon)
        self.train_neural_network_button.setIconSize(QtCore.QSize(50, 50))
        self.train_neural_network_button.setFlat(False)
        self.train_neural_network_button.setObjectName("train_neural_network_button")
        self.horizontal_layout.addWidget(self.train_neural_network_button)

        self.settings_button.setAutoFillBackground(False)
        self.settings_button.setStyleSheet(MAIN_BUTTON_STYLE_SHEET)
        self.settings_icon.addPixmap(QtGui.QPixmap("data/icons/settings_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings_button.setIcon(self.settings_icon)
        self.settings_button.setIconSize(QtCore.QSize(50, 50))
        self.settings_button.setFlat(False)
        self.settings_button.setObjectName("settings_button")
        self.horizontal_layout.addWidget(self.settings_button)

        self.help_button.setAutoFillBackground(False)
        self.help_button.setStyleSheet(MAIN_BUTTON_STYLE_SHEET)
        self.help_icon.addPixmap(QtGui.QPixmap("data/icons/help_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.help_button.setIcon(self.help_icon)
        self.help_button.setIconSize(QtCore.QSize(50, 50))
        self.help_button.setFlat(False)
        self.help_button.setObjectName("help_button")
        self.horizontal_layout.addWidget(self.help_button)

        self.retranslate_window()

    def retranslate_window(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Hand Recognition Application"))
        self.hand_gesture_recognition_button.setText(_translate("self", "Sign Recognition"))
        self.settings_button.setText(_translate("self", "Settings"))
        self.train_neural_network_button.setText(_translate("self", "Train Neural Network"))
        self.new_gesture_button.setText(_translate("self", "New Sign"))
        self.help_button.setText(_translate("self", "Help"))

    @staticmethod
    def get_instance():
        if MainView._instance is None:
            MainView._instance = MainView()
        return MainView._instance

    def closeEvent(self, event):
        self.closed.emit()
        QtWidgets.QMainWindow.closeEvent(self, event)


# noinspection PyArgumentList
class HomeView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(HomeView, self).__init__(parent)

        self.h_picture = QtWidgets.QLabel(self)
        self.r_picture = QtWidgets.QLabel(self)
        self.a_picture = QtWidgets.QLabel(self)

        self.h_first = QtWidgets.QLabel(self)
        self.h_rest = QtWidgets.QLabel(self)
        self.r_first = QtWidgets.QLabel(self)
        self.r_rest = QtWidgets.QLabel(self)
        self.a_first = QtWidgets.QLabel(self)
        self.a_rest = QtWidgets.QLabel(self)

        self.setup_page()

    def setup_page(self):
        self.h_first.setGeometry(QtCore.QRect(310, 520, 51, 61))
        self.h_first.setStyleSheet(FIRST_LETTERS_LABEL_STYLE_SHEET)
        self.h_first.setObjectName("h_first")
        self.h_rest.setGeometry(QtCore.QRect(360, 520, 121, 61))
        self.h_rest.setStyleSheet(REST_LETTERS_LABEL_STYLE_SHEET)
        self.h_rest.setObjectName("h_rest")

        self.r_first.setGeometry(QtCore.QRect(700, 520, 51, 61))
        self.r_first.setStyleSheet(FIRST_LETTERS_LABEL_STYLE_SHEET)
        self.r_first.setObjectName("r_first")
        self.r_rest.setGeometry(QtCore.QRect(740, 510, 351, 81))
        self.r_rest.setStyleSheet(REST_LETTERS_LABEL_STYLE_SHEET)
        self.r_rest.setObjectName("r_rest")

        self.a_first.setGeometry(QtCore.QRect(1130, 520, 51, 61))
        self.a_first.setStyleSheet(FIRST_LETTERS_LABEL_STYLE_SHEET)
        self.a_first.setObjectName("a_first")
        self.a_rest.setGeometry(QtCore.QRect(1170, 500, 351, 91))
        self.a_rest.setStyleSheet(REST_LETTERS_LABEL_STYLE_SHEET)
        self.a_rest.setObjectName("a_rest")

        self.h_picture.setGeometry(QtCore.QRect(161, 280, 432, 230))
        self.h_picture.setStyleSheet(MAIN_PICTURE_STYLE_SHEET)
        self.h_picture.setText("")
        self.h_picture.setPixmap(QtGui.QPixmap("D:/Hand Gesture Datasets/Training/Only_Letters/Only_Letters/H/H.png"))
        self.h_picture.setObjectName("h_picture")

        self.r_picture.setGeometry(QtCore.QRect(754, 10, 242, 500))
        self.r_picture.setStyleSheet(MAIN_PICTURE_STYLE_SHEET)
        self.r_picture.setText("")
        self.r_picture.setPixmap(QtGui.QPixmap(
            "D:/Hand Gesture Datasets/Training/Only_Letters/Only_Letters/R/hand1_r_bot_seg_2_cropped.png"))
        self.r_picture.setObjectName("r_picture")

        self.a_picture.setGeometry(QtCore.QRect(1160, 130, 282, 370))
        self.a_picture.setStyleSheet(MAIN_PICTURE_STYLE_SHEET)
        self.a_picture.setText("")
        self.a_picture.setPixmap(QtGui.QPixmap("D:/Hand Gesture Datasets/Training/Only_Letters/Only_Letters/A/A.png"))
        self.a_picture.setObjectName("a_picture")

        self.retranslate_page()

    def retranslate_page(self):
        _translate = QtCore.QCoreApplication.translate
        self.h_first.setText(_translate("self", "H"))
        self.h_rest.setText(_translate("self", "and"))
        self.r_first.setText(_translate("self", "R"))
        self.r_rest.setText(_translate("self", "ecognition"))
        self.a_first.setText(_translate("self", "A"))
        self.a_rest.setText(_translate("self", "pplication"))



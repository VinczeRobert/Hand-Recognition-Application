# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_page.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from view.style_sheets.main_view_stylesheet import MAIN_WINDOW_STYLE_SHEET, MAIN_BUTTON_STYLE_SHEET


class MainView(object):
    def __init__(self):
        self.main_window = QtWidgets.QMainWindow()
        self.central_widget = QtWidgets.QWidget(self.main_window)

        self.hand_gesture_recognition_button = QtWidgets.QPushButton(self.central_widget)
        self.hand_gesture_recognition_icon = QtGui.QIcon()

        self.settings_button = QtWidgets.QPushButton(self.central_widget)
        self.settings_icon = QtGui.QIcon()

        self.train_neural_network_button = QtWidgets.QPushButton(self.central_widget)
        self.train_neural_network_icon = QtGui.QIcon()

        self.new_gesture_button = QtWidgets.QPushButton(self.central_widget)
        self.new_gesture_icon = QtGui.QIcon()

        self.help_button = QtWidgets.QPushButton(self.central_widget)
        self.help_icon = QtGui.QIcon()


    def setup_window(self):
        self.main_window.setObjectName("main_window")
        main_window.resize(1600, 900)
        main_window.setStyleSheet(MAIN_WINDOW_STYLE_SHEET)

        self.central_widget.setObjectName("central_widget")

        self.hand_gesture_recognition_button.setGeometry(QtCore.QRect(100, 750, 200, 80))
        self.hand_gesture_recognition_button.setAutoFillBackground(False)
        self.hand_gesture_recognition_button.setStyleSheet(MAIN_BUTTON_STYLE_SHEET)
        self.hand_gesture_recognition_icon.addPixmap(QtGui.QPixmap("../License Figures/324-3249426_click-hand-icon-png-transparent-png.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hand_gesture_recognition_button.setIcon(self.hand_gesture_recognition_icon)
        self.hand_gesture_recognition_button.setIconSize(QtCore.QSize(50, 50))
        self.hand_gesture_recognition_button.setFlat(False)
        self.hand_gesture_recognition_button.setObjectName("hand_gesture_recognition_button")

        self.settings_button.setGeometry(QtCore.QRect(1000, 750, 200, 80))
        self.settings_button.setAutoFillBackground(False)
        self.settings_button.setStyleSheet(MAIN_BUTTON_STYLE_SHEET)
        self.settings_icon.addPixmap(QtGui.QPixmap("../License Figures/Windows_Settings_app_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings_button.setIcon(self.settings_icon)
        self.settings_button.setIconSize(QtCore.QSize(50, 50))
        self.settings_button.setFlat(False)
        self.settings_button.setObjectName("settings_button")

        self.train_neural_network_button.setGeometry(QtCore.QRect(700, 750, 200, 80))
        self.train_neural_network_button.setAutoFillBackground(False)
        self.train_neural_network_button.setStyleSheet(MAIN_BUTTON_STYLE_SHEET)
        self.train_neural_network_icon.addPixmap(QtGui.QPixmap("../License Figures/873053-200.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.train_neural_network_button.setIcon(self.train_neural_network_icon)
        self.train_neural_network_button.setIconSize(QtCore.QSize(50, 50))
        self.train_neural_network_button.setFlat(False)
        self.train_neural_network_button.setObjectName("train_neural_network_button")

        self.new_gesture_button.setGeometry(QtCore.QRect(400, 750, 200, 80))
        self.new_gesture_button.setAutoFillBackground(False)
        self.new_gesture_button.setStyleSheet(MAIN_BUTTON_STYLE_SHEET)
        self.new_gesture_icon.addPixmap(QtGui.QPixmap("../License Figures/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.new_gesture_button.setIcon(self.new_gesture_icon)
        self.new_gesture_button.setIconSize(QtCore.QSize(50, 50))
        self.new_gesture_button.setFlat(False)
        self.new_gesture_button.setObjectName("new_gesture_button")


        self.help_button.setGeometry(QtCore.QRect(1300, 750, 200, 80))
        self.help_button.setAutoFillBackground(False)
        self.help_button.setStyleSheet(MAIN_BUTTON_STYLE_SHEET)

        self.help_icon.addPixmap(QtGui.QPixmap("../License Figures/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.help_button.setIcon(self.help_icon)
        self.help_button.setIconSize(QtCore.QSize(50, 50))
        self.help_button.setFlat(False)
        self.help_button.setObjectName("help_button")

        self.h_label = QtWidgets.QLabel(self.centralwidget)
        self.h_label.setGeometry(QtCore.QRect(161, 280, 432, 230))
        self.h_label.setStyleSheet("background-color: white;")
        self.h_label.setText("")
        self.h_label.setPixmap(QtGui.QPixmap("D:/Hand Gesture Datasets/Training/Only_Letters/Only_Letters/H/H.png"))
        self.h_label.setObjectName("h_label")
        self.r_label = QtWidgets.QLabel(self.centralwidget)
        self.r_label.setGeometry(QtCore.QRect(754, 10, 242, 500))
        self.r_label.setStyleSheet("background-color: white;")
        self.r_label.setText("")
        self.r_label.setPixmap(QtGui.QPixmap("D:/Hand Gesture Datasets/Training/Only_Letters/Only_Letters/R/hand1_r_bot_seg_2_cropped.png"))
        self.r_label.setObjectName("r_label")
        self.a_label = QtWidgets.QLabel(self.centralwidget)
        self.a_label.setGeometry(QtCore.QRect(1160, 130, 282, 370))
        self.a_label.setStyleSheet("background-color: white;")
        self.a_label.setText("")
        self.a_label.setPixmap(QtGui.QPixmap("D:/Hand Gesture Datasets/Training/Only_Letters/Only_Letters/A/A.png"))
        self.a_label.setObjectName("a_label")
        self.first_let = QtWidgets.QLabel(self.centralwidget)
        self.first_let.setGeometry(QtCore.QRect(310, 520, 51, 61))
        self.first_let.setStyleSheet("font-size: 70px;")
        self.first_let.setObjectName("first_let")
        self.h_rest = QtWidgets.QLabel(self.centralwidget)
        self.h_rest.setGeometry(QtCore.QRect(360, 520, 121, 61))
        self.h_rest.setStyleSheet("font-size: 70px;\n"
"color: white;\n"
"")
        self.h_rest.setObjectName("h_rest")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(700, 520, 51, 61))
        self.label_6.setStyleSheet("font-size: 70px;")
        self.label_6.setObjectName("label_6")
        self.r_rest = QtWidgets.QLabel(self.centralwidget)
        self.r_rest.setGeometry(QtCore.QRect(740, 510, 351, 81))
        self.r_rest.setStyleSheet("font-size: 70px;\n"
"color: white;\n"
"")
        self.r_rest.setObjectName("r_rest")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(1130, 520, 51, 61))
        self.label_8.setStyleSheet("font-size: 70px;")
        self.label_8.setObjectName("label_8")
        self.a_rest = QtWidgets.QLabel(self.centralwidget)
        self.a_rest.setGeometry(QtCore.QRect(1170, 500, 351, 91))
        self.a_rest.setStyleSheet("font-size: 70px;\n"
"color: white;\n"
"")
        self.a_rest.setObjectName("a_rest")
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1598, 26))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Hand Recognition Application"))
        self.hand_gesture_recognition_button.setText(_translate("main_window", "Sign Recognition"))
        self.settings_button.setText(_translate("main_window", "Settings"))
        self.train_neural_network_button.setText(_translate("main_window", "Train Neural Network"))
        self.new_gesture_button.setText(_translate("main_window", "New Sign"))
        self.help_button.setText(_translate("main_window", "Help"))
        self.first_let.setText(_translate("main_window", "H"))
        self.h_rest.setText(_translate("main_window", "and"))
        self.label_6.setText(_translate("main_window", "R"))
        self.r_rest.setText(_translate("main_window", "ecognition"))
        self.label_8.setText(_translate("main_window", "A"))
        self.a_rest.setText(_translate("main_window", "pplication"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_main_window()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())


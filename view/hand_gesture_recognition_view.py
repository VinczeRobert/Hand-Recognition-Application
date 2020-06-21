from PyQt5 import QtCore, QtWidgets
from view.hand_graphics_view import HandGraphicsView
from view.style_sheets.main_view_stylesheet import BUTTON_STYLE_SHEET


# noinspection PyArgumentList
class HandGestureRecognitionView(HandGraphicsView):

    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self):
        super(HandGestureRecognitionView, self).__init__()

        self.load_text_button = QtWidgets.QPushButton("Load text", self)
        self.save_text_button = QtWidgets.QPushButton("Save text", self)
        self.save_background_button = QtWidgets.QPushButton("Set Background", self)

        self.setup_view()

    def setup_view(self):
        super(HandGestureRecognitionView, self).setup_view()

        self.load_text_button.setGeometry(QtCore.QRect(1340, 50, 150, 60))
        self.save_text_button.setGeometry(QtCore.QRect(1340, 170, 150, 60))
        self.save_background_button.setGeometry(QtCore.QRect(1340, 290, 150, 60))

        self.setStyleSheet(BUTTON_STYLE_SHEET)





from PyQt5 import QtCore, QtWidgets, QtGui
from view.style_sheets.main_view_stylesheet import MAIN_BUTTON_STYLE_SHEET


# noinspection PyArgumentList
class HandRecognitionView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(HandRecognitionView, self).__init__(parent)

        self.recognition_graphics_view = QtWidgets.QGraphicsView(self)

        self.load_text_button = QtWidgets.QPushButton(self)
        self.save_text_button = QtWidgets.QPushButton(self)

        self.setup_page()

    def setup_page(self):
        self.recognition_graphics_view.setGeometry(QtCore.QRect(0, 0, 1200, 700))
        self.recognition_graphics_view.setObjectName("recognition_graphics_view")

        self.load_text_button.setGeometry(QtCore.QRect(1240, 50, 150, 60))
        self.load_text_button.setStyleSheet(MAIN_BUTTON_STYLE_SHEET)
        self.load_text_button.setObjectName("load_text_button")

        self.save_text_button.setGeometry(QtCore.QRect(1240, 170, 150, 60))
        self.save_text_button.setStyleSheet(MAIN_BUTTON_STYLE_SHEET)
        self.save_text_button.setObjectName("save_text_button")

        self.retranslate_view()

    def retranslate_view(self):
        _translate = QtCore.QCoreApplication.translate
        self.load_text_button.setText(_translate("self", "Load Text"))
        self.save_text_button.setText(_translate("self", "Save Text"))

    def update_frame(self, image):
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        new_image = QtGui.QPixmap(qImg)
        self.pixmap.setPixmap(new_image)


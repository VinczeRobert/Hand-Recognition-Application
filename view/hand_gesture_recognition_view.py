from PyQt5 import QtCore, QtWidgets, QtGui
from view.style_sheets.main_view_stylesheet import MAIN_BUTTON_STYLE_SHEET, SOLID_BORDER_STYLE_SHEET


# noinspection PyArgumentList
class HandGestureRecognitionView(QtWidgets.QWidget):

    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(HandGestureRecognitionView, self).__init__(parent)

        self.recognition_graphics_view = QtWidgets.QGraphicsView(self)
        self.recognition_graphics_scene = QtWidgets.QGraphicsScene()
        self.pixmap = QtWidgets.QGraphicsPixmapItem()

        self.load_text_button = QtWidgets.QPushButton(self)
        self.save_text_button = QtWidgets.QPushButton(self)

        self.setup_page()

    def setup_page(self):
        self.recognition_graphics_view.setGeometry(QtCore.QRect(0, 0, 1285, 725))
        self.recognition_graphics_view.setObjectName("recognition_graphics_view")

        self.recognition_graphics_scene.addItem(self.pixmap)
        self.recognition_graphics_view.setScene(self.recognition_graphics_scene)
        # self.recognition_graphics_view.setStyleSheet(SOLID_BORDER_STYLE_SHEET)

        self.load_text_button.setGeometry(QtCore.QRect(1340, 50, 150, 60))
        self.load_text_button.setStyleSheet(MAIN_BUTTON_STYLE_SHEET)
        self.load_text_button.setObjectName("load_text_button")

        self.save_text_button.setGeometry(QtCore.QRect(1340, 170, 150, 60))
        self.save_text_button.setStyleSheet(MAIN_BUTTON_STYLE_SHEET)
        self.save_text_button.setObjectName("save_text_button")

        self.retranslate_view()

    def retranslate_view(self):
        _translate = QtCore.QCoreApplication.translate
        self.load_text_button.setText(_translate("self", "Load Text"))
        self.save_text_button.setText(_translate("self", "Save Text"))

    def keyPressEvent(self, key_event):
        super(HandGestureRecognitionView, self).keyPressEvent(key_event)
        self.keyPressed.emit(key_event.key())

    def update_frame(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        qImg = QtGui.QImage(image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        new_image = QtGui.QPixmap(qImg)
        self.pixmap.setPixmap(new_image)


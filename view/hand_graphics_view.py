from PyQt5.QtCore import pyqtSignal, QRect
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem


# noinspection PyArgumentList
class HandGraphicsView(QWidget):
    """
    This class is the superclass of AddNewSignView and HandGestureRecognitionView
    It contains the frame for displaying the recording results which is a common part
    """

    keyPressed = pyqtSignal(int)

    def __init__(self, parent=None):
        super(HandGraphicsView, self).__init__(parent)

        self.graphics_view = QGraphicsView(self)
        self.graphics_scene = QGraphicsScene()
        self.pixmap = QGraphicsPixmapItem()

    def setup_view(self):
        self.graphics_scene.addItem(self.pixmap)

        self.graphics_view.setGeometry(QRect(0, 0, 1285, 725))
        self.graphics_view.setScene(self.graphics_scene)

    def keyPressEvent(self, key_event):
        super(HandGraphicsView, self).keyPressEvent(key_event)
        self.keyPressed.emit(key_event.key())

    def update_frame(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        new_image = QPixmap(q_image)
        self.pixmap.setPixmap(new_image)
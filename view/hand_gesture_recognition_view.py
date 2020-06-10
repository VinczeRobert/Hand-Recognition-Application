from PyQt5 import QtCore, QtGui, QtWidgets


class HandGestureRecognitionView:
    def __init__(self):
        self.main_window = QtWidgets.QMainWindow()
        self.central_widget = QtWidgets.QWidget(self.main_window)

        self.graphics_view = QtWidgets.QGraphicsView(self.central_widget)
        self.graphics_scene = QtWidgets.QGraphicsScene()
        self.pixmap = QtWidgets.QGraphicsPixmapItem()

        self.menu_bar = QtWidgets.QMenuBar(self.main_window)
        self.status_bar = QtWidgets.QStatusBar(self.main_window)
        self.prediction_button = QtWidgets.QPushButton(self.central_widget)

        self.setup_window()

    def setup_window(self):
        self.main_window.setObjectName("MainView")
        self.main_window.resize(1400, 900)

        self.central_widget.setObjectName("centralWidget")

        self.graphics_view.setGeometry(QtCore.QRect(0, 0, 1200, 700))
        self.graphics_view.setObjectName("graphicsView")
        self.main_window.setCentralWidget(self.central_widget)

        self.graphics_scene.addItem(self.pixmap)
        self.graphics_view.setScene(self.graphics_scene)

        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menu_bar.setObjectName("menuBar")
        self.main_window.setMenuBar(self.menu_bar)

        self.status_bar.setObjectName("statusBar")
        self.main_window.setStatusBar(self.status_bar)

        self.prediction_button.setGeometry(QtCore.QRect(540, 730, 121, 41))
        self.prediction_button.setObjectName("predictionButton")

        self.retranslate_window()
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def retranslate_window(self):
        _translate = QtCore.QCoreApplication.translate
        self.main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def update_frame(self, image):
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        new_image = QtGui.QPixmap(qImg)
        self.pixmap.setPixmap(new_image)



import os

from PyQt5 import QtCore, QtGui, QtWidgets
from view.style_sheets.main_view_stylesheet import MAIN_BUTTON_STYLE_SHEET, FORM_GROUP_BOX_STYLE_SHEET

# noinspection PyArgumentList
class AddNewSignView(QtWidgets.QWidget):

    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(AddNewSignView, self).__init__(parent)

        self.new_sign_graphics_view = QtWidgets.QGraphicsView(self)
        self.new_sign_graphics_scene = QtWidgets.QGraphicsScene()
        self.pixmap = QtWidgets.QGraphicsPixmapItem()

        self.load_text_button = QtWidgets.QPushButton(self)
        self.start_saving_button = QtWidgets.QPushButton(self)

        self.form_group_box = QtWidgets.QGroupBox(self)
        self.form_layout = QtWidgets.QFormLayout(self.form_group_box)

        self.class_name_label = QtWidgets.QLabel(self.form_group_box)
        self.class_name_line_edit = QtWidgets.QLineEdit(self.form_group_box)
        self.start_index_label = QtWidgets.QLabel(self.form_group_box)
        self.start_index_line_edit = QtWidgets.QLineEdit(self.form_group_box)
        self.end_index_label = QtWidgets.QLabel(self.form_group_box)
        self.end_index_line_edit = QtWidgets.QLineEdit(self.form_group_box)

        self.download_path_label = QtWidgets.QLabel(self)

        self.setup_page()

    def setup_page(self):
        self.new_sign_graphics_view.setGeometry(QtCore.QRect(0, 0, 1285, 725))
        self.new_sign_graphics_view.setObjectName("new_sign_graphics_view")

        self.new_sign_graphics_scene.addItem(self.pixmap)
        self.new_sign_graphics_view.setScene(self.new_sign_graphics_scene)

        self.load_text_button.setGeometry(QtCore.QRect(1300, 50, 150, 60))
        self.load_text_button.setStyleSheet(MAIN_BUTTON_STYLE_SHEET)
        self.load_text_button.setObjectName("load_text_button")

        self.form_group_box.setGeometry(QtCore.QRect(1300, 230, 311, 161))
        self.form_group_box.setStyleSheet(FORM_GROUP_BOX_STYLE_SHEET)
        self.form_group_box.setObjectName("form_group_box")

        self.form_layout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.form_layout.setFormAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.form_layout.setVerticalSpacing(20)
        self.form_layout.setObjectName("form_layout")

        self.class_name_line_edit.setStyleSheet("border: 5px solid black;")
        self.class_name_line_edit.setObjectName("class_name_line_edit")
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.class_name_line_edit)
        self.start_index_label.setObjectName("start_index_label")
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.start_index_label)
        self.start_index_line_edit.setStyleSheet("border: 5px solid black;")
        self.start_index_line_edit.setObjectName("start_index_line_edit")
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.start_index_line_edit)
        self.end_index_label.setObjectName("end_index_label")
        self.form_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.end_index_label)
        self.end_index_line_edit.setStyleSheet("border: 5px solid black;")
        self.end_index_line_edit.setObjectName("end_index_line_edit")
        self.form_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.end_index_line_edit)

        self.start_saving_button.setGeometry(QtCore.QRect(1300, 400, 150, 60))
        self.start_saving_button.setStyleSheet(MAIN_BUTTON_STYLE_SHEET)
        self.start_saving_button.setObjectName("start_saving_button")

        self.download_path_label.setGeometry(QtCore.QRect(1300, 120, 241, 36))
        self.download_path_label.setStyleSheet("font-size: 20px;")
        self.download_path_label.setObjectName("class_name_label_2")

        self.retranslate_view()

    def retranslate_view(self):
        _translate = QtCore.QCoreApplication.translate
        self.load_text_button.setText(_translate("self", "Select Path"))
        self.class_name_label.setText(_translate("self", "Class name:"))
        self.start_index_label.setText(_translate("self", "Start index:"))
        self.start_saving_button.setText(_translate("self", "Start"))
        self.end_index_label.setText(_translate("self", "End index:"))
        self.download_path_label.setText(_translate("self", "No path has been chosen."))

    def keyPressEvent(self, key_event):
        super(AddNewSignView, self).keyPressEvent(key_event)
        self.keyPressed.emit(key_event.key())

    def update_frame(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        qImg = QtGui.QImage(image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        new_image = QtGui.QPixmap(qImg)
        self.pixmap.setPixmap(new_image)

    def choose_folder(self):
        dialog = QtWidgets.QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Folder")
        self.download_path_label.setText(os.path.basename(folder_path))
        return folder_path

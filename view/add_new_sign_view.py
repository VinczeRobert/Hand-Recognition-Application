import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QGroupBox, QFormLayout, QLabel, QLineEdit
from view.dialogs import choose_folder
from view.hand_graphics_view import HandGraphicsView
from view.style_sheets.main_view_stylesheet import BUTTON_STYLE_SHEET, LINE_EDIT_STYLE_SHEET, LABEL_STYLE_SHEET


# noinspection PyArgumentList
class AddNewSignView(HandGraphicsView):
    """
    View class used for displaying the Add New Gesture submenu
    """

    def __init__(self):
        super(AddNewSignView, self).__init__()

        self.load_text_button = QPushButton("Select Path", self)
        self.start_saving_button = QPushButton("Start", self)
        self.save_background_button = QPushButton("Set Background", self)

        self.form_group_box = QGroupBox(self)
        self.form_layout = QFormLayout(self.form_group_box)

        self.class_name_label = QLabel("Class name *:", self.form_group_box)
        self.class_name_line_edit = QLineEdit(self.form_group_box)
        self.start_index_label = QLabel("Start index *: ", self.form_group_box)
        self.start_index_line_edit = QLineEdit(self.form_group_box)
        self.end_index_label = QLabel("End index *: ",self.form_group_box)
        self.end_index_line_edit = QLineEdit(self.form_group_box)

        self.download_path_label = QLabel("No path has been chosen", self)

        self.setup_view()

    def setup_view(self):
        super(AddNewSignView, self).setup_view()
        self.load_text_button.setGeometry(QtCore.QRect(1300, 50, 150, 60))
        self.load_text_button.setStyleSheet(BUTTON_STYLE_SHEET)

        self.start_saving_button.setGeometry(QtCore.QRect(1300, 400, 150, 60))
        self.start_saving_button.setStyleSheet(BUTTON_STYLE_SHEET)

        self.save_background_button.setGeometry(QtCore.QRect(1300, 500, 150, 60))
        self.save_background_button.setStyleSheet(BUTTON_STYLE_SHEET)

        self.form_group_box.setGeometry(QtCore.QRect(1300, 230, 310, 160))
        self.form_group_box.setStyleSheet("border: none;")

        self.form_layout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.form_layout.setFormAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.form_layout.setVerticalSpacing(20)

        self.form_layout.setWidget(0, QFormLayout.LabelRole, self.class_name_label)
        self.form_layout.setWidget(0, QFormLayout.FieldRole, self.class_name_line_edit)
        self.form_layout.setWidget(1, QFormLayout.LabelRole, self.start_index_label)
        self.form_layout.setWidget(1, QFormLayout.FieldRole, self.start_index_line_edit)
        self.form_layout.setWidget(2, QFormLayout.LabelRole, self.end_index_label)
        self.form_layout.setWidget(2, QFormLayout.FieldRole, self.end_index_line_edit)

        self.class_name_label.setStyleSheet(LABEL_STYLE_SHEET)
        self.class_name_line_edit.setStyleSheet(LINE_EDIT_STYLE_SHEET)
        self.start_index_label.setStyleSheet(LABEL_STYLE_SHEET)
        self.start_index_line_edit.setStyleSheet(LINE_EDIT_STYLE_SHEET)
        self.end_index_label.setStyleSheet(LABEL_STYLE_SHEET)
        self.end_index_line_edit.setStyleSheet(LINE_EDIT_STYLE_SHEET)

        self.download_path_label.setGeometry(QtCore.QRect(1300, 120, 240, 35))
        self.download_path_label.setStyleSheet(LABEL_STYLE_SHEET)

    def choose_new_gesture_folder(self):
        folder_path = choose_folder('Select Folder For Creating New Gesture')
        if folder_path != '':
            self.download_path_label.setText(os.path.basename(folder_path))
            return folder_path
        return None

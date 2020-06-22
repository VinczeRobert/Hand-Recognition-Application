from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QCheckBox, QFormLayout, QLabel, QLineEdit, QRadioButton
from model.settings import HAND, IMAGE_TYPE
from view.style_sheets.main_view_stylesheet import LABEL_STYLE_SHEET, LINE_EDIT_STYLE_SHEET, GROUP_BOX_STYLE_SHEET


# noinspection PyArgumentList
class SettingsView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(SettingsView, self).__init__(parent)

        self.vertical_group_box = QGroupBox(self)
        self.vertical_layout = QVBoxLayout(self.vertical_group_box)

        self.form_group_box = QGroupBox(self)
        self.form_layout = QFormLayout(self.form_group_box)

        self.filtered_checkbox = QCheckBox("Filtered Image")
        self.background_difference_checkbox = QCheckBox("Background Difference Image")
        self.extracted_hand_checkbox = QCheckBox("Extracted Binary Hand Image")
        self.opened_hand_checkbox = QCheckBox("Opened Hand Image")
        self.contoured_checkbox = QCheckBox("Contoured Image")
        self.final_checkbox = QCheckBox("Final Image")

        self.intermediary_steps_label = QLabel("Show Intermediary Steps", self)
        self.android_server_url_label = QLabel("Android Server URL", self.form_group_box)
        self.hand_label = QLabel("Choose Hand", self)
        self.image_type_label = QLabel("Choose Image Type", self)

        self.android_server_url_line_edit = QLineEdit(self.form_group_box)

        self.hand_vertical_box = QGroupBox(self)
        self.image_type_vertical_box = QGroupBox(self)

        self.right_hand_radio_button = QRadioButton("Right Hand", self.hand_vertical_box)
        self.left_hand_radio_button = QRadioButton("Left Hand", self.hand_vertical_box)
        self.rgb_image_radio_button = QRadioButton("RGB Images", self.image_type_vertical_box)
        self.binary_image_radio_button = QRadioButton("Binary Images", self.image_type_vertical_box)

        self.vertical_layout_2 = QVBoxLayout(self.hand_vertical_box)
        self.vertical_layout_3 = QVBoxLayout(self.image_type_vertical_box)

        self.setup_view()

    def setup_view(self):
        self.vertical_group_box.setGeometry(QtCore.QRect(1200, 160, 250, 500))
        self.vertical_group_box.setStyleSheet(GROUP_BOX_STYLE_SHEET)

        self.vertical_layout.addWidget(self.filtered_checkbox, 0)
        self.vertical_layout.addWidget(self.background_difference_checkbox, 1)
        self.vertical_layout.addWidget(self.extracted_hand_checkbox, 2)
        self.vertical_layout.addWidget(self.opened_hand_checkbox, 3)
        self.vertical_layout.addWidget(self.contoured_checkbox, 4)
        self.vertical_layout.addWidget(self.final_checkbox, 5)

        self.form_group_box.setGeometry(QtCore.QRect(480, 300, 601, 141))
        self.form_group_box.setStyleSheet(GROUP_BOX_STYLE_SHEET)

        self.form_layout.setContentsMargins(-1, 5, -1, -1)
        self.form_layout.setHorizontalSpacing(12)
        self.form_layout.setVerticalSpacing(50)
        self.form_layout.setWidget(0, QFormLayout.LabelRole, self.android_server_url_label)
        self.form_layout.setWidget(0, QFormLayout.FieldRole, self.android_server_url_line_edit)

        self.android_server_url_line_edit.setStyleSheet(LINE_EDIT_STYLE_SHEET)

        self.hand_vertical_box.setGeometry(QtCore.QRect(150, 140, 150, 150))
        self.hand_vertical_box.setStyleSheet(GROUP_BOX_STYLE_SHEET)

        self.hand_label.setGeometry(QtCore.QRect(160, 80, 190, 80))
        self.hand_label.setStyleSheet(LABEL_STYLE_SHEET)

        self.vertical_layout_2.addWidget(self.right_hand_radio_button)
        self.vertical_layout_2.addWidget(self.left_hand_radio_button)

        self.image_type_vertical_box.setGeometry(QtCore.QRect(150, 520, 180, 150))
        self.image_type_vertical_box.setStyleSheet(GROUP_BOX_STYLE_SHEET)

        self.image_type_label.setGeometry(QtCore.QRect(160, 460, 190, 80))
        self.image_type_label.setStyleSheet(LABEL_STYLE_SHEET)

        self.vertical_layout_3.addWidget(self.rgb_image_radio_button)
        self.vertical_layout_3.addWidget(self.binary_image_radio_button)

        self.intermediary_steps_label.setGeometry(QtCore.QRect(1200, 75, 241, 111))
        self.intermediary_steps_label.setStyleSheet(LABEL_STYLE_SHEET)

    def set_view_options(self, data):
        if data['hand'] == HAND[1]:
            self.left_hand_radio_button.setChecked(True)
        else:
            self.right_hand_radio_button.setChecked(True)

        if data['image_type'] == IMAGE_TYPE[1]:
            self.binary_image_radio_button.setChecked(True)
        else:
            self.rgb_image_radio_button.setChecked(True)

        self.android_server_url_line_edit.setText(data['android_server_url'])

        for checkbox in self.vertical_group_box.children()[1:]:
            if data['intermediary_steps'][checkbox.text()]:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)
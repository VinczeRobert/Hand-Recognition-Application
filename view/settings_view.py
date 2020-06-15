from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from view.style_sheets.main_view_stylesheet import NO_BORDER_STYLE_SHEET, SOLID_BORDER_STYLE_SHEET, \
    MAIN_WINDOW_STYLE_SHEET, SETTINGS_TEXT_STYLE_SHEET


# noinspection PyArgumentList
class SettingsView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(SettingsView, self).__init__(parent)

        self.vertical_group_box = QtWidgets.QGroupBox(self)
        self.vertical_layout = QtWidgets.QVBoxLayout(self.vertical_group_box)

        self.filtered_image_checkbox = QtWidgets.QCheckBox()
        self.grayscale_image_checkbox = QtWidgets.QCheckBox()
        self.binary_image_checkbox = QtWidgets.QCheckBox()
        self.extracted_hand_checkbox = QtWidgets.QCheckBox()
        self.opened_hand_checkbox = QtWidgets.QCheckBox()
        self.contoured_checkbox = QtWidgets.QCheckBox()
        self.final_image_checkbox = QtWidgets.QCheckBox()

        self.form_group_box = QtWidgets.QGroupBox(self)
        self.form_layout = QtWidgets.QFormLayout(self.form_group_box)

        self.intermediary_steps_label = QtWidgets.QLabel(self)
        self.android_server_url_label = QtWidgets.QLabel(self.form_group_box)
        self.h5_path_label = QtWidgets.QLabel(self.form_group_box)
        self.hand_label = QtWidgets.QLabel(self)
        self.image_type_label = QtWidgets.QLabel(self)

        self.android_server_url_line_edit = QtWidgets.QLineEdit(self.form_group_box)
        self.h5_path_line_edit = QtWidgets.QLineEdit(self.form_group_box)

        self.vocal_mode_checkbox = QtWidgets.QCheckBox(self)

        self.hand_vertical_box = QtWidgets.QGroupBox(self)
        self.image_type_vertical_box = QtWidgets.QGroupBox(self)

        self.vertical_layout_2 = QtWidgets.QVBoxLayout(self.hand_vertical_box)

        self.right_hand_radio_button = QtWidgets.QRadioButton(self.hand_vertical_box)
        self.left_hand_radio_button = QtWidgets.QRadioButton(self.hand_vertical_box)
        self.rgb_images_radio_button = QtWidgets.QRadioButton(self.image_type_vertical_box)
        self.binary_image_radio_button = QtWidgets.QRadioButton(self.image_type_vertical_box)

        self.vertical_layout_3 = QtWidgets.QVBoxLayout(self.image_type_vertical_box)

        self.setup_page()

    def setup_page(self):
        self.setStyleSheet(MAIN_WINDOW_STYLE_SHEET + '\n' + SETTINGS_TEXT_STYLE_SHEET)

        self.vertical_group_box.setGeometry(QtCore.QRect(1200, 160, 250, 500))
        self.vertical_group_box.setStyleSheet(NO_BORDER_STYLE_SHEET)
        self.vertical_group_box.setObjectName("vertical_group_box")

        self.vertical_layout.setObjectName("vertical_layout")

        self.filtered_image_checkbox.setObjectName("filtered_image_checkbox")
        self.vertical_layout.addWidget(self.filtered_image_checkbox, 0)
        self.grayscale_image_checkbox.setObjectName("grayscale_image_checkbox")
        self.vertical_layout.addWidget(self.grayscale_image_checkbox, 1)
        self.binary_image_checkbox.setObjectName("binary_image_checkbox")
        self.vertical_layout.addWidget(self.binary_image_checkbox, 2)
        self.extracted_hand_checkbox.setObjectName("extracted_hand_checkbox")
        self.vertical_layout.addWidget(self.extracted_hand_checkbox, 3)
        self.opened_hand_checkbox.setObjectName("opened_hand_checkbox")
        self.vertical_layout.addWidget(self.opened_hand_checkbox, 4)
        self.contoured_checkbox.setObjectName("contoured_checkbox")
        self.vertical_layout.addWidget(self.contoured_checkbox, 5)
        self.final_image_checkbox.setObjectName("final_image_checkbox")
        self.vertical_layout.addWidget(self.final_image_checkbox, 6)

        self.intermediary_steps_label.setGeometry(QtCore.QRect(1200, 75, 241, 111))
        self.intermediary_steps_label.setObjectName("intermediary_steps_label")

        self.form_group_box.setGeometry(QtCore.QRect(480, 300, 601, 141))
        self.form_group_box.setStyleSheet(NO_BORDER_STYLE_SHEET)
        self.form_group_box.setObjectName("form_group_box")

        self.form_layout.setContentsMargins(-1, 5, -1, -1)
        self.form_layout.setHorizontalSpacing(12)
        self.form_layout.setVerticalSpacing(50)
        self.form_layout.setObjectName("formLayout")

        self.android_server_url_label.setObjectName("android_server_url_label")
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.android_server_url_label)

        self.android_server_url_line_edit.setStyleSheet(SOLID_BORDER_STYLE_SHEET)
        self.android_server_url_line_edit.setObjectName("android_server_url_line_edit")
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.android_server_url_line_edit)

        self.h5_path_label.setObjectName("h5_path_label")
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.h5_path_label)

        self.h5_path_line_edit.setStyleSheet(SOLID_BORDER_STYLE_SHEET)
        self.h5_path_line_edit.setObjectName("h5_path_line_edit")
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.h5_path_line_edit)

        self.vocal_mode_checkbox.setGeometry(QtCore.QRect(480, 130, 241, 71))
        self.vocal_mode_checkbox.setObjectName("vocal_mode_checkbox")

        self.hand_vertical_box.setGeometry(QtCore.QRect(150, 140, 150, 150))
        self.hand_vertical_box.setStyleSheet(NO_BORDER_STYLE_SHEET)
        self.hand_vertical_box.setObjectName("hand_vertical_box")

        self.vertical_layout_2.setObjectName("vertical_layout_2")

        self.right_hand_radio_button.setObjectName("right_hand_radio_button")
        self.right_hand_radio_button.setChecked(True)
        self.vertical_layout_2.addWidget(self.right_hand_radio_button)
        self.left_hand_radio_button.setObjectName("left_hand_radio_button")
        self.vertical_layout_2.addWidget(self.left_hand_radio_button)

        self.hand_label.setGeometry(QtCore.QRect(160, 80, 190, 80))
        self.hand_label.setObjectName("hand_label")

        self.image_type_vertical_box.setGeometry(QtCore.QRect(150, 520, 180, 150))
        self.image_type_vertical_box.setStyleSheet(NO_BORDER_STYLE_SHEET)
        self.image_type_vertical_box.setObjectName("image_type_vertical_box")

        self.vertical_layout_3.setObjectName("vertical_layout_3")

        self.rgb_images_radio_button.setObjectName("rgb_images_radio_button")
        self.rgb_images_radio_button.setChecked(True)
        self.vertical_layout_3.addWidget(self.rgb_images_radio_button)
        self.binary_image_radio_button.setObjectName("binary_image_radio_button")
        self.vertical_layout_3.addWidget(self.binary_image_radio_button)

        self.image_type_label.setGeometry(QtCore.QRect(160, 460, 190, 80))
        self.image_type_label.setObjectName("image_type_label")

        self.retranslate_view()

    def retranslate_view(self):
        _translate = QtCore.QCoreApplication.translate
        self.filtered_image_checkbox.setText(_translate("self", "Filtered Image"))
        self.grayscale_image_checkbox.setText(_translate("self", "Grayscale Image"))
        self.binary_image_checkbox.setText(_translate("self", "Binary Image"))
        self.extracted_hand_checkbox.setText(_translate("self", "Extracted Hand Image"))
        self.opened_hand_checkbox.setText(_translate("self", "Opened Hand Image"))
        self.contoured_checkbox.setText(_translate("self", "Contoured Image"))
        self.final_image_checkbox.setText(_translate("self", "Final Image"))
        self.intermediary_steps_label.setText(_translate("self", "Show Intermediary Steps"))
        self.android_server_url_label.setText(_translate("self", "Android Server URL"))
        self.h5_path_label.setText(_translate("self", "H5 Path"))
        self.vocal_mode_checkbox.setText(_translate("self", "Activate Vocal Mode"))
        self.right_hand_radio_button.setText(_translate("self", "Right Hand"))
        self.left_hand_radio_button.setText(_translate("self", "Left Hand"))
        self.hand_label.setText(_translate("self", "Choose Hand"))
        self.rgb_images_radio_button.setText(_translate("self", "RGB Images"))
        self.binary_image_radio_button.setText(_translate("self", "Binary Images"))
        self.image_type_label.setText(_translate("self", "Choose Image Type"))

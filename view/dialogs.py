from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMessageBox


# Methods used for selecting opening folders, files, for saving files and for displaying error messages

def choose_folder(message):
    dialog = QFileDialog()
    folder_path = dialog.getExistingDirectory(None, message)
    return folder_path

def choose_file_to_load(message, filter):
    dialog = QFileDialog()
    file_path = dialog.getOpenFileName(None, message, filter=filter)
    return file_path[0]

def choose_file_to_save(message, filter):
    dialog = QFileDialog
    file_path = dialog.getSaveFileName(None, message, filter=filter)
    return file_path[0]

def show_error_message(message):
    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Critical)
    error_dialog.setText(message)
    error_dialog.setWindowTitle("Error")
    error_dialog.setWindowIcon(QIcon("data/icons/hand_icon"))
    error_dialog.exec_()

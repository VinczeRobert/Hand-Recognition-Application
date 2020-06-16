import sys
from PyQt5 import QtWidgets

from controllers.hand_gesture_prediction_controller import HandGestureRecognitionController
from controllers.main_controller import MainController
from controllers.settings_controller import SettingsController

# For printing exception messages
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    HandGestureRecognitionController()
    SettingsController()
    MainController()
    sys.excepthook = except_hook
    sys.exit(app.exec_())

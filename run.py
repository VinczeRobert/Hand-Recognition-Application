import sys
from PyQt5.QtWidgets import QApplication
from controller.add_new_sign_controller import AddNewSignController
from controller.hand_gesture_prediction_controller import HandGestureRecognitionController
from controller.main_controller import MainController
from controller.settings_controller import SettingsController
from controller.train_neural_network_controller import TrainNeuralNetworkController


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    HandGestureRecognitionController()
    AddNewSignController()
    TrainNeuralNetworkController()
    SettingsController()
    MainController()
    sys.excepthook = except_hook
    sys.exit(app.exec_())

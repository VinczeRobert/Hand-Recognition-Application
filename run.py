import sys
from PyQt5 import QtWidgets
from controllers.main_controller import MainController
from controllers.settings_controller import SettingsController

StyleSheet = '''
QPushButton:hover {
   background-color: #000000;
   color: #579641;
}
'''

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainController()
    SettingsController()
    sys.exit(app.exec_())

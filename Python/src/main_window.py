"""
This file implements the main window file
"""

from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from src.user_interface.gui import MainApp
from src.workers.serial_communication import ArduinoCommunication


class MainWindow(QMainWindow):
    """
    Main Window Class
    """

    APP_TITLE = "Ball and Plate"

    def __init__(self, screen_resolution, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle(self.APP_TITLE)
        self.setWindowIcon(QIcon("resources/images/icon.ico"))
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        self.main_app_widget = MainApp(screen_resolution)
        self.arduino_communication = ArduinoCommunication()

        self.main_app_widget.close_signal.connect(self.close)

        self.arduino_communication.make_connection(self.main_app_widget)
        self.arduino_communication.toggle_communication(self.main_app_widget)

        self.init_user_interface()

    def init_user_interface(self):
        """
        Method to init user interface
        """
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.addWidget(self.main_app_widget)
        self.central_widget.setCurrentWidget(self.main_app_widget)

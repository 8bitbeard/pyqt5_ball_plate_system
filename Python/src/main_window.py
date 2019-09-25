"""
This file implements the main window file
"""

from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QAction, QMenu
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt

from src.user_interface.gui import MainApp
from src.workers.serial_communication import ArduinoCommunication

from src.utils import utils


class MainWindow(QMainWindow):
    """
    Main Window Class
    """

    APP_TITLE = "Ball and Plate"

    def __init__(self, screen_resolution, main_application, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle(self.APP_TITLE)
        self.setWindowIcon(QIcon(utils.get_absolute_resource_path("resources/images/icon.png")))
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        self.main_application = main_application

        self.main_app_widget = MainApp(screen_resolution)
        self.arduino_communication = ArduinoCommunication()

        self.main_app_widget.close_signal.connect(self.close)

        self.arduino_communication.make_connection(self.main_app_widget)
        self.arduino_communication.toggle_communication(self.main_app_widget)

        self.init_menu_bar()
        self.init_user_interface()


    def toggle_dark_mode(self, value):
        """
        Method to start the app with a dark theme
        """
        dark_palette = QPalette()
        if value:
            dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.WindowText, Qt.white)
            dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
            dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
            dark_palette.setColor(QPalette.ToolTipText, Qt.white)
            dark_palette.setColor(QPalette.Text, Qt.white)
            dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ButtonText, Qt.white)
            dark_palette.setColor(QPalette.BrightText, Qt.red)
            dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.HighlightedText, Qt.black)
            dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
            dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)

            self.main_application.setPalette(dark_palette)
            self.main_application.setStyleSheet("QToolTip { color: #ffffff;\
                                                            background-color: #2a82da;\
                                                            border: 1px solid white; }")
        else:
            self.main_application.setPalette(self.main_application.style().standardPalette())
            self.main_application.setStyleSheet("")

    def change_resolution(self, resolution_value):
        """
        Method to change the resolution
        """
        if resolution_value:
            self.main_app_widget.set_widgets_size(1.25)
        else:
            self.main_app_widget.set_widgets_size(1)
        self.setFixedSize(self.main_app_widget.sizeHint())
        self.setFixedSize(self.main_app_widget.sizeHint())
        print(self.main_app_widget.sizeHint())

    def init_user_interface(self):
        """
        Method to init user interface
        """
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.addWidget(self.main_app_widget)
        self.central_widget.setCurrentWidget(self.main_app_widget)

    def init_menu_bar(self):
        """
        This method handles the creation of the menubar
        """
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        settings_menu = QMenu('Settings', self)

        settings_menu_two = QMenu('Theme', self)
        settings_theme_action_one = QAction('Default', self)
        settings_theme_action_one.triggered.connect(lambda: self.toggle_dark_mode(False))
        settings_theme_action_two = QAction('Dark mode', self)
        settings_theme_action_two.triggered.connect(lambda: self.toggle_dark_mode(True))

        settings_menu_three = QMenu('Resolution', self)
        settings_resolution_action_one = QAction('1280x720', self)
        settings_resolution_action_one.triggered.connect(lambda: self.change_resolution(0))
        settings_resolution_action_two = QAction('1920x1080', self)
        settings_resolution_action_two.triggered.connect(lambda: self.change_resolution(1))

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)

        file_menu.addMenu(settings_menu)
        file_menu.addAction(exit_action)
        settings_menu.addMenu(settings_menu_two)
        settings_menu_two.addAction(settings_theme_action_one)
        settings_menu_two.addAction(settings_theme_action_two)
        settings_menu.addMenu(settings_menu_three)
        settings_menu_three.addAction(settings_resolution_action_one)
        settings_menu_three.addAction(settings_resolution_action_two)

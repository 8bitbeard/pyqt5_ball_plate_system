# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
This is the main file of the Ball and Plate app
"""

import sys

from PyQt5 import QtWidgets
from src.workers.serial_communication import ArduinoCommunication
from src.user_interface.gui import MainApp


def main():
    """
    Main function to start the app
    """
    app = QtWidgets.QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    arduino = ArduinoCommunication()
    win = MainApp(screen_resolution)
    arduino.make_connection(win)
    arduino.toggle_communication(win)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

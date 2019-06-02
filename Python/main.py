"""
This is the main file of the Ball and Plate app
"""
# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from arduino_communication.serial_communication import ArduinoCommunication
from user_interface.gui import MainApp


def main():
    """
    Main function to start the app
    """
    app = QtWidgets.QApplication(sys.argv)
    arduino = ArduinoCommunication()
    win = MainApp()
    arduino.make_connection(win)
    arduino.toggle_communication(win)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

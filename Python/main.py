#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from arduino_communication.serial_communication import ArduinoCommunication
from user_interface.gui import MainApp
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    arduino = ArduinoCommunication()
    win = MainApp()
    arduino.make_connection(win)
    arduino.toggle_communication(win)
    win.show()
    sys.exit(app.exec_())

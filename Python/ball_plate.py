# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
This is the main file of the Ball and Plate app
"""

import sys

from PyQt5.QtWidgets import QApplication
from src.main_window import MainWindow


def main():
    """
    Main function to start the app
    """
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    screen_resolution = app.desktop().screenGeometry()
    window = MainWindow(screen_resolution, app)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

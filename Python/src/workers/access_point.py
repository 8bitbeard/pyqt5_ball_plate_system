"""
This file defines the AccessPoint class.

This class implements the access point feature ofa the app.
With this, the user can create a local wireless network to
connect the robot camera.

This feature only works on linux machines, as the
app used to create the access points is the create_ap

https://github.com/oblique/create_ap
"""

import subprocess
from pathlib import Path

from PyQt5.QtCore import QThread


class AccessPoint(QThread):
    """
    Class to manage the thread to run the access point scripts
    """

    SCRIPTS_FOLDER = Path("src/resources/")
    START_SCRIPT = SCRIPTS_FOLDER / "start_ap.zsh"
    STOP_SCRIPT = SCRIPTS_FOLDER / "stop_ap.zsh"

    def __init__(self):
        QThread.__init__(self)
        self.thread_status = False

    def __del__(self):
        if self.thread_status:
            self.run_script(self.STOP_SCRIPT)
            self.thread_status = False
        self.wait()

    @staticmethod
    def run_script(script):
        """
        Method to run the script passed as a argument. (Start or Stop)
        """
        subprocess.Popen(script, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def start(self):
        """
        Method to pass the start ap script to the run_script static method
        """
        self.run_script(self.START_SCRIPT)
        self.thread_status = True

    def stop(self):
        """
        Method to pass the stop ap script to the run_script static method
        """
        self.run_script(self.STOP_SCRIPT)
        self.thread_status = False

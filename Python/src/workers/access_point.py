"""
Access point class
"""

import subprocess
import os.path

from PyQt5.QtCore import QThread


class AccessPoint(QThread):
    """
    Class to manage the thread to run the access point scripts
    """

    START_SCRIPT = os.path.join("Python/src/resources", "start_ap.zsh")
    STOP_SCRIPT = os.path.join("Python/src/resources", "stop_ap.zsh")

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.run_script(self.STOP_SCRIPT)
        self.wait()

    @staticmethod
    def run_script(script):
        """
        Temp
        """
        subprocess.Popen(script, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def start(self):
        """
        Temp
        """
        self.run_script(self.START_SCRIPT)

    def stop(self):
        """
        Temp
        """
        self.run_script(self.STOP_SCRIPT)

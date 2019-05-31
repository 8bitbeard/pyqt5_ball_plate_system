from PyQt5 import QtCore
import subprocess
import os.path


class AccessPoint(QtCore.QThread):
    """
    Class to manage the thread to run the access point scripts
    """

    START_SCRIPT = os.path.join("resources", "start_ap.zsh")
    STOP_SCRIPT = os.path.join("resources", "stop_ap.zsh")

    def __init__(self):
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.run_script(self.STOP_SCRIPT)
        self.wait()

    def run_script(self, script):
        subprocess.Popen(script, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def start(self):
        self.run_script(self.START_SCRIPT)

    def stop(self):
        self.run_script(self.STOP_SCRIPT)

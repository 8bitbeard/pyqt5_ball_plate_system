#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from random import randint
import serial.tools.list_ports
import serial
import time


class ArduinoCommunication(QtCore.QThread):
    """
    Class to manage the thread to do the arduino communication
    """

    arduino_data = QtCore.pyqtSignal(tuple)

    def __init__(self, isRunning=False, isConnected=False, sample_time=0.033):
        QtCore.QThread.__init__(self)
        self.isRunning = isRunning
        self.isConnected = isConnected
        self.sample_time = sample_time
        self.constant_changed = False

        self.center_centimeters = (0, 0)
        self.setpoint_centimeters = (0, 0)

        self.angle_x = 0
        self.angle_y = 0
        self.joystick_x = 0
        self.joystick_y = 0

    def __del__(self):
        self.wait()

    @QtCore.pyqtSlot(tuple, tuple)
    def getDataFromApplication(self, center_centimeters, setpoint_centimeters):
        """
        This function handles the data received from the application (Values acquired from the video processing)
        """
        self.center_centimeters = center_centimeters
        self.setpoint_centimeters = setpoint_centimeters

    @QtCore.pyqtSlot(bool)
    def toggleRunning(self, value):
        """
        This function hanles the isRunning flag value
        """
        self.isRunning = value

    def make_connection(self, application_object):
        application_object.centers_signal.connect(self.getDataFromApplication)

    def toggle_communication(self, application_object):
        application_object.start_signal.connect(self.toggleRunning)

    def is_connected(self):
        return self.isConnected

    def getDataFromArduino(self):
        """
        This function handles all the data received from the arduino board
        """
        arduino_string = self.data.readline().decode("utf-8")
        data_array = arduino_string.split(",")
        angle_x = float(data_array[0])
        angle_y = float(data_array[1])
        joystick_x = float(data_array[2])
        joystick_y = float(data_array[3])
        # print("Received: {}".format(data_array))
        return (angle_x, angle_y, joystick_x, joystick_y)

    def sendDataToArduino(self, tupleA, tupleB, tupleC, tupleD):
        """
        This function send all processed data to the arduino board
        """
        valA = "%+.2f" % (tupleA[0])
        valB = "%+.2f" % (tupleA[1])
        valC = "%+.2f" % (tupleB[0])
        valD = "%+.2f" % (tupleB[1])
        valE = "%+.3f" % (tupleC[0])
        valF = "%+.3f" % (tupleC[1])
        valG = "%+.3f" % (tupleC[2])
        valH = "%+.3f" % (tupleD[0])
        valI = "%+.3f" % (tupleD[1])
        valJ = "%+.3f" % (tupleD[2])
        if self.constant_changed:
            result = valA + '!' + valB + '#' + valC + '$' + valD + '%' + valE + '&' \
                     + valF + '[' + valG + ']' + valH + '{' + valI + '}' + valJ + '*'
        else:
            result = valA + '!' + valB + '#' + valC + '$' + valD + '%' + valE + '&' \
                     + valF + '[' + valG + ']' + valH + '{' + valI + '}' + valJ + '@'
        self.constant_changed = False
        # print("Sent:{}".format(result))
        self.data.write(result.encode())

    def dummydata(self):
        """
        This function simulates the data received from the Arduino Board
        """
        angle_x = randint(-20, 20)
        angle_y = randint(-20, 20)
        joystick_x = randint(-100, 100)
        joystick_y = randint(-100, 100)
        return (angle_x, angle_y, joystick_x, joystick_y)

    def stop(self):
        self.isConnected = False
        self.isRunning = False
        self.data.close()

    def run(self):
        self.arduino_ports = [p.device for p in serial.tools.list_ports.comports() if 'Arduino' in p.description]
        if not self.arduino_ports:
            raise IOError("No Arduino board found, check if the board is really connected")

        self.data = serial.Serial(self.arduino_ports[0], 115200)

        self.isRunning = False
        self.isConnected = True

        self.arduino_communication()

    def arduino_communication(self):
        while self.isConnected:

            initial_time = time.time()
            if self.isRunning:
                self.sendDataToArduino(self.center_centimeters, self.setpoint_centimeters, (0, 0, 0), (0, 0, 0))
                while self.data.in_waiting:
                    self.angle_x, self.angle_y, self.joystick_x, self.joystick_y = self.getDataFromArduino()
            final_time = time.time()
            total_time = final_time - initial_time

            time.sleep(abs(self.sample_time - total_time))

            self.arduino_communication_time = time.time() - initial_time
            self.arduino_data.emit((self.angle_x, self.angle_y,
                                    self.joystick_x, self.joystick_y,
                                    self.arduino_communication_time))

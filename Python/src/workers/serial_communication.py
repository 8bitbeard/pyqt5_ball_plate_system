#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This file implements te ArduinoCommunication thread, responsible
for all the dat transfer between the application and the arduino
board
"""

import time
from random import randint

import serial
import serial.tools.list_ports

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot


class ArduinoCommunication(QThread):
    """
    Class to manage the thread to do the arduino communication
    """

    arduino_data = pyqtSignal(tuple)

    def __init__(self, is_thread_running=False, is_board_connected=False, sample_time=0.033):
        QThread.__init__(self)
        self.is_thread_running = is_thread_running
        self.is_board_connected = is_board_connected
        self.sample_time = sample_time
        self.constant_changed = False

        self.center_centimeters = (0, 0)
        self.setpoint_centimeters = (0, 0)

        self.angle_x = 0
        self.angle_y = 0
        self.joystick_x = 0
        self.joystick_y = 0

        self.arduino_ports = None
        self.data = None
        self.arduino_communication_time = None

    def __del__(self):
        self.wait()

    @pyqtSlot(tuple, tuple)
    def get_data_from_application(self, center_centimeters, setpoint_centimeters):
        """
        This function handles the data received from the application (Values acquired from the video processing)
        """
        self.center_centimeters = center_centimeters
        self.setpoint_centimeters = setpoint_centimeters

    @pyqtSlot(bool)
    def toggle_running_thread(self, value):
        """
        This function hanles the is_thread_running flag value
        """
        self.is_thread_running = value

    def make_connection(self, application_object):
        """
        Temporary
        """
        application_object.centers_signal.connect(self.get_data_from_application)

    def toggle_communication(self, application_object):
        """
        Temporary
        """
        application_object.start_signal.connect(self.toggle_running_thread)

    def is_connected(self):
        """
        Temporary
        """
        return self.is_board_connected

    def get_data_from_arduino(self):
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

    def send_data_to_arduino(self, tuple_a, tuple_b, tuple_c, tuple_d):
        """
        This function send all processed data to the arduino board
        """
        value_a = "%+.2f" % (tuple_a[0])
        value_b = "%+.2f" % (tuple_a[1])
        value_c = "%+.2f" % (tuple_b[0])
        value_d = "%+.2f" % (tuple_b[1])
        value_e = "%+.3f" % (tuple_c[0])
        value_f = "%+.3f" % (tuple_c[1])
        value_g = "%+.3f" % (tuple_c[2])
        value_h = "%+.3f" % (tuple_d[0])
        value_i = "%+.3f" % (tuple_d[1])
        value_j = "%+.3f" % (tuple_d[2])
        if self.constant_changed:
            result = value_a + '!' + value_b + '#' + value_c + '$' + value_d + '%' + value_e + '&' \
                     + value_f + '[' + value_g + ']' + value_h + '{' + value_i + '}' + value_j + '*'
        else:
            result = value_a + '!' + value_b + '#' + value_c + '$' + value_d + '%' + value_e + '&' \
                     + value_f + '[' + value_g + ']' + value_h + '{' + value_i + '}' + value_j + '@'
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
        """
        Method to stop the arduino communicaton thread
        """
        self.is_board_connected = False
        self.is_thread_running = False
        self.data.close()

    def run(self):
        """
        Method to start the arduino communication thread
        """
        self.arduino_ports = [p.device for p in serial.tools.list_ports.comports() if 'Arduino' in p.description]
        if not self.arduino_ports:
            raise IOError("No Arduino board found, check if the board is really connected")

        self.data = serial.Serial(self.arduino_ports[0], 115200)

        self.is_thread_running = False
        self.is_board_connected = True

        self.arduino_communication()

    def arduino_communication(self):
        """
        Method with the main data communicaton loop
        """
        while self.is_board_connected:

            initial_time = time.time()
            if self.is_thread_running:
                self.send_data_to_arduino(self.center_centimeters, self.setpoint_centimeters, (0, 0, 0), (0, 0, 0))
                while self.data.in_waiting:
                    self.angle_x, self.angle_y, self.joystick_x, self.joystick_y = self.get_data_from_arduino()
            final_time = time.time()
            total_time = final_time - initial_time

            time.sleep(abs(self.sample_time - total_time))

            self.arduino_communication_time = time.time() - initial_time
            self.arduino_data.emit((self.angle_x, self.angle_y,
                                    self.joystick_x, self.joystick_y,
                                    self.arduino_communication_time))

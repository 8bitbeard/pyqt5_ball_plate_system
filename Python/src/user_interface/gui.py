"""
This is the app main file
"""
# !/usr/bin/python
# -*- coding: utf-8 -*-

import math
import time
import os
from collections import deque
from functools import partial
import numpy as np

import pyqtgraph as pg
import imutils
from imutils.video import WebcamVideoStream

from PyQt5.QtCore import QSize, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QMessageBox

import cv2
from src.user_interface.widgets import AppWidgets
from src.workers.access_point import AccessPoint
from src.workers.serial_communication import ArduinoCommunication


class MainApp(QWidget, AppWidgets):
    """
    Initialize all constant variables
    """
    # Defining Wiget sizes
    TEXT_SIZE = QSize(35, 15)
    SMALL_TEXT_SIZE = QSize(26, 15)
    LARGE_TEXT_SIZE = QSize(85, 15)
    IMAGE_SIZE = QSize(450, 450)
    VIDEO_SIZE = QSize(450, 450)
    GRAPH_SIZE = QSize(450, 210)
    BUTTON_SIZE = QSize(120, 22)
    SLIDER_SIZE = QSize(170, 15)
    TEXT_BOX_SIZE = QSize(270, 25)
    COMBO_BOX_SIZE = QSize(105, 25)

    # Physical model parameters
    BALL_DIAMETER = 0.0022
    BALL_WEIGHT = 0.031
    PLATE_FRICTION = 0.0010
    GRAVITY = -9.81

    # Defining the sample time
    TIME = 0.033

    centers_signal = pyqtSignal(tuple, tuple)
    start_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        """
        This is the main app class
        """
        super(MainApp, self).__init__(parent)

        self.tick_high = 0
        self.step = 0.5
        self.joystick_points = deque(maxlen=3)
        self.circle_radius = 50
        self.center_pixels = (0, 0)
        self.move_pattern = "Center"
        # Lower and Upper Threshold values
        self.threshold_ball = [0, 0, 145, 0, 0, 255]
        self.threshold_plate = [0, 178, 0, 255, 255, 218]
        # Defining setpoints
        self.setpoint_mouse = (0, 0)
        self.setpoint_joystick = (0, 0)
        self.setpoint_square = [(-90, -90), (90, -90), (90, 90), (-90, 90)]
        # Arduino input variables
        self.joystick_x = 0
        self.joystick_y = 0
        self.angle_x = 0
        self.angle_y = 0

        self.ip_value = '192.168.12.86'

        self.center_centimeters = (0, 0)
        self.setpoint_centimeters = (0, 0)

        self.without_ball = 0
        self.radius = 0

        self.constant_changed = False

        self.start_time = None
        self.video_source = None
        self.previous_time = None
        self.current_output = None
        self.video_processing_time = None
        self.arduino_communication_time = None
        self.loop_time = None
        self.update_widgets_time = None
        self.data_buffer_one = None
        self.data_buffer_two = None
        self.data_buffer_three = None
        self.data_buffer_four = None
        self.data_buffer_five = None
        self.data_buffer_six = None
        self.x_axis = None
        self.setpoint_pixels = None
        self.image = None
        self.mask_3ch_rgb = None
        self.pts_list = None
        self.black = None
        self.warped = None
        self.prediction = None
        self.d_x = None
        self.d_y = None
        self.error_pixels = None
        self.error_centimeters = None
        self.coordinate_values = None

        self.access_point_server = AccessPoint()
        self.start_arduino_connection = ArduinoCommunication()
        self.start_arduino_connection.make_connection(self)
        self.start_arduino_connection.toggle_communication(self)

        self.setup_kalman_filter()
        self.setup_ui()
        self.setup_graphs()

    def setup_ui(self):
        """
        This function sets up all the Labels used in the widget, and start all threads
        """
        # Connecting the inherited combo box to its functions
        self.combo_box_one.currentTextChanged.connect(self.video_input_change)
        self.combo_box_two.currentTextChanged.connect(self.mode_change)
        self.combo_box_three.currentTextChanged.connect(self.step_change)
        self.combo_box_four.currentTextChanged.connect(self.radius_change)

        # Connecting the inherited ip QLineEdit to its function
        self.camera_ip_textbox.setText(self.ip_value)

        # Connecting the inherited buttons to its functions
        self.start_button.clicked.connect(self.start_app)
        self.serial_connect_button.clicked.connect(self.connect_serial)
        self.quit_button.clicked.connect(self.close)
        self.thresh_button.clicked.connect(self.change_threshold_value)
        self.select_ip_button.clicked.connect(self.set_video_ip)
        self.access_point_button.clicked.connect(self.toggle_access_point)
        if os.name != 'posix':
            self.access_point_button.setEnabled(False)

        # Connecting the inherite Sliders to its functions
        self.slider_r_low.valueChanged.connect(partial(self.slider_value_change, number=0,
                                                       text_value_label=self.text_r_low_value_label,
                                                       slider=self.slider_r_low))
        self.slider_g_low.valueChanged.connect(partial(self.slider_value_change, number=1,
                                                       text_value_label=self.text_g_low_value_label,
                                                       slider=self.slider_g_low))
        self.slider_b_low.valueChanged.connect(partial(self.slider_value_change, number=2,
                                                       text_value_label=self.text_b_low_value_label,
                                                       slider=self.slider_b_low))
        self.slider_r_high.valueChanged.connect(partial(self.slider_value_change, number=3,
                                                        text_value_label=self.text_r_high_value_label,
                                                        slider=self.slider_r_high))
        self.slider_g_high.valueChanged.connect(partial(self.slider_value_change, number=4,
                                                        text_value_label=self.text_g_high_value_label,
                                                        slider=self.slider_g_high))
        self.slider_b_high.valueChanged.connect(partial(self.slider_value_change, number=5,
                                                        text_value_label=self.text_b_high_value_label,
                                                        slider=self.slider_b_high))

        # Inherited from the AppWidgets class
        self.setLayout(self.main_layout)

    def update_gui(self, frame, black, image):
        """
        This function update the widget custom GUI
        """
        # Setting up the FONT
        font = cv2.FONT_HERSHEY_SIMPLEX
        # Drawing the bounding squares in the frame
        cv2.rectangle(frame, (25, 25), (425, 425), (0, 255, 0), 2)

        # Square that limits the lateral GUI
        cv2.rectangle(frame, (500, 10), (630, 470), (0, 255, 0), 1)
        cv2.rectangle(black, (10, 10), (160, 440), (0, 255, 0), 1)
        cv2.rectangle(black, (170, 10), (440, 440), (0, 255, 0), 1)

        cv2.line(image, (self.pts_list[0][0], 0), (self.pts_list[0][0], 480), (0, 255, 0), 1, 8, 0)
        cv2.line(image, (0, self.pts_list[0][1]), (480, self.pts_list[0][1]), (0, 255, 0), 1, 8, 0)
        cv2.line(image, (self.pts_list[1][0], 0), (self.pts_list[1][0], 480), (0, 255, 0), 1, 8, 0)
        cv2.line(image, (0, self.pts_list[1][1]), (480, self.pts_list[1][1]), (0, 255, 0), 1, 8, 0)
        cv2.line(image, (self.pts_list[2][0], 0), (self.pts_list[2][0], 480), (0, 255, 0), 1, 8, 0)
        cv2.line(image, (0, self.pts_list[2][1]), (480, self.pts_list[2][1]), (0, 255, 0), 1, 8, 0)
        cv2.line(image, (self.pts_list[3][0], 0), (self.pts_list[3][0], 480), (0, 255, 0), 1, 8, 0)
        cv2.line(image, (0, self.pts_list[3][1]), (480, self.pts_list[3][1]), (0, 255, 0), 1, 8, 0)

        cv2.circle(image, (self.pts_list[0][0], self.pts_list[0][1]), 5, (0, 0, 255), -1)
        cv2.circle(image, (self.pts_list[1][0], self.pts_list[1][1]), 5, (0, 0, 255), -1)
        cv2.circle(image, (self.pts_list[2][0], self.pts_list[2][1]), 5, (0, 0, 255), -1)
        cv2.circle(image, (self.pts_list[3][0], self.pts_list[3][1]), 5, (0, 0, 255), -1)

        # Circulos limite do CP e SP
        cv2.circle(frame, (int(self.prediction[0][0] + self.IMAGE_SIZE.width()/2),
                           int(self.IMAGE_SIZE.height()/2 - self.prediction[1][0])), int(self.radius), (0, 255, 0), 2)

        cv2.circle(frame, (int(self.prediction[0][0] + self.IMAGE_SIZE.width()/2),
                           int(self.IMAGE_SIZE.height()/2 - self.prediction[1][0])), 5, (0, 0, 255), -1)

        cv2.putText(frame, "CP", (self.prediction[0][0].astype(int) + int(self.IMAGE_SIZE.width()/2 + 10),
                                  int(self.IMAGE_SIZE.height()/2 + 20) - self.prediction[1][0].astype(int)),
                    font, 0.5, (0, 0, 255), 1)
        cv2.circle(frame, (self.setpoint_pixels[0] + int(self.IMAGE_SIZE.width()/2), int(self.IMAGE_SIZE.height()/2)
                           - self.setpoint_pixels[1]), 5, (255, 0, 0), -1)
        cv2.putText(frame, "SP", (self.setpoint_pixels[0] + int(self.IMAGE_SIZE.width()/2 - 20),
                                  int(self.IMAGE_SIZE.height()/2 - 10) - self.setpoint_pixels[1]),
                    font, 0.5, (255, 0, 0), 1)

        cv2.line(frame, (25, int(self.IMAGE_SIZE.height()/2 - self.prediction[1][0])),
                 (425, int(self.IMAGE_SIZE.height()/2 - self.prediction[1][0])), (0, 0, 255), 1, 8, 0)
        cv2.line(frame, (int(self.prediction[0][0] + self.IMAGE_SIZE.width()/2), 25),
                 (int(self.prediction[0][0] + self.IMAGE_SIZE.width()/2), 425), (0, 0, 255), 1, 8, 0)

        text_pos_x = [10, 55, 95, 135, 175, 222, 262, 302, 344, 380, 418]
        text_pos_y = [8, 13, 13, 13, 13, 13, 6, 6, 6, 6, 2]
        for i in range(0, 11):
            cv2.line(frame, (25 + i * 40, 425), (25 + i * 40, 415), (0, 255, 0), 1, 8, 0)
            cv2.line(frame, (25, 25 + i*40), (35, 25 + i * 40), (0, 255, 0), 1, 8, 0)
            cv2.putText(frame, str(int(-10 + 2 * i)), (text_pos_x[i], 440), font, 0.3, (0, 255, 0), 1)
            cv2.putText(frame, str(int(10 - 2 * i)), (text_pos_y[i], 27 + i*40), font, 0.3, (0, 255, 0), 1)

        # Gui #1
        cv2.putText(black, "Ball Speed", (15, 30), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "dX: %+.2f m/s" % (self.d_x), (15, 50), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "dY: %+.2f m/s" % (self.d_y), (15, 65), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "Set Point", (15, 85), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "X: %+.2f Cm" % (self.setpoint_centimeters[0]), (15, 105), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "Y: %+.2f Cm" % (self.setpoint_centimeters[1]), (15, 120), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "Current Point", (15, 140), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "X: %+.2f Cm" % (self.center_centimeters[0]), (15, 160), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "Y: %+.2f Cm" % (self.center_centimeters[1]), (15, 175), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "Error", (15, 195), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "X: %+.2f Cm" % (self.error_centimeters[0]), (15, 215), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "Y: %+.2f Cm" % (self.error_centimeters[1]), (15, 230), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "Mode", (15, 250), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "{}".format(self.move_pattern), (15, 270), font, 0.5, (255, 255, 0), 1)

        # Criando os gauges do gui lateral
        angle_x_text_size = int(cv2.getTextSize(str(int(self.angle_x)), font, 0.6, 1)[0][0] / 2)
        angle_y_text_size = int(cv2.getTextSize(str(int(self.angle_y)), font, 0.6, 1)[0][0] / 2)
        cv2.putText(black, "X-axis angle", (15, 292), font, 0.5, (0, 255, 0), 1)
        cv2.ellipse(black, (85, 350), (49, 49), 0, 180, 360, (255, 255, 255), -1)
        cv2.ellipse(black, (85, 350), (50, 50), 0, int(270 + int(3 * self.angle_x)), 180, (255, 0, 0), -1)
        cv2.ellipse(black, (85, 350), (30, 30), 0, 180, 360, (0, 0, 0), -1)
        cv2.putText(black, "{}".format(int(self.angle_x)), (85 - angle_x_text_size, 350), font, 0.6, (0, 255, 0), 1)
        cv2.putText(black, "Y-axis angle", (15, 370), font, 0.5, (0, 255, 0), 1)
        cv2.ellipse(black, (85, 430), (49, 49), 0, 180, 360, (255, 255, 255), -1)
        cv2.ellipse(black, (85, 430), (50, 50), 0, int(270 + int(3 * self.angle_y)), 180, (0, 0, 255), -1)
        cv2.ellipse(black, (85, 430), (30, 30), 0, 180, 360, (0, 0, 0), -1)
        cv2.putText(black, "{}".format(int(self.angle_y)), (85 - angle_y_text_size, 430), font, 0.6, (0, 255, 0), 1)

        # Gui #2
        cv2.putText(black, "System settings", (225, 35), font, 0.6, (0, 255, 0), 1)
        cv2.putText(black, "Mechanical constants", (180, 60), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "Ball diameter: {} m".format(self.BALL_DIAMETER), (180, 85), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "Ball weight: {} Kg".format(self.BALL_WEIGHT), (180, 105), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "Plate friction: {} N/m".format(self.PLATE_FRICTION), (180, 125), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "Gravity: {} m/s^2".format(self.GRAVITY), (180, 145), font, 0.5, (0, 255, 0), 1)

        # Marcador de Tempo para debugging
        # cv2.putText(black, "Sample Time: {0:.3f} s".format(self.loop_time), (180, 290), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "WiFi Server Status:", (180, 260), font, 0.5, (0, 255, 0), 1)
        if self.access_point_button.text() == 'Stop server':
            cv2.putText(black, "Online", (335, 260), font, 0.5, (0, 255, 0), 1)
        else:
            cv2.putText(black, "Offline", (335, 260), font, 0.5, (255, 0, 0), 1)
        cv2.putText(black, "Serial Status:", (180, 290), font, 0.5, (0, 255, 0), 1)
        if self.serial_connect_button.text() == 'Serial disconnect':
            cv2.putText(black, "Connected", (290, 290), font, 0.5, (0, 255, 0), 1)
        else:
            cv2.putText(black, "Disconnected", (290, 290), font, 0.5, (255, 0, 0), 1)
        cv2.putText(black, "Sample Time: {} ms".format(int(1000 * self.arduino_communication_time)), (180, 330),
                    font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "Total Time: {0:.2f} s".format(time.time() - self.start_time), (180, 360),
                    font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "UFPE", (180, 390), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "DES - CTG", (180, 410), font, 0.5, (0, 255, 0), 1)
        cv2.putText(black, "Wilton O. de Souza Filho", (180, 430), font, 0.5, (0, 255, 0), 1)

    def setup_graphs(self):
        """
        This function sets up all configuration for the live graphs displayed on the widget
        """
        sample_interval = 1
        sample_window = 100

        # Creating all the 3 graphs and setting their titles
        my_plot_one = self.graph_one.addPlot(title='Total Error')
        my_plot_two = self.graph_two.addPlot(title='X - Set Point / Current Point')
        my_plot_three = self.graph_three.addPlot(title='Y - Set Point / Current Point')

        # self._interval = int(sample_interval*1000)
        bufsize = int(sample_window/sample_interval)
        self.data_buffer_one = deque([0.0]*bufsize, bufsize)
        self.data_buffer_two = deque([0.0]*bufsize, bufsize)
        self.data_buffer_three = deque([0.0]*bufsize, bufsize)
        self.data_buffer_four = deque([0.0]*bufsize, bufsize)
        self.data_buffer_five = deque([0.0]*bufsize, bufsize)
        self.data_buffer_six = deque([0.0]*bufsize, bufsize)
        # Criando variável que armazena a quatidade de amostras a serem mostradas (Range do eixo X)
        self.x_axis = np.linspace(-sample_window, 0.0, bufsize)
        # Criando variáveis que armazenarão os dados a serem plotados para cada variável

        my_plot_one.showGrid(x=True, y=True)
        my_plot_one.setLabel('left', 'Position', 'Cm')
        my_plot_one.setLabel('bottom', 'Samples', 'n')
        my_plot_one.setYRange(-22, 22)

        my_plot_two.showGrid(x=True, y=True)
        my_plot_two.setLabel('left', 'Position', 'Cm')
        my_plot_two.setLabel('bottom', 'Samples', 'n')
        my_plot_two.setYRange(-12, 12)

        my_plot_three.showGrid(x=True, y=True)
        my_plot_three.setLabel('left', 'Position', 'Cm')
        my_plot_three.setLabel('bottom', 'Samples', 'n')
        my_plot_three.setYRange(-12, 12)

        self.curve_one = my_plot_one.plot(self.x_axis, self.data_buffer_one, pen=pg.mkPen((255, 0, 0), width=2))
        self.curve_two = my_plot_one.plot(self.x_axis, self.data_buffer_two, pen=pg.mkPen((0, 0, 255), width=2))
        self.curve_three = my_plot_two.plot(self.x_axis, self.data_buffer_three, pen=pg.mkPen((255, 0, 0), width=2))
        self.curve_four = my_plot_two.plot(self.x_axis, self.data_buffer_four, pen=pg.mkPen((0, 0, 255), width=2))
        self.curve_five = my_plot_three.plot(self.x_axis, self.data_buffer_five, pen=pg.mkPen((255, 0, 0), width=2))
        self.curve_six = my_plot_three.plot(self.x_axis, self.data_buffer_six, pen=pg.mkPen((0, 0, 255), width=2))

        # Adicionando as Legendas no Gráfico 1
        self.legend_one = pg.LegendItem((30, 10), offset=(70, 10))
        self.legend_one.setParentItem(my_plot_one.graphicsItem())
        self.legend_one.addItem(self.curve_one, 'X ')
        self.legend_one.addItem(self.curve_two, 'Y ')

        # Adicionando as Legendas no Gráfico 2
        self.legend_two = pg.LegendItem((30, 10), offset=(70, 30))
        self.legend_two.setParentItem(my_plot_two.graphicsItem())
        self.legend_two.addItem(self.curve_three, 'X SP')
        self.legend_two.addItem(self.curve_four, 'X CP')

        # Adicionando as Legendas no Gráfico 3
        self.legend_three = pg.LegendItem(size=(10, 10), offset=(70, 30))
        self.legend_three.setParentItem(my_plot_three.graphicsItem())
        self.legend_three.addItem(self.curve_five, 'Y SP')
        self.legend_three.addItem(self.curve_six, 'Y CP')

    def start_app(self):
        """
        This function start all threads and starts the Widget
        """
        # If the Start button is in the mode "Start"
        if self.start_button.text() == 'Start':

            # To prevent any not connected device error, start the app always with video feed from the embedded webcam
            self.video_source = WebcamVideoStream(src=0).start()
            self.current_output = 0

            if self.start_arduino_connection.is_connected:
                self.start_signal.emit(True)

            # Iniciando o QTimer
            self.timer.timeout.connect(self.videoProcessing)
            self.timer.timeout.connect(self.update_widgets)
            self.timer.start(self.TIME)

            self.start_button.setText("Pause")
            self.serial_connect_button.setEnabled(False)
            self.access_point_button.setEnabled(False)
            self.quit_button.setEnabled(False)

            # Iniciando o armazenamento do temporizador
            self.start_time = time.time()
            self.previous_time = self.start_time
            self.loop_time = 0
            self.update_widgets_time = 0
            self.video_processing_time = 0
            self.arduino_communication_time = 0

        # Executar quando apertar o botão Pause
        elif self.start_button.text() == 'Pause':
            self.timer.stop()
            self.start_button.setText("Resume")
            if self.start_arduino_connection.is_connected:
                self.start_signal.emit(False)
            self.serial_connect_button.setEnabled(True)
            if os.name == 'posix':
                self.access_point_button.setEnabled(True)
            self.quit_button.setEnabled(True)

        # Executar quando apertar o botão Start
        else:
            self.timer.start(self.TIME)
            self.start_button.setText("Pause")
            if self.start_arduino_connection.is_connected:
                self.start_signal.emit(True)
            self.serial_connect_button.setEnabled(False)
            self.access_point_button.setEnabled(False)
            self.quit_button.setEnabled(False)

    def connect_serial(self):
        """
        This function handles the arduino serial connection using the QThread method
        """
        if self.serial_connect_button.text() == 'Serial connect' and self.start_button.text() != 'Pause':
            # self.start_arduino_connection = ArduinoComunication()
            self.start_arduino_connection.start()
            self.start_arduino_connection.arduino_data.connect(self.get_data_from_arduino)
            self.serial_connect_button.setText("Serial disconnect")

        elif self.serial_connect_button.text() == 'Serial disconnect':
            self.start_arduino_connection.stop()
            # del self.start_arduino_connection
            self.serial_connect_button.setText("Serial connect")

    def toggle_access_point(self):
        """
        Method to start/stop the access point thread
        """

        if os.name != 'posix':
            print("This Access Point module works only on Linux, sorry!")
        else:
            if self.access_point_button.text() == "Start server":
                self.access_point_button.setText("Stop server")
                self.access_point_server.start()
            else:
                self.access_point_button.setText("Start server")
                self.access_point_server.stop()

    def change_threshold_value(self):
        """
        This function handles the selection of the threshold frame to be displayed
        """
        sliders = [self.slider_r_low, self.slider_g_low, self.slider_b_low,
                   self.slider_r_high, self.slider_g_high, self.slider_b_high]

        labels = [self.text_r_low_value_label, self.text_g_low_value_label, self.text_b_low_value_label,
                  self.text_r_high_value_label, self.text_g_high_value_label, self.text_b_high_value_label]

        if self.thresh_button.text() == 'Ball':
            self.thresh_button.setText("Plate")

            for index, (slider, label) in enumerate(zip(sliders, labels)):
                slider.setValue(self.threshold_plate[index])
                label.setText(str(self.threshold_plate[index]))

        else:
            self.thresh_button.setText("Ball")

            for index, (slider, label) in enumerate(zip(sliders, labels)):
                slider.setValue(self.threshold_ball[index])
                label.setText(str(self.threshold_ball[index]))

    def handle_close_event(self):
        """
        Method to handle the cloe event from the application
        """
        if self.timer.isActive():
            print("Stopping Timer...")
            self.timer.stop()
            print("Done!")
        if self.access_point_button.text() == 'Stop server':
            print("Shutting down the WiFi Server")
            self.access_point_server.stop()
            print("Done!")
        if self.start_button.text() != 'Start':
            print("Stopping Video Stream Thread...")
            self.video_source.stop()
            print("Done!")
        if self.serial_connect_button.text() == 'Serial disconnect':
            print("Stopping Serial Data Communication...")
            self.start_arduino_connection.stop()
            print("Done!")
        print("Exiting...")
        time.sleep(1)

    # pylint: disable=invalid-name
    # This method name can't be snake_case because it overrides a PyQt5 native function
    def closeEvent(self, event):
        """
        This function handles the close event (Pop up message to exit the application)
        """
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.handle_close_event()
            event.accept()
        else:
            event.ignore()

    def video_input_change(self, text):
        """
        This function handles the video input change from the combobox
        """
        if self.start_button.text() != 'Start':
            if text == 'Webcam' and self.current_output != 0:
                self.video_source.stop()
                self.video_source = WebcamVideoStream(src=0).start()
                self.current_output = 0
            elif text == 'USB Camera' and self.current_output != 1:
                self.video_source.stop()
                self.video_source = WebcamVideoStream(src=1).start()
                self.current_output = 1
            elif text == 'IP Camera' and self.current_output != 2:
                self.video_source.stop()
                website = 'http://' + self.ip_value + ':8080/video'
                self.video_source = WebcamVideoStream(src=website).start()
                self.current_output = 2
            else:
                print("This video is already selected")

    def set_video_ip(self):
        """
        Method to set the ip adress of the remote camera
        """
        self.ip_value = self.camera_ip_textbox.text()

    def mode_change(self, text):
        """
        This function handles the mode change from the combobox
        """
        self.move_pattern = text

    def step_change(self, text):
        """
        This function handles the change on step size
        """
        self.step = int(text)

    def radius_change(self, text):
        """
        This function handles the change on radius size
        """
        if text == '2.5':
            self.circle_radius = 50
        elif text == '5.0':
            self.circle_radius = 100
        elif text == '7.5':
            self.circle_radius = 150

    def slider_value_change(self, number=None, text_value_label=None, slider=None):
        """
        This function handles the value change of the sliders
        """
        if self.thresh_button.text() == 'Ball':
            self.threshold_ball[number] = slider.value()
            text_value_label.setText(str(self.threshold_ball[number]))
        else:
            self.threshold_plate[number] = slider.value()
            text_value_label.setText(str(self.threshold_plate[number]))

    def set_setpoint_type(self):
        """
        This function sets the correct setpoint variable according to the choosen mode
        """
        if self.move_pattern == 'Center':
            self.setpoint_pixels = (0, 0)
        elif self.move_pattern == 'Mouse':
            self.setpoint_pixels = self.setpoint_mouse
        elif self.move_pattern == 'Joystick':
            self.setpoint_pixels = self.setpoint_joystick
        elif self.move_pattern == 'Square':
            self.setpoint_pixels = self.setpoint_square[int(((time.time() - self.start_time)/4) % 4)]
        elif self.move_pattern == 'Circle':
            pointX = int(self.circle_radius * math.cos(self.step/3 * (time.time() - self.start_time) * math.pi))
            pointY = int(self.circle_radius * math.sin(self.step/3 * (time.time() - self.start_time) * math.pi))
            self.setpoint_pixels = (pointX, pointY)
        elif self.move_pattern == 'Lissajous':
            pointX = int(120 * math.cos(self.step/4 * (time.time() - self.start_time) * math.pi))
            pointY = int(80 * math.sin(2 * self.step/4 * (time.time() - self.start_time) * math.pi))
            self.setpoint_pixels = (pointX, pointY)

    def update_graph(self, input_list):
        """
        This function updates all three graphs data
        """
        # Armazenando os dados recebidos pela função nos buffers
        self.data_buffer_one.append(input_list[0])
        self.data_buffer_two.append(input_list[1])
        self.data_buffer_three.append(input_list[2])
        self.data_buffer_four.append(input_list[3])
        self.data_buffer_five.append(input_list[4])
        self.data_buffer_six.append(input_list[5])
        # Atualizando as variáveis de curva x e y de cada gráfico
        self.curve_one.setData(self.x_axis, self.data_buffer_one)
        self.curve_two.setData(self.x_axis, self.data_buffer_two)
        self.curve_three.setData(self.x_axis, self.data_buffer_three)
        self.curve_four.setData(self.x_axis, self.data_buffer_four)
        self.curve_five.setData(self.x_axis, self.data_buffer_five)
        self.curve_six.setData(self.x_axis, self.data_buffer_six)

    def update_joystick_position(self, joystick_x, joystick_y):
        """
        This function updates the points of the joystick setpoint variable
        """
        self.joystick_points.appendleft((joystick_x, joystick_y))
        xList, yList = zip(*self.joystick_points)
        self.setpoint_joystick = (int(np.mean(xList)), int(np.mean(yList)))

    def pixelToCentimeter(self, px_value):
        """
        This function converts the value from pixels to centimeters
        """
        return round(0.05 * px_value[0], 2), round(0.05 * px_value[1], 2)

    def image_to_qimage(self, image):
        """
        This function converts the processed frame to a QtGui.QImage, which is needed to be displayed on the widget
        """
        height, width, __ = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return q_image

    def setup_kalman_filter(self):
        """
        This function sets up the Kalman Filter parameters
        """
        self.kalman = cv2.KalmanFilter(4, 2)
        self.kalman.measurementMatrix = np.array([[1, 0, 0, 0],
                                                  [0, 1, 0, 0]], np.float32)

        self.kalman.transitionMatrix = np.array([[1, 0, 1, 0],
                                                 [0, 1, 0, 1],
                                                 [0, 0, 1, 0],
                                                 [0, 0, 0, 1]], np.float32)

        self.kalman.processNoiseCov = np.array([[1, 0, 0, 0],
                                                [0, 1, 0, 0],
                                                [0, 0, 1, 0],
                                                [0, 0, 0, 1]], np.float32) * 0.03

        self.prediction = np.zeros((2, 1), np.float32)

    def mousePressEvent(self, event):
        """
        This function handles the mouse press event, to setting the setpoint in mouse mode
        """
        if event.button() == Qt.LeftButton:
            if (493 < event.x() < 893) and (121 < event.y() < 521) and (self.move_pattern == 'Mouse'):
                valueX = event.x() - 693
                valueY = -event.y() + 321
                self.setpoint_mouse = (valueX, valueY)

    def videoProcessing(self):
        """
        This function does all the video processing, wich includes:
        tracking the ball, tracking the corners of the moving plate, and apllying all the filters
        """
        tick_one = cv2.getTickCount()
        # Capture the Camera Frame
        frame = self.video_source.read()
        try:
            frame = frame[15:465, 95:545]
        except TypeError:
            print("Failed to capture image!")
            if self.start_button.text() == 'Pause':
                self.timer.stop()
                self.start_button.setText("Resume")
                if self.start_arduino_connection.is_connected:
                    self.start_signal.emit(False)
                self.serial_connect_button.setEnabled(True)
                if os.name != 'posix':
                    self.access_point_button.setEnabled(True)
                self.quit_button.setEnabled(True)
            return
        frame = imutils.rotate(frame, 90)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.image = frame.copy()
        blurred_rgb = cv2.medianBlur(frame, 5)

        # Create a Kernel
        kernel = np.ones((5, 5), np.uint8)
        # Create and process the mask, which will show a binary image
        mask_rgb = cv2.inRange(blurred_rgb, tuple(self.threshold_plate[0:3]), tuple(self.threshold_plate[3:6]))
        mask_rgb = cv2.morphologyEx(mask_rgb, cv2.MORPH_CLOSE, kernel)
        mask_rgb[0:450, 120:330] = [0]
        mask_rgb[120:330, 0:450] = [0]

        self.mask_3ch_rgb = cv2.cvtColor(mask_rgb, cv2.COLOR_GRAY2BGR)

        contours, _ = cv2.findContours(mask_rgb.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        self.pts_list = [[0, 0], [0, 0], [0, 0], [0, 0]]
        for contour in contours:
            moments = cv2.moments(contour)
            if moments['m00'] > 200:
                center_x = int(moments['m10']/moments['m00'])
                center_y = int(moments['m01']/moments['m00'])
                if center_x < 150:
                    if center_y < 120:
                        self.pts_list[0][0] = int(center_x)
                        self.pts_list[0][1] = int(center_y)
                    else:
                        self.pts_list[3][0] = int(center_x)
                        self.pts_list[3][1] = int(center_y)
                else:
                    if center_y < 150:
                        self.pts_list[1][0] = int(center_x)
                        self.pts_list[1][1] = int(center_y)
                    else:
                        self.pts_list[2][0] = int(center_x)
                        self.pts_list[2][1] = int(center_y)

        points_one = np.float32([[self.pts_list[0][0], self.pts_list[0][1]],
                                 [self.pts_list[1][0], self.pts_list[1][1]],
                                 [self.pts_list[2][0], self.pts_list[2][1]],
                                 [self.pts_list[3][0], self.pts_list[3][1]]])
        points_two = np.float32([[45, 45], [405, 45], [405, 405], [45, 405]])

        self.black = np.zeros((450, 450, 3), np.uint8)
        perspective = cv2.getPerspectiveTransform(points_one, points_two)
        self.warped = cv2.warpPerspective(frame, perspective, (450, 450))

        warped_scrot = self.warped[30:420, 30:420]

        blur = cv2.medianBlur(warped_scrot, 5)

        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 500, param1=60, param2=20, minRadius=15, maxRadius=40)

        if circles is not None:
            self.without_ball = 0
            x = int(circles[0][0][0]) + 30
            y = int(circles[0][0][1]) + 30
            radius = circles[0][0][2]
            self.center_pixels = np.array([np.float32(x - self.IMAGE_SIZE.width()/2),
                                           np.float32(self.IMAGE_SIZE.height()/2 - y)], np.float32)
            if 190 > self.center_pixels[0] > -190 and 190 > self.center_pixels[1] > -190:
                self.radius = radius
                self.kalman.correct(self.center_pixels)
                self.prediction = self.kalman.predict()

        else:
            # If lost tracking of the ball, use kalman prediction for a certain period of time
            if self.without_ball < 20:
                self.prediction = self.kalman.predict()
                self.without_ball += 1
            else:
                self.radius = 0
                self.prediction[0][0] = 0
                self.prediction[1][0] = 0

        # Updating the point array
        self.d_x = round(self.prediction[2][0], 2)
        self.d_y = round(self.prediction[3][0], 2)

        # Updating Set Point according to choosen mode
        self.set_setpoint_type()
        self.error_pixels = (self.setpoint_pixels[0] - self.prediction[0][0],
                             self.setpoint_pixels[1] - self.prediction[1][0])

        # Centimeters conversion
        self.error_centimeters = self.pixelToCentimeter(self.error_pixels)
        self.center_centimeters = self.pixelToCentimeter((self.prediction[0][0], self.prediction[1][0]))
        self.setpoint_centimeters = self.pixelToCentimeter(self.setpoint_pixels)

        self.coordinate_values = (self.error_centimeters, self.center_centimeters, self.setpoint_centimeters)

        self.centers_signal.emit(self.center_centimeters, self.setpoint_centimeters)

        tick_two = cv2.getTickCount()
        self.video_processing_time = (tick_two - tick_one)/cv2.getTickFrequency()

    def get_data_from_arduino(self, data):
        """
        This function handles the data sent from the arduino communication QThread
        """
        self.angle_x = data[0]
        self.angle_y = data[1]
        self.joystick_x = data[2]
        self.joystick_y = data[3]
        self.arduino_communication_time = data[4]

    def get_arduino_data(self, application_object):
        """
        Metho to connect the arduino data signal to the main app
        """
        application_object.arduino_data.connect(self.get_data_from_arduino)

    def update_widgets(self):
        """
        Method to update the app widgets data
        """
        initial_time = time.time()
        self.update_joystick_position(self.joystick_x, self.joystick_y)

        self.update_graph([self.error_centimeters[0], self.error_centimeters[1],
                           self.setpoint_centimeters[0], self.center_centimeters[0],
                           self.setpoint_centimeters[1], self.center_centimeters[1]])

        self.update_gui(self.warped, self.black, self.image)

        if self.thresh_button.text() == 'Ball':
            image_one = self.image_to_qimage(self.image)
        else:
            image_one = self.image_to_qimage(self.mask_3ch_rgb)

        image_two = self.image_to_qimage(self.warped)
        image_three = self.image_to_qimage(self.black)

        # Update the QLabel Widget with all processed images
        self.image_label_one.setPixmap(QPixmap.fromImage(image_one))
        self.image_label_two.setPixmap(QPixmap.fromImage(image_two))
        self.image_label_three.setPixmap(QPixmap.fromImage(image_three))

        final_time = time.time()
        self.update_widgets_time = final_time - initial_time

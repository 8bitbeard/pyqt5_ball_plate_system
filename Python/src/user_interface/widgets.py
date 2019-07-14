"""
This file defines all the main app wigets
"""

import os

import pyqtgraph as pg

from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit, QPushButton, QSlider, QGridLayout
from PyQt5.QtCore import QTimer, QSize, Qt


class AppWidgets(object):
    """
    Class to define all widgets. This will be inherited by the main app
    """

    # Defining Wiget sizes
    TEXT_SIZE = QSize(35, 15)
    SMALL_TEXT_SIZE = QSize(26, 15)
    LARGE_TEXT_SIZE = QSize(85, 15)
    VIDEO_SIZE = QSize(450, 450)
    GRAPH_SIZE = QSize(450, 210)
    BUTTON_SIZE = QSize(150, 25)
    SLIDER_SIZE = QSize(170, 15)
    TEXT_BOX_SIZE = QSize(270, 25)
    COMBO_BOX_SIZE = QSize(105, 25)

    def __init__(self):
        super(AppWidgets).__init__()

        self.ip_value = '192.168.12.186'
        # Lower and Upper Threshold values
        self.threshold_ball = [0, 0, 145, 0, 0, 255]
        self.threshold_plate = [0, 178, 0, 255, 255, 218]

        # Initializing the QTimer
        self.timer = QTimer(self)

        # Video Widgets
        self.image_label_one = QLabel()
        self.image_label_two = QLabel()
        self.image_label_three = QLabel()

        # Video output ComboBox
        self.combo_box_one = QComboBox()
        self.combo_box_one.addItem("Webcam")
        self.combo_box_one.addItem("USB Camera")
        self.combo_box_one.addItem("IP Camera")
        self.text_combo_box_one = QLabel(text='Video Input:')
        self.text_combo_box_one.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Pattern type ComboBox
        self.combo_box_two = QComboBox()
        self.combo_box_two.addItem("Center")
        self.combo_box_two.addItem("Mouse")
        self.combo_box_two.addItem("Joystick")
        self.combo_box_two.addItem("Square")
        self.combo_box_two.addItem("Circle")
        self.combo_box_two.addItem("Lissajous")
        self.text_combo_box_two = QLabel(text='Mode:')
        self.text_combo_box_two.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Step value ComboBox
        self.combo_box_three = QComboBox()
        self.combo_box_three.addItem("1")
        self.combo_box_three.addItem("2")
        self.combo_box_three.addItem("3")
        self.text_combo_box_three = QLabel(text='Step time (s):')
        self.text_combo_box_three.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Radius value ComboBox
        self.combo_box_four = QComboBox()
        self.combo_box_four.addItem("2.5")
        self.combo_box_four.addItem("5.0")
        self.combo_box_four.addItem("7.5")
        self.text_combo_box_four = QLabel(text='Radius (cm):')
        self.text_combo_box_four.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Creating the ip line edit box
        self.camera_ip_textbox = QLineEdit()
        self.camera_ip_textbox.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.camera_ip_textbox.setText(self.ip_value)
        font = self.camera_ip_textbox.font()
        font.setPointSize(12)
        self.camera_ip_textbox.setFont(font)

        # Creating the ip line edit box label
        self.camera_ip_label = QLabel(text='Camera IP:')
        self.camera_ip_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Creating the Start/Pause button for the video feed
        self.start_button = QPushButton("Start")

        # Creating the Connect/Disconnect for Arduino communication
        self.serial_connect_button = QPushButton("Serial connect")

        # Creating the Quit button
        self.quit_button = QPushButton("Quit")

        # Creating the Threshold button for the Widget
        self.thresh_button = QPushButton("Ball")

        # Creating the start Acess Point button
        self.access_point_button = QPushButton("Start server")
        if os.name != 'posix':
            self.access_point_button.setEnabled(False)

        # Creating the set ip button
        self.select_ip_button = QPushButton("Set IP")

        # Text labels for Sliders type
        self.text_r_low_label = QLabel(text='B:')
        self.text_r_low_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.text_g_low_label = QLabel(text='G:')
        self.text_g_low_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.text_b_low_label = QLabel(text='R:')
        self.text_b_low_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.text_r_high_label = QLabel(text='B:')
        self.text_r_high_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.text_g_high_label = QLabel(text='G:')
        self.text_g_high_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.text_b_high_label = QLabel(text='R:')
        self.text_b_high_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Text labels for Sliders values
        self.text_r_low_value_label = QLabel(text=str(self.threshold_ball[0]))
        self.text_g_low_value_label = QLabel(text=str(self.threshold_ball[1]))
        self.text_b_low_value_label = QLabel(text=str(self.threshold_ball[2]))
        self.text_r_high_value_label = QLabel(text=str(self.threshold_ball[3]))
        self.text_g_high_value_label = QLabel(text=str(self.threshold_ball[4]))
        self.text_b_high_value_label = QLabel(text=str(self.threshold_ball[5]))

        # Creating the lower threshold slider for the red color
        self.slider_r_low = QSlider(Qt.Horizontal)
        self.slider_r_low.setMinimum(0)
        self.slider_r_low.setMaximum(255)
        self.slider_r_low.setValue(self.threshold_ball[0])

        # Creating the lower threshold slider for the green color
        self.slider_g_low = QSlider(Qt.Horizontal)
        self.slider_g_low.setMinimum(0)
        self.slider_g_low.setMaximum(255)
        self.slider_g_low.setValue(self.threshold_ball[1])

        # Creating the lower threshold slider for the blue color
        self.slider_b_low = QSlider(Qt.Horizontal)
        self.slider_b_low.setMinimum(0)
        self.slider_b_low.setMaximum(255)
        self.slider_b_low.setValue(self.threshold_ball[2])

        # Creating the upper threshold slider for the red color
        self.slider_r_high = QSlider(Qt.Horizontal)
        self.slider_r_high.setMinimum(0)
        self.slider_r_high.setMaximum(255)
        self.slider_r_high.setValue(self.threshold_ball[3])

        # Creating the upper threshold slider for the green color
        self.slider_g_high = QSlider(Qt.Horizontal)
        self.slider_g_high.setMinimum(0)
        self.slider_g_high.setMaximum(255)
        self.slider_g_high.setValue(self.threshold_ball[4])

        # Creating the upper threshold slider for the blue color
        self.slider_b_high = QSlider(Qt.Horizontal)
        self.slider_b_high.setMinimum(0)
        self.slider_b_high.setMaximum(255)
        self.slider_b_high.setValue(self.threshold_ball[5])

        # Graph 1
        self.graph_one = pg.GraphicsWindow()

        # Graph 2
        self.graph_two = pg.GraphicsWindow()

        # Graph 3
        self.graph_three = pg.GraphicsWindow()

        self.set_grid_layout()

    def set_grid_layout(self):
        """
        Method to create and organize the main widget layout
        """
        # Creating the Widget layout
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.start_button, 0, 0)
        self.main_layout.addWidget(self.quit_button, 0, 1)
        self.main_layout.addWidget(self.text_combo_box_one, 0, 2)
        self.main_layout.addWidget(self.combo_box_one, 0, 3)
        self.main_layout.addWidget(self.text_combo_box_two, 0, 4)
        self.main_layout.addWidget(self.combo_box_two, 0, 5)
        self.main_layout.addWidget(self.text_r_low_label, 0, 6)
        self.main_layout.addWidget(self.slider_r_low, 0, 7)
        self.main_layout.addWidget(self.text_r_low_value_label, 0, 8)
        self.main_layout.addWidget(self.text_r_high_label, 0, 9)
        self.main_layout.addWidget(self.slider_r_high, 0, 10)
        self.main_layout.addWidget(self.text_r_high_value_label, 0, 11)

        self.main_layout.addWidget(self.access_point_button, 1, 0)
        self.main_layout.addWidget(self.serial_connect_button, 1, 1)
        self.main_layout.addWidget(self.text_combo_box_three, 1, 2)
        self.main_layout.addWidget(self.combo_box_three, 1, 3)
        self.main_layout.addWidget(self.text_combo_box_four, 1, 4)
        self.main_layout.addWidget(self.combo_box_four, 1, 5)
        self.main_layout.addWidget(self.text_g_low_label, 1, 6)
        self.main_layout.addWidget(self.slider_g_low, 1, 7)
        self.main_layout.addWidget(self.text_g_low_value_label, 1, 8)
        self.main_layout.addWidget(self.text_g_high_label, 1, 9)
        self.main_layout.addWidget(self.slider_g_high, 1, 10)
        self.main_layout.addWidget(self.text_g_high_value_label, 1, 11)

        self.main_layout.addWidget(self.thresh_button, 2, 0)
        self.main_layout.addWidget(self.select_ip_button, 2, 1)
        self.main_layout.addWidget(self.camera_ip_label, 2, 2)
        self.main_layout.addWidget(self.camera_ip_textbox, 2, 3, 1, 3)
        self.main_layout.addWidget(self.text_b_low_label, 2, 6)
        self.main_layout.addWidget(self.slider_b_low, 2, 7)
        self.main_layout.addWidget(self.text_b_low_value_label, 2, 8)
        self.main_layout.addWidget(self.text_b_high_label, 2, 9)
        self.main_layout.addWidget(self.slider_b_high, 2, 10)
        self.main_layout.addWidget(self.text_b_high_value_label, 2, 11)

        self.video_layout = QGridLayout()
        self.video_layout.addWidget(self.image_label_one, 0, 0)
        self.video_layout.addWidget(self.image_label_two, 0, 1)
        self.video_layout.addWidget(self.image_label_three, 0, 2)

        self.graph_layout = QGridLayout()
        self.graph_layout.addWidget(self.graph_one, 0, 1)
        self.graph_layout.addWidget(self.graph_two, 0, 2)
        self.graph_layout.addWidget(self.graph_three, 0, 3)

        self.main_layout.addLayout(self.video_layout, 3, 0, 1, 12)
        self.main_layout.addLayout(self.graph_layout, 4, 0, 1, 12)

    def set_widgets_size(self, ratio=1):
        """
        Method to set all the widgets size ratio
        """
        self.image_label_one.setFixedSize(self.VIDEO_SIZE * ratio)
        self.image_label_one.setFixedSize(self.VIDEO_SIZE * ratio)
        self.image_label_two.setFixedSize(self.VIDEO_SIZE * ratio)
        self.image_label_three.setFixedSize(self.VIDEO_SIZE * ratio)
        self.combo_box_one.setFixedSize(self.COMBO_BOX_SIZE * ratio)
        self.text_combo_box_one.setFixedSize(self.LARGE_TEXT_SIZE * ratio)
        self.combo_box_two.setFixedSize(self.COMBO_BOX_SIZE * ratio)
        self.text_combo_box_two.setFixedSize(self.LARGE_TEXT_SIZE * ratio)
        self.combo_box_three.setFixedSize(self.COMBO_BOX_SIZE * ratio)
        self.text_combo_box_three.setFixedSize(self.LARGE_TEXT_SIZE * ratio)
        self.combo_box_four.setFixedSize(self.COMBO_BOX_SIZE * ratio)
        self.text_combo_box_four.setFixedSize(self.LARGE_TEXT_SIZE * ratio)
        self.camera_ip_textbox.setFixedSize(self.TEXT_BOX_SIZE * ratio)
        self.camera_ip_label.setFixedSize(self.LARGE_TEXT_SIZE * ratio)
        self.start_button.setFixedSize(self.BUTTON_SIZE * ratio)
        self.serial_connect_button.setFixedSize(self.BUTTON_SIZE * ratio)
        self.quit_button.setFixedSize(self.BUTTON_SIZE * ratio)
        self.thresh_button.setFixedSize(self.BUTTON_SIZE * ratio)
        self.access_point_button.setFixedSize(self.BUTTON_SIZE * ratio)
        self.select_ip_button.setFixedSize(self.BUTTON_SIZE * ratio)
        self.text_r_low_label.setFixedSize(self.SMALL_TEXT_SIZE * ratio)
        self.text_g_low_label.setFixedSize(self.SMALL_TEXT_SIZE * ratio)
        self.text_b_low_label.setFixedSize(self.SMALL_TEXT_SIZE * ratio)
        self.text_r_high_label.setFixedSize(self.SMALL_TEXT_SIZE * ratio)
        self.text_g_high_label.setFixedSize(self.SMALL_TEXT_SIZE * ratio)
        self.text_b_high_label.setFixedSize(self.SMALL_TEXT_SIZE * ratio)
        self.text_r_low_value_label.setFixedSize(self.TEXT_SIZE * ratio)
        self.text_g_low_value_label.setFixedSize(self.TEXT_SIZE * ratio)
        self.text_b_low_value_label.setFixedSize(self.TEXT_SIZE * ratio)
        self.text_r_high_value_label.setFixedSize(self.TEXT_SIZE * ratio)
        self.text_g_high_value_label.setFixedSize(self.TEXT_SIZE * ratio)
        self.text_b_high_value_label.setFixedSize(self.TEXT_SIZE * ratio)
        self.slider_r_low.setFixedSize(self.SLIDER_SIZE * ratio)
        self.slider_g_low.setFixedSize(self.SLIDER_SIZE * ratio)
        self.slider_b_low.setFixedSize(self.SLIDER_SIZE * ratio)
        self.slider_r_high.setFixedSize(self.SLIDER_SIZE * ratio)
        self.slider_g_high.setFixedSize(self.SLIDER_SIZE * ratio)
        self.slider_b_high.setFixedSize(self.SLIDER_SIZE * ratio)
        self.graph_one.setFixedSize(self.GRAPH_SIZE * ratio)
        self.graph_two.setFixedSize(self.GRAPH_SIZE * ratio)
        self.graph_three.setFixedSize(self.GRAPH_SIZE * ratio)

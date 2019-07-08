"""
This file defines all the main app wigets
"""

import os

import pyqtgraph as pg

from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit, QPushButton, QSlider, QVBoxLayout, QHBoxLayout
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
    BUTTON_SIZE = QSize(120, 22)
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
        self.image_label_one.setFixedSize(self.VIDEO_SIZE)
        self.image_label_two = QLabel()
        self.image_label_two.setFixedSize(self.VIDEO_SIZE)
        self.image_label_three = QLabel()
        self.image_label_three.setFixedSize(self.VIDEO_SIZE)

        # Video output ComboBox
        self.combo_box_one = QComboBox()
        self.combo_box_one.addItem("Webcam")
        self.combo_box_one.addItem("USB Camera")
        self.combo_box_one.addItem("IP Camera")
        self.combo_box_one.setFixedSize(self.COMBO_BOX_SIZE)
        self.text_combo_box_one = QLabel(text='Video Input:')
        self.text_combo_box_one.setFixedSize(self.LARGE_TEXT_SIZE)
        self.text_combo_box_one.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Pattern type ComboBox
        self.combo_box_two = QComboBox()
        self.combo_box_two.addItem("Center")
        self.combo_box_two.addItem("Mouse")
        self.combo_box_two.addItem("Joystick")
        self.combo_box_two.addItem("Square")
        self.combo_box_two.addItem("Circle")
        self.combo_box_two.addItem("Lissajous")
        self.combo_box_two.setFixedSize(self.COMBO_BOX_SIZE)
        self.text_combo_box_two = QLabel(text='Mode:')
        self.text_combo_box_two.setFixedSize(self.LARGE_TEXT_SIZE)
        self.text_combo_box_two.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Step value ComboBox
        self.combo_box_three = QComboBox()
        self.combo_box_three.addItem("1")
        self.combo_box_three.addItem("2")
        self.combo_box_three.addItem("3")
        self.combo_box_three.setFixedSize(self.COMBO_BOX_SIZE)
        self.text_combo_box_three = QLabel(text='Step time (s):')
        self.text_combo_box_three.setFixedSize(self.LARGE_TEXT_SIZE)
        self.text_combo_box_three.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Radius value ComboBox
        self.combo_box_four = QComboBox()
        self.combo_box_four.addItem("2.5")
        self.combo_box_four.addItem("5.0")
        self.combo_box_four.addItem("7.5")
        self.combo_box_four.setFixedSize(self.COMBO_BOX_SIZE)
        self.text_combo_box_four = QLabel(text='Radius (cm):')
        self.text_combo_box_four.setFixedSize(self.LARGE_TEXT_SIZE)
        self.text_combo_box_four.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Creating the ip line edit box
        self.camera_ip_textbox = QLineEdit()
        self.camera_ip_textbox.setFixedSize(self.TEXT_BOX_SIZE)
        self.camera_ip_textbox.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.camera_ip_textbox.setText(self.ip_value)
        font = self.camera_ip_textbox.font()
        font.setPointSize(12)
        self.camera_ip_textbox.setFont(font)

        # Creating the ip line edit box label
        self.camera_ip_label = QLabel(text='Camera IP:')
        self.camera_ip_label.setFixedSize(self.LARGE_TEXT_SIZE)
        self.camera_ip_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Creating the Start/Pause button for the video feed
        self.start_button = QPushButton("Start")
        self.start_button.setFixedSize(self.BUTTON_SIZE)

        # Creating the Connect/Disconnect for Arduino communication
        self.serial_connect_button = QPushButton("Serial connect")
        self.serial_connect_button.setFixedSize(self.BUTTON_SIZE)

        # Creating the Quit button
        self.quit_button = QPushButton("Quit")
        self.quit_button.setFixedSize(self.BUTTON_SIZE)

        # Creating the Threshold button for the Widget
        self.thresh_button = QPushButton("Ball")
        self.thresh_button.setFixedSize(self.BUTTON_SIZE)

        # Creating the start Acess Point button
        self.access_point_button = QPushButton("Start server")
        self.access_point_button.setFixedSize(self.BUTTON_SIZE)
        if os.name != 'posix':
            self.access_point_button.setEnabled(False)

        # Creating the set ip button
        self.select_ip_button = QPushButton("Set IP")
        self.select_ip_button.setFixedSize(self.BUTTON_SIZE)

        # Text labels for Sliders type
        self.text_r_low_label = QLabel(text='B:')
        self.text_r_low_label.setFixedSize(self.SMALL_TEXT_SIZE)
        self.text_r_low_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.text_g_low_label = QLabel(text='G:')
        self.text_g_low_label.setFixedSize(self.SMALL_TEXT_SIZE)
        self.text_g_low_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.text_b_low_label = QLabel(text='R:')
        self.text_b_low_label.setFixedSize(self.SMALL_TEXT_SIZE)
        self.text_b_low_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.text_r_high_label = QLabel(text='B:')
        self.text_r_high_label.setFixedSize(self.SMALL_TEXT_SIZE)
        self.text_r_high_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.text_g_high_label = QLabel(text='G:')
        self.text_g_high_label.setFixedSize(self.SMALL_TEXT_SIZE)
        self.text_g_high_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.text_b_high_label = QLabel(text='R:')
        self.text_b_high_label.setFixedSize(self.SMALL_TEXT_SIZE)
        self.text_b_high_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Text labels for Sliders values
        self.text_r_low_value_label = QLabel(text=str(self.threshold_ball[0]))
        self.text_r_low_value_label.setFixedSize(self.TEXT_SIZE)
        self.text_g_low_value_label = QLabel(text=str(self.threshold_ball[1]))
        self.text_g_low_value_label.setFixedSize(self.TEXT_SIZE)
        self.text_b_low_value_label = QLabel(text=str(self.threshold_ball[2]))
        self.text_b_low_value_label.setFixedSize(self.TEXT_SIZE)
        self.text_r_high_value_label = QLabel(text=str(self.threshold_ball[3]))
        self.text_r_high_value_label.setFixedSize(self.TEXT_SIZE)
        self.text_g_high_value_label = QLabel(text=str(self.threshold_ball[4]))
        self.text_g_high_value_label.setFixedSize(self.TEXT_SIZE)
        self.text_b_high_value_label = QLabel(text=str(self.threshold_ball[5]))
        self.text_b_high_value_label.setFixedSize(self.TEXT_SIZE)

        # Creating the lower threshold slider for the red color
        self.slider_r_low = QSlider(Qt.Horizontal)
        self.slider_r_low.setFixedSize(self.SLIDER_SIZE)
        self.slider_r_low.setMinimum(0)
        self.slider_r_low.setMaximum(255)
        self.slider_r_low.setValue(self.threshold_ball[0])

        # Creating the lower threshold slider for the green color
        self.slider_g_low = QSlider(Qt.Horizontal)
        self.slider_g_low.setFixedSize(self.SLIDER_SIZE)
        self.slider_g_low.setMinimum(0)
        self.slider_g_low.setMaximum(255)
        self.slider_g_low.setValue(self.threshold_ball[1])

        # Creating the lower threshold slider for the blue color
        self.slider_b_low = QSlider(Qt.Horizontal)
        self.slider_b_low.setFixedSize(self.SLIDER_SIZE)
        self.slider_b_low.setMinimum(0)
        self.slider_b_low.setMaximum(255)
        self.slider_b_low.setValue(self.threshold_ball[2])

        # Creating the upper threshold slider for the red color
        self.slider_r_high = QSlider(Qt.Horizontal)
        self.slider_r_high.setFixedSize(self.SLIDER_SIZE)
        self.slider_r_high.setMinimum(0)
        self.slider_r_high.setMaximum(255)
        self.slider_r_high.setValue(self.threshold_ball[3])

        # Creating the upper threshold slider for the green color
        self.slider_g_high = QSlider(Qt.Horizontal)
        self.slider_g_high.setFixedSize(self.SLIDER_SIZE)
        self.slider_g_high.setMinimum(0)
        self.slider_g_high.setMaximum(255)
        self.slider_g_high.setValue(self.threshold_ball[4])

        # Creating the upper threshold slider for the blue color
        self.slider_b_high = QSlider(Qt.Horizontal)
        self.slider_b_high.setFixedSize(self.SLIDER_SIZE)
        self.slider_b_high.setMinimum(0)
        self.slider_b_high.setMaximum(255)
        self.slider_b_high.setValue(self.threshold_ball[5])

        # Graph 1
        self.graph_one = pg.GraphicsWindow()
        self.graph_one.setFixedSize(self.GRAPH_SIZE)

        # Graph 2
        self.graph_two = pg.GraphicsWindow()
        self.graph_two.setFixedSize(self.GRAPH_SIZE)

        # Graph 3
        self.graph_three = pg.GraphicsWindow()
        self.graph_three.setFixedSize(self.GRAPH_SIZE)

        # Creating the Layouts
        # Main Layout
        self.main_layout = QVBoxLayout()
        # Top Layout
        self.top_layout = QHBoxLayout()
        # Top Left
        self.top_left_layout = QVBoxLayout()
        self.top_left_top_layout = QHBoxLayout()
        self.top_left_mid_layout = QHBoxLayout()
        self.top_left_bot_layout = QHBoxLayout()
        # Top Mid
        self.top_mid_layout = QVBoxLayout()
        self.top_mid_top_layout = QHBoxLayout()
        self.top_mid_mid_layout = QHBoxLayout()
        self.top_mid_bot_layout = QHBoxLayout()
        # Top Right
        self.top_right_layout = QVBoxLayout()
        self.top_right_top_layout = QHBoxLayout()
        self.top_right_mid_layout = QHBoxLayout()
        self.top_right_bot_layout = QHBoxLayout()
        # Mid Layout
        self.mid_layout = QHBoxLayout()
        # Bot Layout
        self.bot_layout = QHBoxLayout()
        # Layouts configuration
        # Adding the Top-Left layout widgets
        self.top_left_top_layout.addWidget(self.start_button)
        self.top_left_top_layout.addWidget(self.quit_button)
        self.top_left_mid_layout.addWidget(self.access_point_button)
        self.top_left_mid_layout.addWidget(self.serial_connect_button)
        self.top_left_bot_layout.addWidget(self.thresh_button)
        self.top_left_bot_layout.addWidget(self.select_ip_button)
        # Adding the Top--Mid layout widgets
        self.top_mid_top_layout.addWidget(self.text_combo_box_one)
        self.top_mid_top_layout.addWidget(self.combo_box_one)
        self.top_mid_top_layout.addWidget(self.text_combo_box_two)
        self.top_mid_top_layout.addWidget(self.combo_box_two)
        self.top_mid_mid_layout.addWidget(self.text_combo_box_three)
        self.top_mid_mid_layout.addWidget(self.combo_box_three)
        self.top_mid_mid_layout.addWidget(self.text_combo_box_four)
        self.top_mid_mid_layout.addWidget(self.combo_box_four)
        self.top_mid_bot_layout.addWidget(self.camera_ip_label)
        self.top_mid_bot_layout.addWidget(self.camera_ip_textbox)
        # Adding the Top-Right-Left layout widgets
        self.top_right_top_layout.addWidget(self.text_r_low_label)
        self.top_right_top_layout.addWidget(self.slider_r_low)
        self.top_right_top_layout.addWidget(self.text_r_low_value_label)
        self.top_right_top_layout.addWidget(self.text_r_high_label)
        self.top_right_top_layout.addWidget(self.slider_r_high)
        self.top_right_top_layout.addWidget(self.text_r_high_value_label)
        # Adding the Right-Left-Bot layout widgets
        self.top_right_mid_layout.addWidget(self.text_g_low_label)
        self.top_right_mid_layout.addWidget(self.slider_g_low)
        self.top_right_mid_layout.addWidget(self.text_g_low_value_label)
        self.top_right_mid_layout.addWidget(self.text_g_high_label)
        self.top_right_mid_layout.addWidget(self.slider_g_high)
        self.top_right_mid_layout.addWidget(self.text_g_high_value_label)
        # Adding the Right-Right-Mid layout widgets
        self.top_right_bot_layout.addWidget(self.text_b_low_label)
        self.top_right_bot_layout.addWidget(self.slider_b_low)
        self.top_right_bot_layout.addWidget(self.text_b_low_value_label)
        self.top_right_bot_layout.addWidget(self.text_b_high_label)
        self.top_right_bot_layout.addWidget(self.slider_b_high)
        self.top_right_bot_layout.addWidget(self.text_b_high_value_label)
        # Adding the Mid layout widgets
        self.mid_layout.addWidget(self.image_label_one)
        self.mid_layout.addWidget(self.image_label_two)
        self.mid_layout.addWidget(self.image_label_three)
        # Adding the Bot layout widgets
        self.bot_layout.addWidget(self.graph_one)
        self.bot_layout.addWidget(self.graph_two)
        self.bot_layout.addWidget(self.graph_three)
        # Linking the Top layouts
        self.top_left_layout.addLayout(self.top_left_top_layout)
        self.top_left_layout.addLayout(self.top_left_mid_layout)
        self.top_left_layout.addLayout(self.top_left_bot_layout)
        self.top_mid_layout.addLayout(self.top_mid_top_layout)
        self.top_mid_layout.addLayout(self.top_mid_mid_layout)
        self.top_mid_layout.addLayout(self.top_mid_bot_layout)
        self.top_right_layout.addLayout(self.top_right_top_layout)
        self.top_right_layout.addLayout(self.top_right_mid_layout)
        self.top_right_layout.addLayout(self.top_right_bot_layout)
        self.top_layout.addLayout(self.top_left_layout)
        self.top_layout.addLayout(self.top_mid_layout)
        self.top_layout.addLayout(self.top_right_layout)
        # Linking the Layouts with the main Layout
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.mid_layout)
        self.main_layout.addLayout(self.bot_layout)

# Computer Vision driven Ball and Plate Project

## Introduction
This repository was created to store all the source code for my Electronic Engineering Graduation Project.

### Here you will find:
<ol>
<li>An Arduino Source Code</li>
<ol>
<li>Code written on the Arduino Syntax (Very simmilar to C++ Programming Language)</li>
<li>The implementation of a PID controller (Proportinal Integrative and Derivative controller) to manage the motors of the construction</li>
<li>The implementation of a Accelerometer/Gyroscope reader to send live data of the X,Y axis Angle</li>
<li>The implementation of a Custom Data communication system to send/receive Live data from a Python software</li>
</ol>
<li>A Python Source Code</li>
<ol>
<li>Python Code implementing a Software to Controll all the Robot Hardware, Process all the acquired Data and display all important informations on a User Interface</li>
<li>The implementation of a Custom User interface Build with PyQt5 to display the WebCam live Feed, the Accelerometer/Gyro live data, and the Current position of a Tracked ball</li>
<li>The implementation of Computer Vision algorithm to Track a ball on a plate</li>
<li>The implementation of Kalman Filter to predict the next position of the tracked ball</li>
<li>The implementation of Worker Threads (With the QThreads module) To process and execute actions in paralell</li>
<li>The implementation of a custom Communication protocol with the Arduino side</li>
</ol>
</ol>

## Technologies
<ul>
<li>PyQt5</li>
<li>QThread</li>
<li>pyqtSignal</li>
<li>pyqtSlot</li>
<li>pyqtgraph</li>
<li>OpenCV</li>
<li>Imutils</li>
</ul>

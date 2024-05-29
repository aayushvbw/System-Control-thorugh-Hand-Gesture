# This is a software by which we can control basic necessary functions of a PC by using some hand gestures which will be tracked by the camera.

# Functions it is capable to perform are :
  1. Mouse functions (left click , right click , scroll up , scroll down , controlling cursor)
  2. Control the volume
  3. Traversing over the taskbar (alt + esc)

<h2>You can add new gestures or functionalities or even edit the present functions based on your preference and ease.<h2>

This project is only for learning concepts of openCV, Mediapipe and some more libraries. 

The mouse works by detecting the hand landmarks and finger tips . The detection is done with the help of Google’s MediaPipe library. MediaPipe is a ML solution library , it provides the user with object detection , image detection , gesture detection and facial detection facilities. We also use OpenCV(CV2) for real time image processing and visualizing hand landmarks. Lastly we use the Pyautogui , a python automation library to map functionalities to every gesture.

# Requirementa
These are the basic requirements which must be fulfilled in order to use the software features.  
  1. Webcam or inbuilt camera  
  2. Well-lit room

# Libraries and frameworks used for development of project
  1. Python 3.8 (above versions of Python does not support some required libraries)
  2. OpenCV - It is a great tool for image processing and performing computer vision tasks.It is an open source library that can be used to perform tasks like Landmark detection, objection tracking and much more.
  3. AutoPY - It is a cross-platform, simple GUI automation toolkit for Python. It includes functions for controlling the mouse and keyboard, finding colors and bitmaps on screen.
  4. Pyautogui - It allows python to control the mouse and keyboard and other GUI automation tasks.
  5. Pycaw - Python Core Audio Windows Library. It allows python to control the volume of windows based devices.
  6. MediaPipe - It is an open source framework for building pipelines. The mediapipe gesture  recognizer task lets you recognize hand gestures in real time, and provides the recognized hand gesture results along      with the landmarks of the detected hands.



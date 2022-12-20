# Interactive-Halloween-Pumpkins
#This code was written in python and was used on a raspberry Pi 4.
#This code does different actions based on the facial expression the user shows.
There are 2 different pumpkins labeld thread.py and pumpkin1.py.
The thread.py components consist of a usb camera, 2- 8x8 LED Matrix panels, 2 - 16 LED rings, and 2 HS-422 servos.
The pumpkin1.py components consist of a auxillory cord/ bluetooth speaker, 2 HS-422 servos.
The code uses TensorFlow and Deepface to read one persons facial expression at a time, and displays the facial expression that was detected while the other components proceed.
For the LED components the use of the rpi ws2182b and neopixel library was installed and used.

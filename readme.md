## hid_gamepad
### Introduction
A simple library for getting game controller and joystick inputs in Python. The module uses the low-level HID interface to communicate with the gamepad device. USB HID devices send their state through input reports that can be decoded to determine the state of the buttons and axes. State of the buttons is interpreted straightforward using bitmasks. The HID reports to gamepad state has to be translated for each device since the reports are different across controllers.

For more information how to use HID interface please read post by Stargirl Flowers from May 22, 2021:
https://blog.thea.codes/talking-to-gamepads-without-pygame/

Check also HID API documentation:
https://trezor.github.io/cython-hidapi/api.html

### Requirements
Required Python packages (as detailed in "requirements.txt"):
hid

To install the hid module on a windows computer use the command:
pip install hidapi

### generic_example.py
An example of how to use the hid_gamepad class to connect to any gamepad device and monitor its status. Data regarding the state of the device is displayed in raw form - a list of bytes. The implementation can be used to develop a mapping of any gamepad. You can figure out the bit for each axis and button this way. Then, you have to translate the HID reports to gamepad state - and the reports are different across controllers.

### asynchronous_example.py
An example of connecting to a device and monitoring its status in asynchronous mode. The current state of the gamepad is updated in parallel in a separate thread.  

### microntek_gamepad.py & microntek_example.py
An example of an implementation of a class derived from hid_gamepad, used to support Microntek gamepads. The class illustrates how to implement the mapping of the device's axes and buttons and the subsequent reading of their states. Before implementing your own class to support your chosen gamepad, please refer to the example implementation.

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


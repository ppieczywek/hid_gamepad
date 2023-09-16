import hid
import time


def list_gamepads():
    """List devices that fit in the category "joystick". Returns list of
    dictionaries with device data for each identified device."""

    device_list = []
    for device in hid.enumerate():
        if "Joystick" in device['product_string']:
            if device not in device_list:
                device_list.append(device)
    return device_list


class hid_gamepad():

    class MappingException(Exception):
        "Raised when the controller mapping is not provided"
        pass

    def __init__(self):
        self.__device_instance = None
        self.__MAX_BYTES = 128
        self._vendor_id = -1
        self._product_id = -1
        self._is_connected = False

        self._raw_inputs = []
        self._button_mapping = {}
        self._button_sate = []
        self._axis_mapping = {}
        self._axis_sate = []
        self._update_thread = None

    def __del__(self):
        self.disconnect()

    @property
    def is_connected(self):
        return self._is_connected

    @property
    def vendor_id(self):
        return self._vendor_id

    @property
    def product_id(self):
        return self._product_id

    @property
    def raw_inputs(self):
        """ Returnslist of bytes that represent the state of the controller."""
        return self._raw_inputs
    
    def connect(self, target_device):
        """Connects with device specified by "target_device" variable. The "target_device"
        is a dictionary containig "ventor_id" and "product_it" keys with assiciated values.
        List of dictionaries with available devides is provided by "list_devices" helper 
        function. The "connect" method returns True if connected with the gamepad, otherwise
        it returns False."""

        try:
            self.__device_instance = hid.device()
            self.__device_instance.open(target_device['vendor_id'], target_device['product_id'])
            self.__device_instance.set_nonblocking(True)
            if (self.__device_instance.error() == "Success"):
                self._vendor_id = target_device['vendor_id']
                self._product_id = target_device['product_id']
                self._is_connected = True
                print('Connection with the device e has been stablished')
                return True
            else:
                self._is_connected = False
                print('Unable to connect with the selected device')
                return False
        except OSError:
            self._is_connected = False
            print('Unable to connect with the selected device')
            return False

    def reconnect(self):
        """Reconnects previosly connected device."""
        try:
            self.__device_instance = hid.device()
            self.__device_instance.open(self._vendor_id, self._product_id)
            self.__device_instance.set_nonblocking(True)
            if (self.__device_instance.error() == "Success"):
                self._is_connected = True
                print('Connection with the device has been reestablished')
                return True
            else:
                self._is_connected = False
                print('Unable to reconnect with the device')
                return False
        except OSError:
            print('Unable to reconnect with the device')
            return False

    def disconnect(self):
        """Disconnects with the controller"""

        try:
            if self._is_connected is True:
                if self.__device_instance is not None:
                    self.__device_instance.close()
                    print('Device disconnected')
                    return True
            return False
        except OSError:
            print('Unable to properly disconnect the device')
            return False

    def read_raw_bits(self):
        """Function reads the controller state as raw bits and returns
        them as list of bytes that represent the state of the controller."""

        if self._is_connected is True:
            try:
                return self.__device_instance.read(self.__MAX_BYTES)
            except IOError:
                print("Device connection lost")
                self._is_connected = False
                return None

    def update_state(self):
        """Function reads the current state of the controller. Calling the
        function is necessary before reading the position of the axes and 
        buttons of the controller. Function reads the controller state
        as raw bits and saves them as list of bytes that represent the 
        state of the controller. Raw bits are storred in "raw_inputs" variable."""

        if self._is_connected is True:
            self._raw_inputs = self.read_raw_bits()
            if self._raw_inputs:
                self.process_inputs()
                return True
            else:
                return False
        else:
            return False

    def process_inputs(self):
        """This function is specific to the selected controller. It is used to 
        interpret the bit fields stored in the "raw_inputs" variable and
        read the values of the defined axes and buttons of the controller.
        
        Each controller should have its own implementation of the "process_inputs"
        function. See example below.
        """
        pass

    def get_button_state(self, button_name):
        """Returns True if the button specified by name or index has been pressed
        since the last call. Throws ValueError if the button name or index cannot
        be found."""

        try:
            if len(self._button_mapping) < 1:
                raise hid_gamepad.MappingException

            if button_name in self._button_mapping:
                button_index = self._button_mapping[button_name]
            else:
                button_index = int(button_name)

            return self._button_state[button_index]

        except KeyError:
            raise ValueError('Button %i was not found' % button_index)
        except ValueError:
            raise ValueError('Button name %s was not found' % button_name)
        except hid_gamepad.MappingException:
            print('Button mapping not provided')

    def set_button_state(self, button_name, state):
        """Returns True if the button specified by name or index has
        been successfully changed. Throws ValueError if the button 
        name or index cannot be found."""

        try:
            if len(self._button_mapping) < 1:
                raise hid_gamepad.MappingException

            if button_name in self._button_mapping:
                button_index = self._button_mapping[button_name]
                self._button_state[button_index] = state
                return True
            else:
                return False
        except KeyError:
            raise ValueError('Button %i was not found' % button_index)
        except ValueError:
            raise ValueError('Button name %s was not found' % button_name)
        except hid_gamepad.MappingException:
            print('Button mapping not provided')

    def get_axis_state(self, axis_name):
        """Returns floating point value of the axis specified by name or index.
        Throws ValueError if the button name or index cannot be found."""

        try:
            if len(self._axis_mapping) < 1:
                raise hid_gamepad.MappingException

            if axis_name in self._axis_mapping:
                axis_index = self._axis_mapping[axis_name]
            else:
                axis_index = int(axis_name)

            return self._axis_state[axis_index]
        except KeyError:
            raise ValueError('Axis %i was not found' % axis_index)
        except ValueError:
            raise ValueError('Axis name %s was not found' % axis_name)
        except hid_gamepad.MappingException:
            print('Axis mapping not provided')

    def set_axis_state(self, axis_name, state):
        """Returns True if the state of the axis specified by name or 
        index has been set. Throws ValueError if the button name or index 
        cannot be found."""

        try:
            if len(self._axis_mapping) < 1:
                raise hid_gamepad.MappingException

            if axis_name in self._axis_mapping:
                axis_index = self._axis_mapping[axis_name]
                self._axis_state[axis_index] = state
                return True
            else:
                return False
        except KeyError:
            raise ValueError('Axis %i was not found' % axis_index)
        except ValueError:
            raise ValueError('Axis name %s was not found' % axis_name)
        except hid_gamepad.MappingException:
            print('Axis mapping not provided')


    def set_axis_mapping(self, mapping):
        """Sets the names for controller axis. Mapping is provided as dictionary
        with axis names as keys and axis indexes as values"""
        if mapping:
            if len(mapping) > 0:
                self._axis_mapping = mapping
                self._axis_state = [0.0 for i in range(len(mapping))]
                return True
        return False

    def set_button_mapping(self, mapping):
        """Sets the names for controller buttons. Mapping is provided as dictionary
        with button names as keys and axis indexes as values"""
        if mapping:
            if len(mapping) > 0:
                self._button_mapping = mapping
                self._button_state = [False for i in range(len(mapping))]
                return True
        return False


class esperanza_gamepad(hid_gamepad):
    """"Class for Esperanza EG102 USB PC gamepad."""

    def __init__(self):
        super().__init__()

        # Axis and buttons mapping with indexes are prvided in class constructor

        axis_mapping = {
            'ax1_x': 0,
            'ax1_y': 1,
            'ax2_x': 2,
            'ax2_y': 3,
            'ax3_x': 4,
            'ax3_y': 5
        }
        self.set_axis_mapping(axis_mapping)

        button_mapping = {
            'l_1': 0,
            'l_2': 1,
            'r_1': 2,
            'r_2': 3,
            'b_1': 4,
            'b_2': 5,
            'b_3': 6,
            'b_4': 7,
            'l_b': 8,
            'r_b': 9,
            'select': 10,
            'start': 11,
            'analog': 12
        }
        self.set_button_mapping(button_mapping)

    def process_inputs(self):
        """This function is specific to the selected controller. It is used to 
        interpret the bit fields stored in the "raw_inputs" variable and
        read the values of the defined axes and buttons of the controller.
            
        Each controller should have its own implementation of the "process_inputs"
        function.
        """
        raw_inputs = self.raw_inputs
        # getting the state of individual axes
        self.set_axis_state('ax1_x', (raw_inputs[1] - 128) / 128)
        self.set_axis_state('ax1_y', (raw_inputs[2] - 128) / 128)
        self.set_axis_state('ax2_x', (raw_inputs[3] - 128) / 128)
        self.set_axis_state('ax2_y', (raw_inputs[4] - 128) / 128)

        if (raw_inputs[5] & 0b00001111) == 0b00001111:
            self.set_axis_state('ax3_x', 0.0)
            self.set_axis_state('ax3_y', 0.0)
        elif (raw_inputs[5] & 0b00000110) == 0b00000110:
            self.set_axis_state('ax3_x', -1.0)
        elif (raw_inputs[5] & 0b00000010) == 0b00000010:
            self.set_axis_state('ax3_x', 1.0)
        elif (raw_inputs[5] & 0b00000000) == 0b00000000:
            self.set_axis_state('ax3_y', -1.0)
        elif (raw_inputs[5] & 0b00000100) == 0b00000100:
            self.set_axis_state('ax3_y', 1.0)
        else:
            pass

        # using the bitmasks to get the state of individual buttons
        self.set_button_state('b_1', (raw_inputs[5] & 0b00010000) == 0b00010000)
        self.set_button_state('b_2', (raw_inputs[5] & 0b00100000) == 0b00100000)
        self.set_button_state('b_3', (raw_inputs[5] & 0b01000000) == 0b01000000)
        self.set_button_state('b_4', (raw_inputs[5] & 0b10000000) == 0b10000000)

        self.set_button_state('l_1', (raw_inputs[6] & 0b00000001) == 0b00000001)
        self.set_button_state('l_2', (raw_inputs[6] & 0b00000100) == 0b00000100)
        self.set_button_state('r_1', (raw_inputs[6] & 0b00000010) == 0b00000010)
        self.set_button_state('r_2', (raw_inputs[6] & 0b00001000) == 0b00001000)

        self.set_button_state('select', (raw_inputs[6] & 0b00010000) == 0b00010000)
        self.set_button_state('start', (raw_inputs[6] & 0b00100000) == 0b00100000)
        self.set_button_state('l_b', (raw_inputs[6] & 0b01000000) == 0b01000000)
        self.set_button_state('r_b', (raw_inputs[6] & 0b10000000) == 0b10000000)



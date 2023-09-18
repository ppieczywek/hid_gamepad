import hid
import time
import threading


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

    class update_thread(threading.Thread):
        """Thread used to continually run the updateState function on a Gamepad
        in the background. One of these is created by the Gamepad start_asynchronous 
        function and closed by stop_asynchronous"""

        def __init__(self, gamepad):
            threading.Thread.__init__(self)
            if isinstance(gamepad, hid_gamepad):
                self.gamepad = gamepad
            else:
                raise ValueError('Gamepad update thread was not created with a valid Gamepad object')
            self.running = True
            print("thread created")

        def run(self):
            try:
                while self.running:
                    time.sleep(100/1000)
                    self.gamepad.update_state()
                self.gamepad = None
            except:
                self.running = False
                self.gamepad = None
                raise


    def __init__(self):
        self.__device_instance = None
        self.__MAX_BYTES = 128
        self._device_info = {}
        self._is_connected = False

        self._raw_inputs = []
        self._button_mapping = {}
        self._button_sate = []
        self._axis_mapping = {}
        self._axis_sate = []
        self._update_thread = None
        self._lock = threading.Lock()

    def __del__(self):
        self.disconnect()


    @property
    def is_connected(self):
        return self._is_connected
    

    def get_available_info(self):
        """Returns all types device informations."""

        if self._is_connected:
            if self._device_info:
                return self._device_info.keys()
            else:
                print('Device info not avialable')
                return None
        else:
            print('Device info not avialable - gamepad is not connected')
            return None
        

    def get_device_info(self, field):
        """"Returns value for specified type of device information. Type of
        device information is provided by 'field' varaible"""

        try:
            if self._is_connected:
                if self._device_info:
                    return self._device_info[field]
                else:
                    print('Device info not avialable')
                    return None
            else:
                print('Device info not avialable - gamepad is not connected')
                return None
        except KeyError:
            raise ValueError(f'Property {field} was not found')
    

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
                self._device_info = target_device
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
                    self.__device_instance = None
                    self.__MAX_BYTES = 128
                    self._device_info = {}
                    self._is_connected = False

                    self._raw_inputs = []
                    self._button_mapping = {}
                    self._button_sate = []
                    self._axis_mapping = {}
                    self._axis_sate = []
                    self.stop_asynchronous()
                    self._update_thread = None
                    
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
            self._lock.acquire()
            self._raw_inputs = self.read_raw_bits()
            if self._raw_inputs:
                self._lock.release()
                self.process_inputs()
                return True
            else:
                self._lock.release()
                return False
        else:
            self._lock.release()
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


    def start_asynchronous(self):
            """Starts a background thread which keeps the gamepad state updated automatically.
            This allows for asynchronous gamepad updates and event callback code."""

            if self._is_connected is True:
                if self._update_thread is not None:
                    if self._update_thread.running:
                        raise RuntimeError('Called startBackgroundUpdates when the update thread is already running')
                self._update_thread = hid_gamepad.update_thread(self)
                self._update_thread.start()


    def stop_asynchronous(self):
            """Stops the background thread which keeps the gamepad state updated automatically.
            This may be called even if the background thread was never started.

            The thread will stop on the next event after this call was made."""
            if self._update_thread is not None:
                self._update_thread.running = False

    def get_axis_names(self):
        if self._is_connected:
            if self._axis_mapping:
                return self._axis_mapping.keys()
            else:
                print('Axis mapping not provided.')
                return None
        else:
            print('Axis mapping not avialable - gamepad is not connected')
            return None


    def get_button_names(self):
        if self._is_connected:
            if self._button_mapping:
                return self._button_mapping.keys()
            else:
                print('Button mapping not provided.')
                return None
        else:
            print('Button mapping not avialable - gamepad is not connected')
            return None
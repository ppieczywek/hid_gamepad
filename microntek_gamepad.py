from hid_gamepad import hid_gamepad

class microntek_gamepad(hid_gamepad):
    """"Class for Microntek EG102 USB PC gamepad."""

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

    def connect(self, target_device):
        try:
            if str(target_device['manufacturer_string']).strip().lower() == "microntek":
                return super().connect(target_device)
            else:
                print("Device is not a Microntek gamepad.")
                return False

        except KeyError:
            raise ValueError(f"Property 'manufacturer_string' was not found")
            return False
        

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



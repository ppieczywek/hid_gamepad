from microntek_gamepad import microntek_gamepad 
from hid_gamepad import list_gamepads
import time

if __name__ == "__main__":

    available_gamepads = list_gamepads()

    if available_gamepads:
        print("\nSelect available gamepad:")
        for index, gamepad in enumerate(available_gamepads):
            print(f"\t{index} - manufacturer: {str(gamepad['manufacturer_string']).strip()}, " +
                  f"product: {str(gamepad['product_string']).strip()}, " +
                  f"vendor id: {str(gamepad['vendor_id']).strip()}, " +
                  f"product id:  {str(gamepad['product_id']).strip()}")

        selected_gamepad = int(input("\nSelect one of available gamepads to connect:"))
        my_gamepad = microntek_gamepad() 
        if my_gamepad.connect(available_gamepads[selected_gamepad]):
            print("\nConnection established with selected gampad.")
            print("Reporting gampad raw input states.")
            while True:
                if my_gamepad.update_state():
                    time.sleep(100/1000)
                    ax1_x = my_gamepad.get_axis_state("ax1_x")
                    ax1_y = my_gamepad.get_axis_state("ax1_y")
                    ax2_x = my_gamepad.get_axis_state("ax2_x")
                    ax2_y = my_gamepad.get_axis_state("ax2_y")
                    b_1 = my_gamepad.get_button_state("b_1")
                    b_2 = my_gamepad.get_button_state("b_2")
                    b_3 = my_gamepad.get_button_state("b_3")
                    b_4 = my_gamepad.get_button_state("b_4")
                    print(f"x1 axis: {ax1_x}, y1 axis: {ax1_y}, x2 axis: {ax2_x}, y2 axis: {ax2_y}, button 1: {b_1}, button 2: {b_2}, button 3: {b_3}, button 4: {b_4}")
                    
                else:
                    if my_gamepad.is_connected is False:
                        my_gamepad.reconnect()
                        time.sleep(2000/1000)
    else:
        print("\nUnable to find gamped devices.")

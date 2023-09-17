from hid_gamepad import hid_gamepad
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
        my_gamepad = hid_gamepad() 
        if my_gamepad.connect(available_gamepads[selected_gamepad]):
            print("\nConnection established with selected gampad.")
            print("Reporting gampad raw input states.")
            my_gamepad.start_asynchronous()
            while True:
                if my_gamepad.is_connected:
                    # time.sleep(100/1000)
                    print(my_gamepad.raw_inputs)
                else:
                    my_gamepad.reconnect()
                    time.sleep(2000/1000)
    else:
        print("\nUnable to find gamped devices.")
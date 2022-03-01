# Adapted from Sandy J Macdonald's gist at https://gist.github.com/sandyjmacdonald/b465377dc11a8c83a8c40d1c9b990a90 to configure all buttons and switch off all lights in loop
# Adapted from Colin Deady's solution on Pimoroni Forum - https://forums.pimoroni.com/t/pico-rgb-keypad-base-as-a-usb-hid-device-solved/16224/7

"""
Purpose: Read in a YAML configuration file, which lists:
- The Key
- The Key On colour and brightness
- The Key Off colour and brightness
- The 'command' to run: its just a text string to send


Maybe also add some pulsing effects too
"""

import time
import board
import busio
import usb_hid

from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_dotstar

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

from digitalio import DigitalInOut, Direction, Pull
import qd_yaml

cs = DigitalInOut(board.GP17)
cs.direction = Direction.OUTPUT
cs.value = 0
num_pixels = 16
pixels = adafruit_dotstar.DotStar(board.GP18, board.GP19, num_pixels, brightness=0.1, auto_write=True)
i2c = busio.I2C(board.GP5, board.GP4)
device = I2CDevice(i2c, 0x20)
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

CONFIG_FILE = 'keypad.yml'

def load_configuration():
    """ Read in the YAML configuration file, and returns the config as a list """
    yml = qd_yaml.YAML()
    with open(CONFIG_FILE) as file:
        config = yml.load(file)

    return config
        

def colourwheel(pos):
    "Change the colour based on the current RGB value"
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def read_button_states(x, y):
    "Read the button state"
    
    # set all 16 buttons to state 0
    pressed = [0] * 16
    with device:
        device.write(bytes([0x0]))
        result = bytearray(2)
        device.readinto(result)
        b = result[0] | result[1] << 8
        for i in range(x, y):
            if not (1 << i) & b:
                pressed[i] = 1
            else:
                pressed[i] = 0
    return pressed

def convert_hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


# held is set of the button is held down, for debouncing
held = [0] * 16

def set_keycolours(config):
#     print(f'config is: {config}')

    for key in config:
        key = dict(sum(map(list, map(dict.items, key)), []))
        print(f"new key {key}")
#         for item in key:
        print (f"key name: {key['name']}")
        print(f'convert_hex_to_rgb(key["off"]) {convert_hex_to_rgb(key["off"])}')
        pixels[int(key["name"])] = convert_hex_to_rgb(key["off"])

def key_on(config, key):
    pixels[int(key["name"])] = convert_hex_to_rgb(key["on"])


    # load the config and set the key colours
config = load_configuration()

set_keycolours(config=config)
while True:
    # check the button press state
    pressed = read_button_states(0, 16)
    
    for key in config:
        key = dict(sum(map(list, map(dict.items, key)), []))
        key_no = int(key['name'])
        if pressed[key_no]:
            print(f"key pressed {key_no}")
            pixels[int(key["name"])] = convert_hex_to_rgb(key["on"])
            
            # send the command
            layout.write(key["command"])
            kbd.send(Keycode.ENTER)
        else:
            pixels[int(key["name"])] = convert_hex_to_rgb(key["off"])
        if not held[key_no]:
            held[key_no] = 1
        
    else:  # Released state
        for i in range(16):
            held[i] = 0  # Set held states to off
        time.sleep(0.1) # Debounce
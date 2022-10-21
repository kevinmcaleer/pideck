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
from key import Key, convert_hex_to_rgb, convert_rgb_to_hex

VERSION = 1.1

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


# held is set of the button is held down, for debouncing
held = [0] * 16

def set_keycolours(config):
#     """ Set the colours based on the yaml file configuration """

    for key in config:
        key = dict(sum(map(list, map(dict.items, key)), []))
        pixels[int(key["name"])] = convert_hex_to_rgb(key["off"])

def key_on(config, key):
    pixels[int(key["name"])] = convert_hex_to_rgb(key["on"])
    
# load the config and set the key colours
config = load_configuration()

set_keycolours(config=config)

keys = []
item_len = len(config)
# print(f"item_len {item_len}")
for index in range(item_len):
#     print(f"index: {index}")
    key = dict(sum(map(list, map(dict.items, config[index])), []))
    key_no = int(key['name'])
    myKey = Key()
    myKey.command = key['command']
    myKey.name = key['name']
    myKey.on = key['on']
    myKey.off = key['off']
    myKey.effect = key['effect']
    myKey.pulse_timing = key.get('pulse_timing')
    myKey.button_type = key['button_type']
    myKey.repeatable = key.get('repeatable', 'false')
    keys.insert(index, myKey)
# print(f"keys: {keys}")

print(f"PiDeck Version {VERSION}")

while True:
    # check the button press state
    pressed = read_button_states(0, 16)
    
    for key_no in range(16):

        do_effect = True
        if keys[key_no].button_type == "toggle":
            do_effect = keys[key_no].toggle_value
        
        if pressed[key_no] and not held[key_no]:
            # print(f"keys[{key_no}]: {keys[key_no].name} {keys[key_no].button_type} keys[key_no].repeatable {keys[key_no].repeatable}")

            if keys[key_no].button_type == "toggle":
                if keys[key_no].toggle:
                    pixels[key_no] = convert_hex_to_rgb(keys[key_no].off)
                    do_effect = False
                else:
                    pixels[key_no] = convert_hex_to_rgb(keys[key_no].on)
            else:
                pixels[key_no] = convert_hex_to_rgb(keys[key_no].on)
            
            # send the command
            keys[key_no].send(kbd)
            # print(f"key sent {keys[key_no].command}")

            held[key_no] = True
        else:
            if keys[key_no].effect == "none":
                if keys[key_no].button_type == "press":
                    pixels[key_no] = convert_hex_to_rgb(keys[key_no].off)

        # Pulse effect if switched on
        if keys[key_no].effect == "pulse" and do_effect and not pressed[key_no]:
            color = keys[key_no].pulse_tick()
            pixels[key_no] = convert_hex_to_rgb(color)
            
        # Flash effect if switched on
        if keys[key_no].effect == "flash" and do_effect and not pressed[key_no]:
            color = keys[key_no].flash_tick()
            pixels[key_no] = convert_hex_to_rgb(color)
         
    # Released state
    time.sleep(0.15) # Debounce
    # check the button press states again
    pressed = read_button_states(0, 16)
    for key_no in range(16): 
        if not pressed[key_no] or keys[key_no].repeatable:
            held[key_no] = False  # Set held states to off

# Welcome to PiDeck
Turn your Pimoroni Pico RBG Keypad into a USB Shortcut Keypad that is configurable via a simple Yaml file.

# Installation & Prerequisites
To get up and running quickly, 
1. Flash your Pico with the latest version of [Circuit Python](https://circuitpython.org/board/raspberry_pi_pico/), from Adafruit
1. Clone this repository and copy all the files on to the pico
2. Edit the `keypad.yml` file to setup your own keyboard shortcuts
3. Restart the Pico and away you go.

# keypad.yml
You can configure the PiDeck using the `keypad.yml` file. It has 16 sections, one for each key.
Each key as a `name` 0 to 15 (why not 1 to 16? - it's a programming thing!)
Then it has an `on` and `off` HEX RGB value (without any leading `#` character). The off value will be shown when the key isn't press, the on value when the key is pressed. 
If the `effect` is set to `pulse` the key will pulse between the off and on values.
The `command` is the sequence of keys (or shortcut) that will be sent to the computer. On a Mac, you can use the Automator to specify a `service` and then Application to launch, then in the Keyboard panel with Settings you can specify the shortcut key combination to launch that app. Pair that with the key combination in the `command` and you have yourself a productivity Swiss Army knife.
Finally `button_type` lets you choose whether the key is a single `press` momentry touch button, or if it is a `toggle` button where it stays on until you press it again.

``` yaml
- name: 0
   off: FFFFFF
   on: B4F8C8
   effect: none
   command: COMMAND S
   button_type: press
- name: 1
   off: FFFF00
   on: 00FF00
   effect: pulse
   command: COMMAND TAB
   button_type: toggle
```

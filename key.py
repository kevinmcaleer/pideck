from adafruit_hid.keycode import Keycode
from time import sleep

def convert_hex_to_rgb(value):
    """ Converts a hex value to RGB values """
    value = value.lstrip('#')
    lv = len(value)
#     print(f"value: {value}, length: {lv}")
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def convert_rgb_to_hex(r:int,g:int,b:int):
#     return "{:02x}{:02x}{:02x}".format(r,g,b)


    hex = "{:02x}{:02x}{:02x}".format(r,g,b).upper()
    return hex

#     print(f"r:{r}, g:{g}, b:{b}")
#     data_str = bytearray([int(r),int(g),int(b)])
#     hex_str = ''.join([chr(b) for b in data_str])
#     print(f"# {hex_str}")
#     return hex_str
    

class Key():
    _off = ""
    _on = ""
    _effect = "" # pulse 
    _command = ""
    _button_type = "" # press, toggle
    _pulse_count = 10
    _pulse_up = False
    _toggle = False
    
    def __init__(self):
        self._type = "press"
    
    @property
    def command(self):
        return self._command
    
    @command.setter
    def command(self, value):
        self._command = value
        
    @property
    def on(self):
        return self._on
    
    @on.setter
    def on(self, value):
        self._on = value
        
    @property
    def off(self):
        return self._off
    
    @off.setter
    def off(self, value):
        self._off = value
        
    @property
    def effect(self):
        return self._effect
    
    @effect.setter
    def effect(self, value):
        self._effect = value

    @property
    def button_type(self):
        return self._button_type
    
    @button_type.setter
    def button_type(self, value):
        if value in ["press","toggle"]:
            self._button_type = value
        else:
            print("not a valid button_type")
    
    @property
    def toggle(self):
        return self._toggle
    
    @toggle.setter
    def toggle(self, value):
        if self._toggle:
            self._toggle = False
        else:
            self._toggle = True
    
    def fade_colour(self, percent):
        '''assumes color is rgb between (0, 0, 0) and (255, 255, 255)'''

#         print (f"on: {self._on}, off: {self.off}, percent: {percent}")
        color_from_r, color_from_g, color_from_b = convert_hex_to_rgb(self._off)
        color_to_r, color_to_g, color_to_b = convert_hex_to_rgb(self._on)
        
        r_vector = color_from_r - color_to_r
        g_vector = color_from_g - color_to_g
        b_vector = color_from_b - color_to_b
        
        r = int(color_to_r + r_vector * percent)
        g = int(color_to_g + g_vector * percent)
        b = int(color_to_b + b_vector * percent)
        
        # return the colours
        return convert_rgb_to_hex(r,g,b)
    
    
    def pulse_tick(self):
        if self._pulse_up:
            if self._pulse_count < 10:
                self._pulse_count += 1
            else:
                self._pulse_up = False
        else:
            if self._pulse_count > 0:
                self._pulse_count -= 1
            else:
                self._pulse_up = True
#         print(f"pulse_count: {self._pulse_count}")
        return self.fade_colour(self._pulse_count/10)
        
    def send(self, keyb):
        # split the string into separate strings
        self._command.replace("+","")
        keys = self._command.split()

        for command in keys:
#             print(f"command: {command}, length: {len(keys)}")
            if command in ["CTRL", "CONTROL"]:
#                 print("press control")
                keyb.press(Keycode.CONTROL)
            elif command in ["SHIFT"]:
#                 print("press shift")
                keyb.press(Keycode.SHIFT)
            elif command in ["OPTION", "ALT"]:
#                 print("press option")
                keyb.press(Keycode.OPTION)
            elif command in ["COMMAND"]:
#                 print("press command")
                keyb.press(Keycode.COMMAND)
            elif command in ["a","A"]:
                keyb.press(Keycode.A)
            elif command in ["b","B"]:
                keyb.press(Keycode.B)
            elif command in ["c","C"]:
                keyb.press(Keycode.C)
            elif command in ["d","D"]:
                keyb.press(Keycode.D)
            elif command in ["e","E"]:
                keyb.press(Keycode.E)
            elif command in ["f","F"]:
                keyb.press(Keycode.F)
            elif command in ["g","G"]:
                keyb.press(Keycode.G)
            elif command in ["h","H"]:
                keyb.press(Keycode.H)
            elif command in ["i","I"]:
                keyb.press(Keycode.I)
            elif command in ["j","J"]:
                keyb.press(Keycode.J)
            elif command in ["k","K"]:
                keyb.press(Keycode.K)
            elif command in ["l","L"]:
                keyb.press(Keycode.L)
            elif command in ["m","M"]:
                keyb.press(Keycode.M)
            elif command in ["n","N"]:
                keyb.press(Keycode.N)
            elif command in ["o","O"]:
                keyb.press(Keycode.O)
            elif command in ["p","P"]:
                keyb.press(Keycode.P)
            elif command in ["q","Q"]:
                keyb.press(Keycode.Q)
            elif command in ["r","R"]:
                keyb.press(Keycode.R)
            elif command in ["s","S"]:
                keyb.press(Keycode.S)
            elif command in ["t","T"]:
                keyb.press(Keycode.T)
            elif command in ["u","U"]:
                keyb.press(Keycode.U)
            elif command in ["v","V"]:
                keyb.press(Keycode.V)
            elif command in ["w","w"]:
                keyb.press(Keycode.W)
            elif command in ["x","X"]:
                keyb.press(Keycode.X)
            elif command in ["y","Y"]:
                keyb.press(Keycode.Y)
            elif command in ["z","Z"]:
                keyb.press(Keycode.Z)
            elif command in ["1"]:
                keyb.press(Keycode.KEYPAD_ONE)
            elif command in ["2"]:
                keyb.press(Keycode.KEYPAD_TWO)
            elif command in ["3"]:
                keyb.press(Keycode.KEYPAD_THREE)
            elif command in ["4"]:
                keyb.press(Keycode.KEYPAD_FOUR)
            elif command in ["5"]:
                keyb.press(Keycode.KEYPAD_FIVE)
            elif command in ["6"]:
                keyb.press(Keycode.KEYPAD_SIX)
            elif command in ["7"]:
                keyb.press(Keycode.KEYPAD_SEVEN)
            elif command in ["8"]:
                keyb.press(Keycode.KEYPAD_EIGHT)
            elif command in ["9"]:
                keyb.press(Keycode.KEYPAD_NINE)
            elif command in ["0"]:
                keyb.press(Keycode.KEYPAD_ZERO)
            elif command in ["[","{"]:
                keyb.press(Keycode.LEFT_BRACKET)
            elif command in ["]","}"]:
                keyb.press(Keycode.RIGHT_BRACKET)
            elif command in ["TAB"]:
                keyb.press(Keycode.TAB)
#                     
#         sleep(0.10)
        keyb.release_all()
#             keyb.send(Keycode.ENTER)

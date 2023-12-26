from adafruit_hid.keycode import Keycode
from time import sleep

pulse_timing = 10 # Default timing.

def convert_hex_to_rgb(value):
    """ Converts a hex value to RGB values """
    
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def convert_rgb_to_hex(r:int,g:int,b:int):
    """ Converts RGB values into a Hex string """
    
    hex = "{:02x}{:02x}{:02x}".format(r,g,b).upper()
    return hex    

class Key():
    """ Models a single Key on the keypad """
    _off = ""
    _on = ""
    _effect = "" # pulse 
    _command = ""
    _button_type = "" # press, toggle
    _pulse_count = pulse_timing  # initialize to the pulse timing
    _pulse_timing = pulse_timing
    _pulse_up = False
    _toggle = False
    _repeatable = False
    
    def __init__(self):
        self._type = "press"
    
    @property
    def command(self):
        """ Gets the current keystrokes to be sent on keypress """
        return self._command
    
    @command.setter
    def command(self, value):
        """ Sets the current keystrokes to be sent on keypress """
        self._command = value
        
    @property
    def on(self):
        """ Gets the current colour value for the button when its pressed """
        return self._on
    
    @on.setter
    def on(self, value):
        """ Sets the current colour value for the button when its pressed """
        self._on = value
        
    @property
    def off(self):
        """ Gets the current colour value for the button when its not pressed """
        return self._off
    
    @off.setter
    def off(self, value):
        """ Sets the current colour value for the button when its not pressed """
        self._off = value
        
    @property
    def effect(self):
        """ Gets the button effect (pulse) """
        return self._effect
    
    @effect.setter
    def effect(self, value):
        """ Sets the button effect (pulse, flash, none) """
        if value in ["pulse","flash","none"]:
            self._effect = value
        else:
            print(f"{value} is not a valid effect type")

    @property
    def pulse_timing(self):
        """ Gets the button color change timing """
        return self._pulse_timing
    
    @pulse_timing.setter
    def pulse_timing(self, value):
        """ Sets the button color change timing """
        if value is not None and value.isdigit() and int(value) > 0:
            self._pulse_timing = int(value)
            self._pulse_count = self._pulse_timing

    @property
    def button_type(self):
        """ Gets the button type (toggle or press) """
        return self._button_type
    
    @button_type.setter
    def button_type(self, value:str):
        """ Sets the button type (toggle or press) """
        if value in ["press","toggle"]:
            self._button_type = value
        else:
            print("not a valid button_type")

    @property
    def repeatable(self):
        """ Gets the setting if the command can be repeated on the same press """
        return self._repeatable
    
    @repeatable.setter
    def repeatable(self, value:bool):
        """ Sets if the command can be repeated on the same press """
        if value.lower() == "true":
            self._repeatable = True
            
    @property
    def toggle(self)->bool:
        """ Gets the current toggle state (True or False) and flips the state """
        if self._toggle:
            self._toggle = False
            return True
        else:
            self._toggle = True
            return False
    
    @property
    def toggle_value(self):
        """ Gets the current toggle state """
        return self._toggle

    def fade_colour(self, percent:float):
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
        """ cycles the pulse animation through one step """
        if self._pulse_up:
            if self._pulse_count < self._pulse_timing:
                self._pulse_count += 1
            else:
                self._pulse_up = False
        else:
            if self._pulse_count > 0:
                self._pulse_count -= 1
            else:
                self._pulse_up = True
#         print(f"pulse_count: {self._pulse_count}")
        return self.fade_colour(self._pulse_count/self._pulse_timing)
    
    def flash_tick(self):
        if self._pulse_count < self._pulse_timing:
            self._pulse_count += 1
           
        else:
            self._pulse_count = 0
            if self._pulse_up:
                self._pulse_up = False
            else:
                self._pulse_up = True
        
        if self._pulse_up:
            return self._on
        else:
            return self._off
        
    def send(self, keyb):
        """ Sends the current command to the attached computer """
        # split the string into separate strings
        keys = self._command.upper().replace("+"," ").split()

        for command in keys:
            if command in ["CTRL", "CONTROL"]:
                keyb.press(Keycode.CONTROL)
            elif command == "SHIFT":
                keyb.press(Keycode.SHIFT)
            elif command in ["OPT", "OPTION", "ALT"]:
                keyb.press(Keycode.OPTION)
            elif command in ["CMD", "COMMAND"]:
                keyb.press(Keycode.COMMAND)
            elif command == "PRINT_SCREEN":
                keyb.press(Keycode.PRINT_SCREEN)
                keyb.release_all()
            elif command == "A":
                keyb.press(Keycode.A)
                keyb.release_all()
            elif command == "B":
                keyb.press(Keycode.B)
                keyb.release_all()
            elif command == "C":
                keyb.press(Keycode.C)
                keyb.release_all()
            elif command == "D":
                keyb.press(Keycode.D)
                keyb.release_all()
            elif command == "E":
                keyb.press(Keycode.E)
                keyb.release_all()
            elif command == "F":
                keyb.press(Keycode.F)
                keyb.release_all()
            elif command == "G":
                keyb.press(Keycode.G)
                keyb.release_all()
            elif command == "H":
                keyb.press(Keycode.H)
                keyb.release_all()
            elif command == "I":
                keyb.press(Keycode.I)
                keyb.release_all()
            elif command == "J":
                keyb.press(Keycode.J)
                keyb.release_all()
            elif command == "K":
                keyb.press(Keycode.K)
                keyb.release_all()
            elif command == "L":
                keyb.press(Keycode.L)
                keyb.release_all()
            elif command == "M":
                keyb.press(Keycode.M)
                keyb.release_all()
            elif command == "N":
                keyb.press(Keycode.N)
                keyb.release_all()
            elif command == "O":
                keyb.press(Keycode.O)
                keyb.release_all()
            elif command == "P":
                keyb.press(Keycode.P)
                keyb.release_all()
            elif command == "Q":
                keyb.press(Keycode.Q)
                keyb.release_all()
            elif command == "R":
                keyb.press(Keycode.R)
                keyb.release_all()
            elif command == "S":
                keyb.press(Keycode.S)
                keyb.release_all()
            elif command == "T":
                keyb.press(Keycode.T)
                keyb.release_all()
            elif command == "U":
                keyb.press(Keycode.U)
                keyb.release_all()
            elif command == "V":
                keyb.press(Keycode.V)
                keyb.release_all()
            elif command == "W":
                keyb.press(Keycode.W)
                keyb.release_all()
            elif command == "X":
                keyb.press(Keycode.X)
                keyb.release_all()
            elif command == "Y":
                keyb.press(Keycode.Y)
                keyb.release_all()
            elif command == "Z":
                keyb.press(Keycode.Z)
                keyb.release_all()
            elif command == "1":
                keyb.press(Keycode.ONE)
                keyb.release_all()
            elif command == "2":
                keyb.press(Keycode.TWO)
                keyb.release_all()
            elif command == "3":
                keyb.press(Keycode.THREE)
                keyb.release_all()
            elif command == "4":
                keyb.press(Keycode.FOUR)
                keyb.release_all()
            elif command == "5":
                keyb.press(Keycode.FIVE)
                keyb.release_all()
            elif command == "6":
                keyb.press(Keycode.SIX)
                keyb.release_all()
            elif command == "7":
                keyb.press(Keycode.SEVEN)
                keyb.release_all()
            elif command == "8":
                keyb.press(Keycode.EIGHT)
                keyb.release_all()
            elif command == "9":
                keyb.press(Keycode.NINE)
                keyb.release_all()
            elif command == "0":
                keyb.press(Keycode.ZERO)
                keyb.release_all()
            elif command in ["[","{"]:
                keyb.press(Keycode.LEFT_BRACKET)
                keyb.release_all()
            elif command in ["]","}"]:
                keyb.press(Keycode.RIGHT_BRACKET)
                keyb.release_all()
            elif command == "TAB":
                keyb.press(Keycode.TAB)
                keyb.release_all()
            elif command == "MINUS":
                keyb.press(Keycode.KEYPAD_MINUS)
                keyb.release_all()
            elif command == "PLUS":
                keyb.press(Keycode.KEYPAD_PLUS)
                keyb.release_all()
            elif command == "EQUALS":
                keyb.press(Keycode.EQUALS)
                keyb.release_all()
            elif command in ["ESC", "ECSCAPE"]:
                keyb.press(Keycode.ESCAPE)
                keyb.release_all()
            elif command == "SPACE":
                keyb.press(Keycode.SPACE)
                keyb.release_all()
            elif command in [".", "PERIOD"]:
                keyb.press(Keycode.PERIOD)
                keyb.release_all()
            elif command in [",", "COMMA"]:
                keyb.press(Keycode.COMMA)
                keyb.release_all()
            elif command in [";", "SEMICOLON"]:
                keyb.press(Keycode.SEMICOLON)
                keyb.release_all()
            elif command == "COLON":
                keyb.press(Keycode.SHIFT)
                keyb.press(Keycode.SEMICOLON)
                keyb.release_all()
            elif command in ["\\", "BACKSLASH"]:
                keyb.press(Keycode.BACKSLASH)
                keyb.release_all()
            elif command in ["/", "FORWARD_SLASH"]:
                keyb.press(Keycode.FORWARD_SLASH)
                keyb.release_all()
            elif command in ["LEFT", "LEFT_ARROW"]:
                keyb.press(Keycode.LEFT_ARROW)
                keyb.release_all()
            elif command in ["RIGHT", "RIGHT_ARROW"]:
                keyb.press(Keycode.RIGHT_ARROW)
                keyb.release_all()
            elif command in ["UP", "UP_ARROW"]:
                keyb.press(Keycode.UP_ARROW)
                keyb.release_all()
            elif command in ["DOWN", "DOWN_ARROW"]:
                keyb.press(Keycode.DOWN_ARROW)
                keyb.release_all()
            elif command == "F1":
                keyb.press(Keycode.F1)
                keyb.release_all()
            elif command == "F2":
                keyb.press(Keycode.F2)
                keyb.release_all()
            elif command == "F3":
                keyb.press(Keycode.F3)
                keyb.release_all()
            elif command == "F4":
                keyb.press(Keycode.F4)
                keyb.release_all()
            elif command == "F5":
                keyb.press(Keycode.F5)
                keyb.release_all()
            elif command == "F6":
                keyb.press(Keycode.F6)
                keyb.release_all()
            elif command == "F7":
                keyb.press(Keycode.F7)
                keyb.release_all()
            elif command == "F8":
                keyb.press(Keycode.F8)
                keyb.release_all()
            elif command == "F9":
                keyb.press(Keycode.F9)
                keyb.release_all()
            elif command == "F10":
                keyb.press(Keycode.F10)
                keyb.release_all()
            elif command == "F11":
                keyb.press(Keycode.F11)
                keyb.release_all()
            elif command == "F12":
                keyb.press(Keycode.F12)
                keyb.release_all()
            elif command in ["RETURN", "ENTER"]:
                keyb.press(Keycode.ENTER)
                keyb.release_all()
            elif command == "THUMBS-UP":
                keyb.press(Keycode.SHIFT)
                keyb.press(Keycode.SEMICOLON)
                keyb.release_all()
                keyb.press(Keycode.KEYPAD_PLUS)
                keyb.release_all()
                keyb.press(Keycode.ONE)
                keyb.release_all()
                keyb.press(Keycode.SHIFT)
                keyb.press(Keycode.SEMICOLON)
                keyb.release_all()
        keyb.release_all()


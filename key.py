from adafruit_hid.keycode import Keycode
from time import sleep

class Key():
    _off = ""
    _on = ""
    _effect = ""
    _command = ""
    
    def __init__(self):
        pass
    
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
    def effect(self):
        return self._effect
    
    @effect.setter
    def effect(self, value):
        self._effect = value
        
    def send(self, keyb):
        # split the string into separate strings
        self._command.replace("+","")
        keys = self._command.split()

        for command in keys:
            print(f"command: {command}, length: {len(keys)}")
            if command in ["CTRL", "CONTROL"]:
                print("press control")
                keyb.press(Keycode.CONTROL)
            elif command in ["SHIFT"]:
                print("press shift")
                keyb.press(Keycode.SHIFT)
            elif command in ["OPTION", "ALT"]:
                print("press alt")
                keyb.press(Keycode.ALT)
            elif command in ["COMMAND"]:
                print("press command")
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
            elif command in ["TAB"]:
                print("press TAB")
                keyb.press(Keycode.TAB)
#                     
#         sleep(0.10)
        keyb.release_all()
#             keyb.send(Keycode.ENTER)

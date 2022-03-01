class Key():
    _off = "FFAEBC"
    _on = "B4F8C8"
    _effect = "none"
    _command = "CTRL + A"
    
    def __init__(self):
        pass
    
    @property
    def command(self):
        return self._command
    
    @command.setter
    def command(self, value):
        self._comand = value
        
    @property
    
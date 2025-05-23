from CodeLanguageBackEnd.Variable import *
from CodeLanguageBackEnd.Mathematics import *

class Print:
    def __init__(self):
        self.display_code = '00000'
    
    
    
    def enable(self, mode: str) -> str:
        mode = mode.lower()
        if mode == 'text':
            self.display_code = self.display_code[0] + '1' + self.display_code[2:]
        elif mode == 'number':
            self.display_code = self.display_code[:2] + '1' + self.display_code[3:]
        else:
            raise ValueError("Invalid Mode")
        return f"INSERT 00000; REG M; INSERT {self.display_code}; REG L; DISP;"
    
    
    
    def disable(self, mode: str) -> str:
        mode = mode.lower()
        if mode == 'text':
            self.display_code = self.display_code[0] + '1' + self.display_code[2:]
        elif mode == 'number':
            self.display_code = self.display_code[:2] + '1' + self.display_code[3:]
        else:
            raise ValueError("Invalid Mode")
        return f"INSERT 00000; REG M; INSERT {self.display_code}; REG L; DISP;"
    
    
    def insert_val(self, val: Variable, index: int = 0) -> str:
        output = ''
        if isinstance(val, Variable):
            if isinstance(val, (Int, Char)):
                output += val.get_var() + " REG L;"
                
        elif isinstance(val, int):
            val = bin(val).removeprefix('0b').zfill(5)
            output += f" INSERT {val}; REG L;"
            
        elif isinstance(val, str):
            val = bin(int(val)).removeprefix('0b').zfill(5)
            output += f"INSERT {val}; REG L;"
        
        
        if isinstance(val, (int, Int)):
            output += f"INSERT 11111; REG M; DISP;"
        
        elif isinstance(val, (str, Char)):
            if isinstance(index, int):
                address = 21
                if index < 0 or index > 9:
                    raise ValueError
                else:
                    address += index
                    
                output += f"INSERT {address}; REG M; DISP;"
            elif isinstance(index, Variable):
                output += f"{ADD(address, index)} REG M; DISP;"
        
        return output
            
        
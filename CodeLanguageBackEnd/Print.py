"""File contains Print functions for 5 Bit Language

Author: Drake Setera

Date: 6/9/2025

Version: 2.2.0
"""



from CodeLanguageBackEnd.Variable import *
from CodeLanguageBackEnd.Mathematics import *



class Print:
    """Print class that contains all the print methods
    """



    def __init__(self):
        self.display_code = '00000'



    def enable(self, mode: str) -> str:
        """Enables mode to display

        Args:
            mode (str): Mode to enable ('t' or 'text') for text and ('n' or 'number') for numbers 

        Raises:
            ValueError: Raised if invalid mode is given

        Returns:
            str: Assembly to set computer display to that mode
        """


        mode = mode.lower()
        if mode in ('text', 't'):
            self.display_code = self.display_code[0] + '1' + self.display_code[2:]
        elif mode in ('number', 'n'):
            self.display_code = self.display_code[:2] + '1' + self.display_code[3:]
        else:
            raise ValueError("Invalid Mode")
        return f"INSERT 00000; REG M; INSERT {self.display_code}; REG L; DISP;"



    def disable(self, mode: str) -> str:
        """Disables mode to display

        Args:
            mode (str): Mode to disable ('t' or 'text') for text and ('n' or 'number') for numbers 

        Raises:
            ValueError: Raised if invalid mode is given

        Returns:
            str: Assembly to set computer display to that mode
        """


        mode = mode.lower()
        if mode == 'text':
            self.display_code = self.display_code[0] + '1' + self.display_code[2:]
        elif mode == 'number':
            self.display_code = self.display_code[:2] + '1' + self.display_code[3:]
        else:
            raise ValueError("Invalid Mode")
        return f"INSERT 00000; REG M; INSERT {self.display_code}; REG L; DISP;"



    def insert_val(self, val: Variable, index: int = 0) -> str:
        """Inserts value into display

        Args:
            val (Variable): variable or value to display contents of
            index (int, optional): If character, then index to place character at. Defaults to 0.

        Raises:
            ValueError: Raised if index is out of bounds

        Returns:
            str: Assembly to display value
        """


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

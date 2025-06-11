"""File compiles 5 bit machine code to Base 5 and vise versa

Author: Drake Setera

Date: 6/11/2025

Version: 3.0.0
"""



class Compiled5Bit:
    """Class converts 5 bit machine code of inputted file to a new file containing Base 5 code and vise versa
    """
    
    def __init__(self, file_name: str):
        if file_name.endswith('.5b'):
            self.Binary_to_Base5(file_name)
        elif file_name.endswith('.b5'):
            self.Base5_to_Binary(file_name)
        else:
            print('Wrong File Type')
            raise TypeError
    
    
    
    def Binary_to_Base5(self, file_name: str):
        """Creates a Base 5 file with the Base 5 equivalent of the Binary file provided

        Args:
            file_name (str): Binary file to convert
        """


        try:
            file = open(f"Code/Binary/{file_name}")
            binary = file.read()
            file.close()
        except:
            print("Couldn't find file")
        
        
        base5 = ''
        for i in range(0, len(binary), 5):
            base5 += self.convert_binary(binary[i:i+5])
        
        file_name = file_name.removesuffix('5b') + 'b5'
        file = open(f"Code/Base5/{file_name}", 'w')
        file.write(base5)
        file.close()
    
    
    
    def convert_binary(self, binary: str) -> str:
        """Converts binary instruction into base 5

        Args:
            binary (str): 5 bit instruction

        Returns:
            str: base 5 equivalent
        """


        val = int(binary,2)
        if val < 10:
            return str(val)
        else:
            return chr(val + 55)



    def Base5_to_Binary(self, file_name: str):
        """Creates a Binary file with the Binary equivalent of the Base 5 file provided

        Args:
            file_name (str): Base 5 file to convert
        """


        try:
            file = open(f"Code/Base5/{file_name}")
            base5 = file.read()
            file.close()
        except:
            print("Couldn't find file")
        
        
        binary = ''
        for b in base5:
            binary += self.convert_base5(b)
        
        file_name = file_name.removesuffix('b5') + '5b'
        file = open(f"Code/Binary/{file_name}", 'w')
        file.write(binary)
        file.close()
    
    
    
    def convert_base5(self, base5: str) -> str:
        """Converts base 5 instruction into binary

        Args:
            binary (str): Base 5 instruction

        Returns:
            str: binary equivalent
        """


        if base5.isdigit():
            base5 = int(base5)
            return bin(base5).removeprefix('0b').zfill(5)
        else:
            return bin(ord(base5) - 55).removeprefix('0b').zfill(5)
   
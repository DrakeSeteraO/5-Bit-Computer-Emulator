"""File contains variables for 5 Bit Language

Author: Drake Setera

Date: 6/11/2025

Version: 3.0.0
"""



class Variable:
    """Variable outline
    """


    def __init__(self, binary_address: str):
        self.type = 'none'
        self.size = 1

        if len(binary_address) != 10:
            raise ValueError("RAM Address must be 10 bits")
        else:
            self.binary_address = binary_address


    def get_address(self) -> str:
        """Gets the RAM address of variable

        Returns:
            str: Variable's binary address in the RAM
        """

        return self.binary_address


    def get_index_address(self, index: int) -> str:
        """Gets the RAM address of variable shifted index amount

        Args:
            index (int): Amount of addresses over in the RAM

        Returns:
            str: Binary address
        """

        val = int(self.binary_address, 2) + index
        return bin(val).removeprefix("0b").zfill(5)


    def set_var(self) -> str:
        """Gets assembly code to set variable

        Returns:
            str: Assembly code to set variable
        """

        return f"REG D; INSERT {self.binary_address[:5]}; REG F; INSERT {self.binary_address[5:]}; REG E; SET;"


    def set_var_to_val(self, val: str) -> str:
        """Returns assembly code to set variable to a certain value

        Args:
            val (str): Value to set variable to

        Raises:
            ValueError: Raised if invalid value

        Returns:
            str: Assembly code to set variable to certain value
        """

        if len(val) != 5:
            raise ValueError("Bit string must be 5 digits")
        else:
            return f"INSERT {val};" + self.set_var()


    def set_var_to_assembly(self, assembly: str) -> str:
        """Returns assembly code to set variable to a certain list of assembly code

        Args:
            assembly (str): Assembly code to set variable to

        Returns:
            str: Assembly code to set variable to a certain list of assembly code
        """

        return f"{assembly} {self.set_var()}"


    def get_var(self) -> str:
        """Gets assembly to get value stored in variable

        Returns:
            str: Assembly to get value stored in variable
        """

        return f"INSERT {self.binary_address[:5]};REG F;INSERT {self.binary_address[5:]};REG E; GET;"



class Int(Variable):
    """Integer variable
    """


    def __init__(self, binary_address):
        super().__init__(binary_address)
        self.type = 'int'


    def set_var_to_val(self, val: int):
        if val < 0 or val > 31:
            raise ValueError
        else:
            val = bin(val).removeprefix("0b").zfill(5)
            return super().set_var_to_val(val)



class Char(Variable):
    """Character variable
    """


    def __init__(self, binary_address):
        super().__init__(binary_address)
        self.type = 'char'

    def set_var_to_val(self, val: int):
        if val < 0 or val > 31:
            raise ValueError
        else:
            val = bin(val).removeprefix("0b").zfill(5)
            return super().set_var_to_val(val)



class Bool(Variable):
    """Boolean variable
    """


    def __init__(self, binary_address):
        super().__init__(binary_address)
        self.type = 'bool'


    def set_var_to_val(self, boolean: str):
        boolean = boolean.lower()
        if boolean == 'true' or boolean == 'false':
            val = '00000'
            if boolean == 'true':
                val = '00001'
            return super().set_var_to_val(val)
        else:
            raise ValueError("Boolean must be true or false")



class Bin(Variable):
    """Binary variable
    """


    def __init__(self, binary_address):
        super().__init__(binary_address)
        self.type = 'bin'



class Float(Variable):
    """Float variable
    """


    def __init__(self, binary_address):
        super().__init__(binary_address)
        self.type = 'float'
        self.size = 2

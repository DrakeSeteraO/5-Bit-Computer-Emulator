
class Variable:
    def __init__(self, binary_address: str):
        self.type = 'none'
        self.size = 1
        
        if len(binary_address) != 10:
            raise ValueError("RAM Address must be 10 bits")
        else:
            self.binary_address = binary_address
    
    
    def get_address(self):
        return self.binary_address
   
    
    def get_index_address(self, index: int):
        val = int(self.binary_address, 2) + index
        return bin(val).removeprefix("0b").zfill(5)
    
    
    def set_var(self):
        return f"REG D; INSERT {self.binary_address[:5]}; REG F; INSERT {self.binary_address[5:]}; REG E; SET;"
    
    
    def set_var_to_val(self, val: str):
        if len(val) != 5:
            raise ValueError("Bit string must be 5 digits")
        else:
            return f"INSERT {val};" + self.set_var()
    
    
    def set_var_to_assembly(self, assembly: str):
        return f"{assembly} {self.set_var()}" 
    
    
    def get_var(self):
        return f"INSERT {self.binary_address[:5]};REG F;INSERT {self.binary_address[5:]};REG E; GET;"



class Int(Variable):
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
    def __init__(self, binary_address):
        super().__init__(binary_address)
        self.type = 'bin'



class Float(Variable):
    def __init__(self, binary_address):
        super().__init__(binary_address)
        self.type = 'float'
        self.size = 2



        
from CodeLanguageBackEnd.Variable import *
from CodeLanguageBackEnd.Print import *
from CodeLanguageBackEnd.Mathematics import *

class CompiledCode:
    
    
    def __init__(self, file_name: str): 
        self.characters = {' ':'00', '.':'27','?':'28','!':'29',',':'30','|':'31'}
        self.variables: dict[str, Variable] = dict()
        self.maths: dict[int, MathTree] = dict()
        self.math_size = 0
        self.taken_memory = "0" * (2 ** 10)
        self.var_sizes = {'int':1,'char':1,'bool':1,'bin':1}
        self.p = Print()
        
        
        if file_name.endswith(".5bl"):
            self.convert_code(file_name)
        else:
            print("Wrong File Type")
            raise TypeError
    
    
    
    def convert_code(self, file_name: str):
        code = self.get_code(file_name)
        instructions = code.split(";")
        self.pre_math(instructions)
        assembly = self.do_instructions(instructions)
        print(self.taken_memory)
        
        try:
            file_name = file_name.removesuffix('l')
            file_name += 'a'
            file = open(f"Code/Assembly/{file_name}", 'w')
            file.write(assembly)
            file.close()
        except:
            print("Error creating assembly file")
        
        
    
    
    def get_code(self, file_name: str) -> str:
        code = ''
        try:
            file_add = r"Code/5BitLanguage/"
            file = open(file_add + f"{file_name}")
            code = file.read().replace(' ', '').replace('\n','').lower()
            file.close()
        except:
            print("Couldn't find file")
            
        code = self.convert_char(code)
        return code
    
    
    
    def convert_char(self, code: str) -> str:
        c = 0
        while c < len(code):
            if code[c] == "'":
                if len(code) - c > 1:
                    val = str(int(self.convert_to_char_num(code[c+1])) - 64).zfill(2)
                    code = code[:c+1] + val + code[c+2:]
                    c += 3
            c +=1
        return code
                
    
    
    def convert_to_char_num(self, char: str) -> str:
        char = char.upper()
        val = '00'
        if 65 <= ord(char) <= 90:
            return str(ord(char)).zfill(2)
        else:
            return self.characters[char]
    
    
    
    def get_string(self, code: str, index: int) -> list[str, int]:
        output = ''
        index += 1
        cur_char = code[index]
        try:
            while cur_char != '"' or index +1 >= len(code):
                output += cur_char
                index += 1
                cur_char = code[index]
        except Exception:
            return '', 0
        return output, index + 1
    
    
    
    def do_instructions(self, instructions: list[str]) -> str:
        self.code_num = 0
        assembly = ''
        for instruction in instructions:
            if len(instruction) > 0:
                assembly += self.perform_instruction(instruction)
                    
            self.code_num += 1
        return assembly
    
    
    
    def perform_instruction(self, instruction: str):
        if instruction[0] == '(':
            return self.declare_variable(instruction)
        
        elif instruction.startswith("print"):
            return self.print(instruction)
        
        elif instruction[0] == '~':
            return instruction[1:]
        
        elif instruction[0].isalpha():
            math = self.maths[self.code_num]
            var_type, var_name = self.get_var_info(instruction) 
            return self.variables[var_name].set_var_to_assembly(math.get_assembly(self.variables))
    
 
    
    def declare_variable(self, instruction: str):
        var_type, var_name = self.get_var_info(instruction)
        size = self.var_sizes[var_type]
        address = self.find_free_memory(size)
        self.create_var(var_type, address, var_name)
        self.update_memory_taken(address, size)
        
        if instruction.find("=") == -1:
            return ''
        else:
            parts = instruction.split("=")
            return self.set_var(var_name)
        
        
    
    def get_var_info(self, instruction: str) -> list[str,str]:
        index = 1
        var_type = ''
        if instruction[0] == '(':
            char = instruction[1]
            
            while char != ')':
                var_type += char
                index += 1
                char = instruction[index]
            index += 1
        else:
            index = 0
        
        var_name = ''
        char = instruction[index]
        while char != '=' and index < len(instruction) - 1:
            var_name += char
            index += 1
            char = instruction[index]
            
        return var_type, var_name
        
    
    
    def find_free_memory(self, size: int) -> str:
        for loc in range(len(self.taken_memory)):
            if self.valid_loc(loc, size):
                return bin(loc).removeprefix("0b").zfill(10)
        raise ValueError("Could not find memory")
    
    
    
    def valid_loc(self, loc: int, size: int) -> bool:
        for i in range(size):
            if self.taken_memory[loc+i] == '1':
                return False
        return True
    
    
    
    def update_memory_taken(self, address: str, size: int):
        if size > 0:
            address = int(address, 2)
            self.taken_memory = self.taken_memory[:address] + ('1' * size) + self.taken_memory[(address+size-1):]
    
    
    def create_var(self, type: str, address: str, name: str):
        var = None
        if type == 'int':
            var = Int(address)
        elif type == 'char':
            var = Char(address)
        elif type == 'bool':
            var = Bool(address)
        elif type == 'bin':
            var == Bin(address)
        
        self.variables[name] = var
        
        
        
    def set_var(self, var_name:str):
        math = self.maths[self.code_num]
        return self.variables[var_name].set_var_to_assembly(math.get_assembly(self.variables))
    
    
    
    def print(self, instruction: str) -> str:
        
        if instruction == 'print.enable("text")':
            return self.p.enable('text')
        if instruction == 'print.enable("number")':
            return self.p.enable('number')
        if instruction == 'print.disable("text")':
            return self.p.disable('text')
        if instruction == 'print.disable("number")':
            return self.p.disable('number')
        if instruction.startswith("print("):
            parts = instruction.split("(")
            vals = parts[1]
            vars = self.print_vars(vals)
            
            val1 = ''
            if vars[0].startswith("'"):
                val1 = vars[1:3]
            elif vars[0].isdigit():
                val1 = int(vars[0])
            else:
                val1 = self.variables[vars[0]]
            
            if len(vars) == 1:
                return self.p.insert_val(val1)
            else:
                
                val2 = ''
            if vars[1].isdigit():
                val2 = int(vars[1])
            else:
                val2 = self.variables[vars[1]]
            
            return self.p.insert_val(val1, val2)
                
                
    
    
    def print_vars(self, param:str) -> list[str]:
        var1 = ''
        var2 = ''
        cur_char = param[0]
        i = 0
        while not cur_char == ',' and not cur_char == ')':
            var1 += cur_char
            i += 1
            cur_char = param[i]
        
        if cur_char == ')':
            return [var1]
        else:
            i += 1
            cur_char = param[i]
            while cur_char != ')':
                var2 += cur_char
                i += 1
                cur_char = param[i]
            return [var1, var2]
    
    
    
    def pre_math(self, instructions: list[str]):
        math_size = 0
        for i in range(len(instructions)):
            if instructions[i].find("=") != -1:
                temp = instructions[i].split("=")
                var_type, var_name = self.get_var_info(temp[0])
                self.maths[i] = MathTree(temp[1], '0000000000', var_type)
                size = self.maths[i].get_address_size()
                if size > math_size:
                    math_size = size
        loc = self.find_free_memory(math_size)
        self.update_memory_taken(loc, math_size)
        
        
        
        
        
            
"""File compiles 5 bit language to 5 bit assembly code

Author: Drake Setera

Date: 6/20/2025

Version: 3.1.0
"""



from CodeLanguageBackEnd.Variable import *
from CodeLanguageBackEnd.Print import *
from CodeLanguageBackEnd.Mathematics import *



class CompiledCode:
    """Class converts 5 bit language of inputted file to a new file containing 5 bit assembly code
    """


    def __init__(self, file_name: str = '', display_error: bool = True): 
        self.characters = {' ':'00', '.':'27','?':'28','!':'29',',':'30','|':'31'}
        self.variables: dict[str, Variable] = dict()
        self.maths: dict[int, MathTree] = dict()
        self.math_size = 0
        self.taken_memory = "0" * (2 ** 10)
        self.var_sizes = {'int':1,'char':1,'bool':1,'bin':1}
        self.p = Print()
        self.display_error = display_error

        if len(file_name) > 0:
            if file_name.endswith(".5bl"):
                self.convert_code(file_name)
            else:
                if self.display_error:
                    print("Wrong File Type")
                raise TypeError



    def reset(self):
        """Resets the CompiledCode object
        """


        self.variables: dict[str, Variable] = dict()
        self.maths: dict[int, MathTree] = dict()
        self.math_size = 0
        self.taken_memory = "0" * (2 ** 10)
        self.p = Print()
        

        
    def convert_text_code(self, code: str) -> str:
        """Converts String 5 Bit Language to String Assembly code

        Args:
            code (str): String 5 Bit Language code to convert

        Returns:
            str: String Assembly code
        """


        self.reset()
        code = code.replace(' ', '').replace('\n','').lower()
        code = self.convert_char(code)
        instructions = code.split(";")
        
        instructions = self.pre_import(instructions)
        self.pre_math(instructions)
        self.instructions = instructions
        
        assembly = self.do_instructions(instructions)
        self.assembly = assembly
        return assembly



    def convert_code(self, file_name: str):
        """Converts the 5 Bit Language code into a 5 Bit Assembly file

        Args:
            file_name (str): 5 Bit Language file to compile (ends in .5bl)
        """


        code = self.get_code(file_name)
        instructions = code.split(";")
        
        instructions = self.pre_import(instructions)
        self.pre_math(instructions)
        self.instructions = instructions
        
        assembly = self.do_instructions(instructions)
        self.assembly = assembly

        try:
            file_name = file_name.removesuffix('l')
            file_name += 'a'
            file = open(f"Code/Assembly/{file_name}", 'w')
            file.write(assembly)
            file.close()
        except:
            if self.display_error:
                print("Error creating assembly file")



    def get_code(self, file_name: str) -> str:
        """Gets 5 Bit Language code and formats it

        Args:
            file_name (str): 5 Bit Language file to compile (ends in .5bl)

        Returns:
            str: Formatted 5 Bit Language code
        """


        code = ''
        try:
            file_add = r"Code/5BitLanguage/"
            file = open(file_add + f"{file_name}")
            code = file.read().replace(' ', '').replace('\n','').lower()
            file.close()
        except Exception:
            if self.display_error:
                print("Couldn't find file")

        code = self.convert_char(code)
        return code



    def convert_char(self, code: str) -> str:
        """Converts Char characters into their respective integer values before compilation

        Args:
            code (str): Formatted 5 Bit Language code

        Returns:
            str: Formatted 5 Bit language code with characters integer value
        """


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
        """Converts selected character to its integer value

        Args:
            char (str): Character to be converted

        Returns:
            str: String of the character's integer value
        """


        char = char.upper()
        if 65 <= ord(char) <= 90:
            return str(ord(char)).zfill(2)
        else:
            return self.characters[char]



    def get_string(self, code: str, index: int) -> list[str, int]:
        """Attempts to retrieve the string value

        Args:
            code (str): Current instruction
            index (int): Index to start string at

        Returns:
            list[str, int]: String value, Index to continue at
        """


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
        """Iterates through every 5 Bit Language instruction and converts it to assembly

        Args:
            instructions (list[str]): List of 5 Bit Language instructions

        Returns:
            str: Assembly version of the 5 Bit Language code
        """


        self.code_num = 0
        assembly = ''
        for instruction in instructions:
            if len(instruction) > 0:
                assembly += self.perform_instruction(instruction)

            self.code_num += 1
        return assembly



    def perform_instruction(self, instruction: str) -> str:
        """Converts instruction into assembly

        Args:
            instruction (str): 5 Bit Language instruction

        Returns:
            str: Assembly to perform instruction
        """


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



    def declare_variable(self, instruction: str) -> str:
        """Declares a new variable

        Args:
            instruction (str): 5 Bit Language instruction that is creating a new variable

        Returns:
            str: Assembly to create new variable
        """


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
        """Gets the selected variables name and type 

        Args:
            instruction (str): 5 Bit Language instruction containing a variable

        Returns:
            list[str,str]: Variable name, Variable type
        """


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
        """Finds free RAM memory to claim

        Args:
            size (int): Number of RAM addresses needed

        Raises:
            ValueError: Raised if there is no where to claim memory

        Returns:
            str: Starting RAM address of free memory
        """


        for loc in range(len(self.taken_memory)):
            if self.valid_loc(loc, size):
                return bin(loc).removeprefix("0b").zfill(10)
        raise ValueError("Could not find memory")



    def valid_loc(self, loc: int, size: int) -> bool:
        """Tests to see if location in the RAM is empty

        Args:
            loc (int): Starting RAM address being checked
            size (int): Number of RAM addresses that need to be open

        Returns:
            bool: Wether the location is valid in the RAM
        """


        for i in range(size):
            if self.taken_memory[loc+i] == '1':
                return False
        return True



    def update_memory_taken(self, address: str, size: int):
        """Updates the addresses in the RAM that are now taken

        Args:
            address (str): Starting RAM address being claimed
            size (int): Number of addresses being claimed
        """


        if size > 0:
            address = int(address, 2)
            self.taken_memory = self.taken_memory[:address] + ('1' * size) + self.taken_memory[(address+size-1):]



    def create_var(self, var_type: str, address: str, name: str):
        """Creates a new variable in the compiler

        Args:
            var_type (str): Variable type for the new variable
            address (str): RAM address for the new variable
            name (str): Name for the new variable
        """


        var = None
        if var_type == 'int':
            var = Int(address)
        elif var_type == 'char':
            var = Char(address)
        elif var_type == 'bool':
            var = Bool(address)
        elif var_type == 'bin':
            var == Bin(address)

        self.variables[name] = var



    def set_var(self, var_name:str) -> str:
        """Sets variable

        Args:
            var_name (str): Name of variable

        Returns:
            str: Assembly to set variable
        """


        math = self.maths[self.code_num]
        return self.variables[var_name].set_var_to_assembly(math.get_assembly(self.variables))



    def print(self, instruction: str) -> str:
        """Determines what Print action is being taken

        Args:
            instruction (str): 5 Bit Language instruction calling Print function

        Returns:
            str: Assembly perform instruction 
        """

        if instruction in ['print.enable("text")','print.enable("t")']:
            return self.p.enable('text')
        if instruction in ['print.enable("number")','print.enable("n")']:
            return self.p.enable('number')
        if instruction in ['print.disable("text")','print.disable("t")']:
            return self.p.disable('text')
        if instruction in ['print.disable("number")','print.disable("n")']:
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
        """Determines what is being printed to the screen

        Args:
            param (str): String of parameters being inputted into Print function

        Returns:
            list[str]: List of variable or values being inputted into Print function
        """


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
        """Calculates RAM needed to perform math instructions

        Args:
            instructions (list[str]): List of 5 Bit Language instructions
        """


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



    def pre_import(self, instructions: list[str]) -> list[str]:
        """Imports code from other files

        Args:
            instructions (list[str]): 5 Bit Language instructions

        Returns:
            list[str]: 5 Bit language code that has been imported
        """
        
        
        output = instructions.copy()
        
        for i in range(len(instructions)):
            
            if instructions[i].startswith("import"):
                file_name = instructions[i].removeprefix('import') + ".5bl"
                compiled = CompiledCode(file_name)
                import_code = compiled.instructions
                
                output.pop(i)
                output = output[:i] + import_code + output[i:]

        return output



    def get_compiled_assembly(self):
        """Returns the assembly of the compiled 5 Bit Language code

        Returns:
            str: assembly
        """
        
        
        return self.assembly
    
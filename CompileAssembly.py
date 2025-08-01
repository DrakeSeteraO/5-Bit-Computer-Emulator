"""File compiles 5 bit assembly to 5 bit machine code

Author: Drake Setera

Date: 6/20/2025

Version: 3.1.0
"""



import re



class CompiledAssembly:
    """Class converts assembly of inputted file to a new file containing 5 bit machine code
    """


    def __init__(self, file_name: str = '', base: str = '5b', display_error: bool = True):
        self.__valid_input = re.compile(r'^[01]{5}$')
        self.assembly_to_binary_convert = {'USER':'10010','RCV':'10011','SEND':'10100','ADD':'10101','NOT':'10110','OR':'10111','XOR':'11000','>>':'11001','SET':'11010','GET':'11011','IF':'11100','POINT':'11101','DISP':'11110','WAIT':'11111'}
        self.display_error = display_error

        if len(file_name) > 0:
            if file_name.endswith('.5ba'):
                self.convert_code(file_name, base)
            else:
                if self.display_error:
                    print('Wrong File Type')
                raise TypeError



    def convert_text_code(self, code: str) -> str:
        """Converts assembly code in string form into binary code in string form

        Args:
            code (str): String assembly code

        Returns:
            str: String binary code
        """


        assembly = self.get_assembly('', code)
        binary, errors, error_amount = self.assembly_to_binary(assembly)
        return binary
        


    def convert_code(self, file_name: str, base: str):
        """Creates and inputs machine code based on inputted assembly

        Args:
            file_name (str): Name of assembly file (ends in .5ba)
        """


        assembly = self.get_assembly(file_name)
        binary, errors, error_amount = self.assembly_to_binary(assembly)

        if self.display_error:
            print(errors)
            
        if error_amount == 0:
            try:
                if base == '5b':
                    file_name = file_name.removesuffix('a')
                    file = open(f"Code/Binary/{file_name}", 'w')
                    file.write(binary)
                    file.close()
                elif base == 'b5':
                    file_name = file_name.removesuffix('5ba') + 'b5'
                    file = open(f"Code/Base5/{file_name}", 'w')
                    base5 = self.binary_to_base5(binary)
                    file.write(base5)
                    file.close()
            except:
                if self.display_error:
                    print("Error creating binary file")



    def get_assembly(self, file_name: str, text_code: str = '') -> list[str]:
        """Gets the assembly instructions from assembly file

        Args:
            file_name (str): Name of assembly file (ends in .5ba)

        Returns:
            list[str]: List of assembly instructions
        """


        try:
            instructions = ''
            if len(text_code) == 0:
                file = open(f"Code/Assembly/{file_name}")
                instructions = file.read().split(";")
                instructions = instructions[:-1]
            else:
                instructions = text_code.split(";")
                instructions = instructions[:-1]
                

            for i in range(len(instructions)):
                instructions[i] = instructions[i].replace(' ','').replace('\n','').upper()
            file.close()
        except:
            if self.display_error:
                print("Couldn't find file")
        return instructions



    def assembly_to_binary(self, assembly: list[str]) -> list[str, str, str]:
        """Converts assembly instructions to binary machine code

        Args:
            assembly (list[str]): List of assembly instructions

        Returns:
            list[str, str, str]: machine code, error message (if any), number of errors ran into
        """


        binary = ''
        error_message = ''
        error_amount = 0

        try:
            for i in range(len(assembly)):
                try:
                    binary += self.command_to_binary(assembly[i], i)
                except InvalidCommandError as ex:
                    error_message += str(ex)
                    error_amount += 1
                except InvalidValueError as ex:
                    error_message += str(ex)
                    error_amount += 1
        except MaxInstructionError as ex:
            error_message += str(ex)
            error_amount += 1

        error_message = f"\nThe program ran into {error_amount} errors while compiling\n" + error_message 
        return binary, error_message, error_amount



    def command_to_binary(self, command: str, line_num: int) -> str:
        """Attempts to convert individual assembly instruction to binary

        Args:
            command (str): assembly instruction
            line_num (int): current command line number

        Raises:
            MaxInstructionError: Raised if line_num is greater than computer can handle
            InvalidCommandError: Raised if register doesn't exist
            InvalidValueError: Raised if inserted value is outside of 5 bit range
            InvalidValueError: Raised if insert raised value error
            InvalidCommandError: Raised if command doesn't exist

        Returns:
            str: binary of inputted instruction
        """


        if line_num >= 32768:
            raise MaxInstructionError(command, line_num)

        if command.startswith('#'):
            return ''

        if command == 'BLANK':
            return '00000'

        if command.startswith('REG'):
            try:
                value = ord(command.removeprefix('REG')) - 64
            except:
                raise InvalidCommandError(command, line_num)

            return bin(value).removeprefix('0b').zfill(5)

        if command.startswith('INSERT'):
            value = ''
            try:

                if self.__valid_input.match(command.removeprefix('INSERT')):
                    value = command.removeprefix('INSERT')
                else:
                    value = int(command.removeprefix('INSERT'))

                    if value < 0 or 31 < value:
                        raise InvalidValueError(command, value, line_num)
                    else:
                        value = bin(value).removeprefix('0b').zfill(5)
            except ValueError:
                raise InvalidValueError(command, command.removeprefix('INSERT'), line_num)
            return '10001' + value

        try:
            return self.assembly_to_binary_convert[command]
        except:
            raise InvalidCommandError(command, line_num)
    


    def binary_to_base5(self, binary: str) -> str:
        """Converts binary code to base 5

        Args:
            binary (str): Binary instructions

        Returns:
            str: Base 5 instructions
        """


        output = ''
        for i in range(0, len(binary), 5):
            output += self.convert_binary(binary[i:i+5])
        return output



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



class InvalidCommandError(Exception):
    """Error raised when command doesn't exist
    """


    def __init__(self, command, line_num):
        super().__init__(command, line_num)
        self.message = f"\n***Invalid Command Error***\nCommand Number: {line_num}\nCommand: {command}\n"

    def __str__(self):
        return self.message



class InvalidValueError(Exception):
    """Error raised when inserted value is invalid
    """


    def __init__(self, command, value, line_num):
        super().__init__(command, value, line_num)
        self.message = f"\n***Invalid Value Error***\nCommand Number: {line_num}\nValue: {value} in command: {command}\n"

    def __str__(self):
        return self.message



class MaxInstructionError(Exception):
    """Error raised when max instruction number is hit
    """


    def __init__(self, command, line_num):
        super().__init__(command, line_num)
        self.message = f"\n***Max Instructions Error***\nCommand Number: {line_num}\nCommand: {command}\n"

    def __str__(self):
        return self.message

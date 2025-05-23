import re

class CompiledAssembly:
    
    def __init__(self, file_name: str):
        self.__valid_input = re.compile(r'^[01]{5}$')
        self.assembly_to_binary_convert = {'USER':'10010','RCV':'10011','SEND':'10100','ADD':'10101','NOT':'10110','OR':'10111','XOR':'11000','>>':'11001','SET':'11010','GET':'11011','IF':'11100','POINT':'11101','DISP':'11110','WAIT':'11111'}
        
        if file_name.endswith('.5ba'):
            self.convert_code(file_name)
        else:
            print('Wrong File Type')
            raise TypeError
        
    
    
    def convert_code(self, file_name: str):
        assembly = self.get_assembly(file_name)
        binary, errors, error_amount = self.assembly_to_binary(assembly)
        
        print(errors)
        if error_amount == 0:
            try:
                file_name = file_name.removesuffix('a')
                file = open(f"Code\Binary\{file_name}", 'w')
                file.write(binary)
                file.close()
            except:
                print("Error creating binary file")
        
        
    
    def get_assembly(self, file_name):
        try:
            file = open(f"Code\Assembly\{file_name}")
            instructions = file.read().split(";")
            instructions = instructions[:-1]
            for i in range(len(instructions)):
                instructions[i] = instructions[i].replace(' ','').replace('\n','').upper()
            file.close()
        except:
            print("Couldn't find file")
        return instructions
    
    
    
    def assembly_to_binary(self, assembly: list[str]):
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
    
    
    
    def command_to_binary(self, command: str, line_num: int):
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
            
            
        
class InvalidCommandError(Exception):
    def __init__(self, command, line_num):
        super().__init__(command, line_num)
        self.message = f"\n***Invalid Command Error***\nCommand Number: {line_num}\nCommand: {command}\n"
    
    def __str__(self):
        return self.message



class InvalidValueError(Exception):
    def __init__(self, command, value, line_num):
        super().__init__(command, value, line_num)
        self.message = f"\n***Invalid Value Error***\nCommand Number: {line_num}\nValue: {value} in command: {command}\n"
    
    def __str__(self):
        return self.message



class MaxInstructionError(Exception):
    def __init__(self, command, line_num):
        super().__init__(command, line_num)
        self.message = f"\n***Max Instructions Error***\nCommand Number: {line_num}\nCommand: {command}\n"
    
    def __str__(self):
        return self.message
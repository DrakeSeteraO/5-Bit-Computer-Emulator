"""5 Bit Computer File

Author: Drake Setera

Date: 6/20/2025

Version: 3.1.0
    
"""



import re
from time import perf_counter_ns, sleep



class Computer:
    """5 Bit computer that can be imported into user's project
    """


    def __init__(self, ROM_file: str = '', hertz: int = 0, refresh_rate: int = 1, code: str = '', display_error: bool = True):
        self.set_time_per_instruction(hertz)
        self.refresh_rate = refresh_rate
        self.valid_input = re.compile(r'^[01]{5}$')
        self.characters = {0:' ', 27:'.',28:'?',29:'!',30:',',31:'|'}
        self.special_characters = {0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'+',11:'-',12:'*',13:'/',14:'=',15:'^',16:'#',17:'(',18:')',19:'&',20:"'",21:'"',22:'@',23:':',24:';',25:'<',26:'>',27:'%',28:'~',29:'[',30:']',31:'|'}
        self.instructions = list()
        self.display_error = display_error
        self.set_up()
        
        if len(code) == 0:
            self.load_ROM(ROM_file)
        else:
            self.load_code(code)




    def load_new_program(self, code: str):
        """Loads a new program into the ROM

        Args:
            code (str): Binary code to load into ROM
        """


        self.set_up()
        self.load_code(code)



    def load_code(self, code: str):
        """Loads code into instructions to perform

        Args:
            code (str): Binary to execute
        """

        self.instructions = list()
        if len(code) % 5 == 0 and len(code) >= 5:
            for i in range(0,len(code),5):
                self.instructions.append(f"{code[i]}{code[i+1]}{code[i+2]}{code[i+3]}{code[i+4]}")



    def load_ROM(self, ROM_file: str):
        """Loads ROM file's data into instructions to perform

        Args:
            ROM_file (str): Binary or Base 5 file to execute, ends in .5b or .b5
        """


        if ROM_file.endswith(".5b"):
            try:
                file = open(f"Code/Binary/{ROM_file}")

                self.instructions = list()
                code = file.read()
                for i in range(0,len(code),5):
                    self.instructions.append(f"{code[i]}{code[i+1]}{code[i+2]}{code[i+3]}{code[i+4]}")
                file.close()
            except:
                if self.display_error:
                    print("There was an error loading the ROM file")

        elif ROM_file.endswith(".b5"):
            try:
                file = open(f"Code/Base5/{ROM_file}")

                self.instructions = list()
                code = file.read()
                for c in code:
                    self.instructions.append(self.base5_to_binary(c))
                file.close()
            except:
                if self.display_error:
                    print("There was an error loading the ROM file")

        else:
            if self.display_error:
                print("Wrong file type")



    def set_time_per_instruction(self, hertz: int):
        """Updates the amount of nanoseconds per instruction based on computer hertz

        Args:
            hertz (int): The computer's hertz
        """


        if hertz <= 0:
            self.__time_per_instruction = 0
        else:
            self.__time_per_instruction = 1 / hertz



    def set_up(self):
        """Sets up the computer's starting values
        """


        self.steps = 0
        self.sleep = 0
        self.wait_wireless = False
        self.wait_sleep = False
        self.end = False

        self.REG = ['00000'] * 16
        self.BUS = '00000'
        self.ALU = '00000'
        self.USER = False
        self.RCV = False
        self.RAM = '00000' * (2 ** 10)
        self.DISP = '00000' * (2 ** 5)
        self.WAIT = '00000'



    def run(self, stop_step=32768):
        """Run the ROM file and ends once all instructions are completed

        Args:
            stop_step (int, optional): Instruction number to stop at (exclusive). 
             Defaults to 32768 (MAX number of instructions).
        """


        step = 0
        while not self.end and step < stop_step:

            start = perf_counter_ns()
            self.step()
            end = perf_counter_ns()
            time = end - start
            if time < self.__time_per_instruction * 1000000000:
                sleep(self.__time_per_instruction - (time / 1000000000))
            step += 1



    def step(self, amount=1):
        """Perform number of instructions. Starting at current instruction in computer.

        Args:
            amount (int, optional): Number of instructions to perform. Defaults to 1.
        """


        if amount < 1:
            amount = 1

        for _ in range(amount):
            self.do_instruction()



    def reset_wait(self):
        """Resets wait registers
        """


        self.wait_wireless = False
        self.wait_sleep = False
        self.sleep = 0



    def pre_instruction(self):
        """Determines if program should end before instruction is performed
        or if waiting for inputs

        Returns:
            bool: Weather instruction should be performed
        """


        if self.end:
            return False

        if self.steps >= len(self.instructions):
            self.end = True
            return False

        if self.wait_wireless:
            if self.BUS != '00000':
                self.reset_wait()
                return True

        if self.wait_sleep:
            if self.sleep == 0:
                self.reset_wait()
                return True
            else:
                self.sleep -= 1

        if self.wait_wireless or self.wait_sleep:
            return False

        return True



    def do_instruction(self):
        """Performs current instruction
        """


        do = self.pre_instruction()

        if do:
            instruction = self.instructions[self.steps]
            instruction = int(instruction, 2)

            if 0 < instruction < 3 or  3 < instruction < 17:
                self.REG[instruction - 1] = self.BUS

            elif instruction == 3:
                self.REG[2] = self.ALU
                self.BUS = self.REG[2]

            elif instruction == 17:
                self.BUS = self.instructions[self.steps + 1]
                self.steps += 1

            elif instruction == 18:
                self.USER = self.USER ^ True

            elif instruction == 19:
                self.RCV = self.RCV ^ True

            elif instruction == 21:
                self.ALU = bin(int(self.REG[0],2) + int(self.REG[1],2)).removeprefix('0b').zfill(5)[-5:]

            elif instruction == 22:
                temp = ''
                for i in self.REG[0]:
                    if i == '0':
                        temp += '1'
                    else:
                        temp += '0'
                self.ALU = temp

            elif instruction == 23:
                temp = ''
                for i in range(5):
                    if self.REG[0][i] == '1' or self.REG[1][i] == '1':
                        temp += '1'
                    else:
                        temp += '0'
                self.ALU = temp

            elif instruction == 24:
                temp = ''
                for i in range(5):
                    if self.REG[0][i] == '1' or self.REG[1][i] == '1':
                        if self.REG[0][i] == '1' and self.REG[1][i] == '1':
                            temp += '0'
                        else:
                            temp += '1'
                    else:
                        temp += '0'
                self.ALU = temp

            elif instruction == 25:
                self.ALU = '0' + self.REG[0][:-1]

            elif instruction == 26:
                address = (int(self.REG[5],2) * 32) + int(self.REG[4],2)
                self.RAM = self.RAM[:(address * 5)] + self.REG[3] + self.RAM[((address+1) * 5):]

            elif instruction == 27:
                address = (int(self.REG[5],2) * 32) + int(self.REG[4],2)
                self.BUS = self.RAM[(address * 5):((address+1) * 5)]

            elif instruction == 28:
                if self.REG[6] != self.REG[7]:
                    self.steps += 1

            elif instruction == 29:
                pointer = (int(self.REG[10],2) * 1024) + (int(self.REG[9],2) * 32) + int(self.REG[8],2)
                self.steps = pointer - 1

            elif instruction == 30:
                address = int(self.REG[12],2)
                self.DISP = self.DISP[:(address * 5)] + self.REG[11] + self.DISP[((address+1) * 5):]

            elif instruction == 31:
                self.WAIT = self.REG[13]
                if self.WAIT[0] == '1':
                    self.sleep = (int(self.REG[15],2) * 32) + int(self.REG[14],2)
                    self.wait_sleep = True
                if self.WAIT[1] == '1':
                    self.BUS = '00000'
                    self.wait_wireless = True
                if self.WAIT[2] == '1':
                    temp = input()
                    if self.valid_input.match(temp):
                        self.BUS = temp
                    else:
                        print('Invalid Input')
                if self.WAIT[4] == '1':
                    self.end = True

            self.steps += 1
        self.load_display()



    def load_display(self):
        """Displays data
        """


        if self.steps % self.refresh_rate == 0:
            output = ''
            if self.DISP[0] == '1' or self.DISP[1] == '1' or self.DISP[2] == '1':
                output = '=' * 21
                output += "\n"

            if self.DISP[0] == '1':
                output += self.load_screen()
            if self.DISP[1] == '1':
                output += self.load_characters()
            if self.DISP[2] == '1':
                val = int(self.DISP[155:],2)
                if val <= 15:
                    output += f"\n{val}"
                else:
                    output += f"\n{self.two_complement(val)}"
                    
            print(output)



    def two_complement(self, val: int) -> str:
        binary = bin(val).removeprefix('0b').zfill(5)
        temp = ''
        for b in binary:
            if b == '1':
                temp += '0'
            else:
                temp += '1'
        val = int(temp,2) + 1
        return f"-{val}"
        
        
        
    def load_screen(self) -> str:
        """Loads 10x10 screen

        Returns:
            str: Current state of the screen
        """


        screen = ''
        for i in range(1, 21):
            values = self.DISP[(i * 5):((i+1) * 5)]
            for v in values:
                if v == '1':
                    screen += '⬜'
                else:
                    screen += '⬛'
            if i % 2 == 0:
                screen += '\n'
        return screen



    def load_characters(self) -> str:
        """Loads characters displayed by screen

        Returns:
            str: characters displayed
        """


        output = ''
        char = ''
        special = False

        for i in range(105, 155, 5):
            value = self.DISP[i:i+5]
            value = int(value, 2)

            if not special:
                char, special = self.get_character(value)
                if not special:
                    output += char
            else:
                output += self.special_characters[value]
                special = False

        return output



    def get_character(self, value: int) -> list[str, bool]:
        """Returns the character of the given value

        Args:
            value (int): value of the character

        Returns:
            list[str, bool]: character, is special character
        """


        if 0 < value < 27:
            return chr(64 + value), False

        character = self.characters[value]
        if character ==  '|':
            return '', True
        return character, False



    def base5_to_binary(self, base5: str) -> str:
        """Converts Base 5 instruction into binary instruction

        Args:
            base5 (str): Base 5 instruction to convert

        Returns:
            str: Binary instruction equivalence
        """


        if base5.isdigit():
            return bin(int(base5)).removeprefix('0b').zfill(5)
        else:
            return bin(ord(base5) - 55).removeprefix('0b').zfill(5)

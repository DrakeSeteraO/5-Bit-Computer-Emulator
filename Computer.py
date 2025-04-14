import re
from time import perf_counter_ns, sleep

class Computer:
    
    
    
    def __init__(self, ROM_file='machineCode.5b',hertz=0):
        self.load_ROM(ROM_file)
        self.set_time_per_instruction(hertz)
        self.__valid_input = re.compile(r'^[01]{5}$')
        self.__characters = {0:' ', 27:'.',28:'?',29:'!',30:',',31:'|'}
        self.__special_characters = {0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'+',11:'-',12:'*',13:'/',14:'=',15:'^',16:'#',17:'(',18:')',19:'&',20:"'",21:'"',22:'@',23:':',24:';',25:'<',26:'>',27:'%',28:'~',29:'[',30:']',31:'|'}
        self.set_up()
        
    
    
    def load_ROM(self, ROM_file: str):
        if ROM_file.endswith(".5b"):
            try:
                file = open(f"Code\Binary\{ROM_file}")
            
                self.__instructions = list()
                code = file.read()
                for i in range(0,len(code),5):
                    self.__instructions.append(f"{code[i]}{code[i+1]}{code[i+2]}{code[i+3]}{code[i+4]}")  
                file.close() 
            except:
                print("There was an error loading the ROM file")
        else:
            print("Wrong file type")
    
    
    
    def set_time_per_instruction(self, hertz: int):
        if hertz <= 0:
            self.__time_per_instruction = 0
        else:
            self.__time_per_instruction = 1 / hertz
    
    
    
    def set_up(self):
        self.__step = 0
        self.__sleep = 0
        self.__wait_wireless = False
        self.__wait_sleep = False
        self.__end = False
        
        self.__REG = ['00000'] * 16
        self.__BUS = '00000'
        self.__ALU = '00000'
        self.__USER = False
        self.__RCV = False
        self.__RAM = '00000' * (2 ** 10)
        self.__DISP = '00000' * (2 ** 5)
        self.__WAIT = '00000'
        

    def run(self, stop_step=32768):
        step = 0
        while not self.__end and step < stop_step:
            
            start = perf_counter_ns()
            self.step()
            end = perf_counter_ns()
            time = end - start
            if time < self.__time_per_instruction * 1000000000:
                sleep(self.__time_per_instruction - (time / 1000000000))
            step += 1
            
        
        
    def step(self, amount=1):
        if amount < 1:
            amount = 1
        
        for i in range(amount):
            self.do_instruction()
    
    
    
    def reset_wait(self):
        self.__wait_wireless = False
        self.__wait_sleep = False
        self.__sleep = 0
     
     
        
    def pre_instruction(self):
        if self.__end:
            return False
        if self.__step >= len(self.__instructions):
            self.__end = True
            return False
        if self.__wait_wireless:
            if self.__BUS != '00000':
                self.reset_wait()
                return True
        if self.__wait_sleep:
            if self.__sleep == 0:
                self.reset_wait()
                return True
            else:
                self.__sleep -= 1
        if self.__wait_wireless or self.__wait_sleep:
            return False
        return True
                
        
        
    def do_instruction(self):
        do = self.pre_instruction()
        
        if do:
            instruction = self.__instructions[self.__step]
            instruction = int(instruction, 2)
            
            if 0 < instruction < 3 or  3 < instruction < 17:
                self.__REG[instruction - 1] = self.__BUS
            
            elif instruction == 3:
                self.__REG[2] = self.__ALU
                self.__BUS = self.__REG[2]
                
            elif instruction == 17:
                self.__BUS = self.__instructions[self.__step + 1]
                self.__step += 1
                
            elif instruction == 18:
                self.__USER = self.__USER ^ True
                
            elif instruction == 19:
                self.__RCV = self.__RCV ^ True
                
            elif instruction == 21:
                self.__ALU = bin(int(self.__REG[0],2) + int(self.__REG[1],2)).removeprefix('0b').zfill(5)
                
            elif instruction == 22:
                temp = ''
                for i in self.__REG[0]:
                    if i == '0':
                        temp += '1'
                    else:
                        temp += '0'
                self.__ALU = temp
                
            elif instruction == 23:
                temp = ''
                for i in range(5):
                    if self.__REG[0][i] == '1' or self.__REG[1][i] == '1':
                        temp += '1'
                    else:
                        temp += '0'
                self.__ALU = temp
                
            elif instruction == 24:
                temp = ''
                for i in range(5):
                    if self.__REG[0][i] == '1' or self.__REG[1][i] == '1':
                        if self.__REG[0][i] == '1' and self.__REG[1][i] == '1':
                            temp += '0'
                        else: 
                            temp += '1'
                    else:
                        temp += '0'
                self.__ALU = temp
            
            elif instruction == 25:
                self.__ALU = '0' + self.__REG[0][:-1]
            
            elif instruction == 26:
                address = (int(self.__REG[5],2) * 32) + int(self.__REG[4],2)
                self.__RAM = self.__RAM[:(address * 5)] + self.__REG[3] + self.__RAM[((address+1) * 5):]
            
            elif instruction == 27:
                address = (int(self.__REG[5],2) * 32) + int(self.__REG[4],2)
                self.__BUS = self.__RAM[(address * 5):((address+1) * 5)]
            
            elif instruction == 28:
                if self.__REG[6] != self.__REG[7]:
                    self.__step += 1
            
            elif instruction == 29:
                pointer = (int(self.__REG[10],2) * 1024) + (int(self.__REG[9],2) * 32) + int(self.__REG[8],2)
                self.__step = pointer - 1
            
            elif instruction == 30:
                address = int(self.__REG[12],2)
                self.__DISP = self.__DISP[:(address * 5)] + self.__REG[11] + self.__DISP[((address+1) * 5):]
            
            elif instruction == 31:
                self.__WAIT = self.__REG[13]
                if self.__WAIT[0] == '1':
                    self.__sleep = (int(self.__REG[15],2) * 32) + int(self.__REG[14],2)
                    self.__wait_sleep = True
                if self.__WAIT[1] == '1':
                    self.__BUS = '00000'
                    self.__wait_wireless = True
                if self.__WAIT[2] == '1':
                    temp = input()
                    if self.__valid_input.match(temp):
                        self.__BUS = temp
                    else:
                        print('Invalid Input')
                if self.__WAIT[4] == '1':
                    self.__end = True
                    
            self.__step += 1
        self.load_display()
    
    
    
    def load_display(self):
        output = ''
        if self.__DISP[0] == '1' or self.__DISP[1] == '1' or self.__DISP[0] == '1':
            output = '=' * 21
            output += "\n"
            
        if self.__DISP[0] == '1':
            output += self.load_screen()
        if self.__DISP[1] == '1':
            output += self.load_characters()
        if self.__DISP[2] == '1':
            output += f"\n{int(self.__DISP[155:],2)}"
        print(output)
    
    
    
    def load_screen(self):
        screen = ''
        for i in range(1, 21):
            values = self.__DISP[(i * 5):((i+1) * 5)]
            for v in values:
                if v == '1':
                    screen += '⬜'
                else:
                    screen += '⬛'
            if i % 2 == 0:
                screen += '\n'
        return screen
                    
    
    
    
    def load_characters(self):
        output = ''
        char = ''
        special = False
        for i in range(105, 155, 5):
            value = self.__DISP[i:i+5]
            value = int(value, 2)
            
            if not special:
                char, special = self.get_character(value)
                if not special:
                    output += char
            else:
                output += self.__special_characters[value]
                special = False
                
        return output
    
    
    
    def get_character(self, value):
        if 0 < value < 27:
            return chr(64 + value), False
        
        character = self.__characters[value]
        if character ==  '|':
            return '', True
        return character, False
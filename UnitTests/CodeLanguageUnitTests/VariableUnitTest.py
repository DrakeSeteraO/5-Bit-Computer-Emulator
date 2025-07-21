"""File unit tests 5 Bit Language Variables

Author: Drake Setera

Date: 6/20/2025

Version: 3.1.0
"""


import sys
import json
import unittest
from random import randint
from math import floor
from faker import Faker



json_data = dict()
with open("Private.json", "r") as file:
    json_data = json.load(file)   
sys.path.append(json_data["Unit_Test_Path"])



from Computer import Computer
from CompileAssembly import CompiledAssembly
from CompileCode import CompiledCode



fake = Faker()
c = Computer(code = ' ', display_error= False)
a = CompiledAssembly(display_error= False)
l = CompiledCode(display_error= False)



n = 25
class TestVariable(unittest.TestCase):
    """tests 5 Bit Language Variables
    """

    
    def run_code(self, code: str):
        c.load_new_program(a.convert_text_code(l.convert_text_code(code)))
        c.run()


    
    def test_declare_INT(self):
        for _ in range(n):
            var_name = fake.name().replace(' ','').lower()
            val = randint(0, 31)
            command = f"(int) {var_name} = {val};"
            
            self.run_code(command)
            
            error_msg = f"Problem declaring INT. Command: {command} returned {c.RAM[0:5]}"
            self.assertEqual(c.RAM[0:5], bin(val).removeprefix('0b').zfill(5), error_msg)
    
    
    
    def test_declare_CHAR(self):
        for _ in range(n):
            var_name = fake.name().replace(' ','').lower()
            val = randint(0, 25)
            char = chr(val + 65)
            command = f"(char) {var_name} = '{char}';"
            
            self.run_code(command)
            
            error_msg = f"Problem declaring CHAR. Command: {command} returned {c.RAM[0:5]}"
            self.assertEqual(c.RAM[0:5], bin(val+1).removeprefix('0b').zfill(5), error_msg)
    
if __name__ == '__main__':
    unittest.main()
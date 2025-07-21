"""File unit tests 5 Bit Language Math

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


    
    def test_ADD(self):
        for _ in range(n):
            var_name = fake.name().replace(' ','').lower()
            val1 = randint(0, 31)
            val2 = randint(0, 31)
            command = f"(int) {var_name} = {val1} + {val2};"
            
            self.run_code(command)
            
            expected = bin(val1+val2).removeprefix('0b').zfill(5)[-5:]
            error_msg = f"Problem with ADD. Command: {command} returned {c.RAM[5:10]}"
            self.assertEqual(c.RAM[5:10], expected, error_msg)
    
    
    
    def test_OR(self):
        for _ in range(n):
            var_name = fake.name().replace(' ','').lower()
            val1 = randint(0, 31)
            val2 = randint(0, 31)
            command = f"(int) {var_name} = {val1} | {val2};"
            
            self.run_code(command)
            
            expected = bin(val1 | val2).removeprefix('0b').zfill(5)[-5:]
            error_msg = f"Problem with OR. Command: {command} returned {c.RAM[5:10]}"
            self.assertEqual(c.RAM[5:10], expected, error_msg)
    
    
    
    def test_AND(self):
        for _ in range(n):
            var_name = fake.name().replace(' ','').lower()
            val1 = randint(0, 31)
            val2 = randint(0, 31)
            command = f"(int) {var_name} = {val1} & {val2};"
            
            self.run_code(command)
            
            expected = bin(val1 & val2).removeprefix('0b').zfill(5)[-5:]
            error_msg = f"Problem with AND. Command: {command} returned {c.RAM[5:10]}"
            self.assertEqual(c.RAM[5:10], expected, error_msg)
    
    
    
    def test_XOR(self):
        for _ in range(n):
            var_name = fake.name().replace(' ','').lower()
            val1 = randint(0, 31)
            val2 = randint(0, 31)
            command = f"(int) {var_name} = {val1} ^ {val2};"
            
            self.run_code(command)
            
            expected = bin((val1+32) ^ (val2+32)).removeprefix('0b').zfill(5)[-5:]
            error_msg = f"Problem with XOR. Command: {command} returned {c.RAM[5:10]}"
            self.assertEqual(c.RAM[5:10], expected, error_msg)



    def two_complement(self, val: int) -> str:
        if val < 0:
            string = bin(val).removeprefix('-0b').zfill(5)
            temp = ''
            for s in string:
                if s == '1':
                    temp += '0'
                else:
                    temp += '1'
            val = int(temp, 2) + 1
        return val



    def test_SUB(self):
        for _ in range(n):
            var_name = fake.name().replace(' ','').lower()
            val1 = randint(0, 31)
            val2 = randint(0, 31)
            command = f"(int) {var_name} = {val1} - {val2};"
            
            self.run_code(command)
            
            val = val1 - val2
            expected = ''
            if val < 0:
                val = self.two_complement(val)
            expected = bin(val).removeprefix('0b').zfill(5)[-5:]
                
            error_msg = f"Problem with SUB. Command: {command} returned {c.RAM[5:10]}"
            self.assertEqual(c.RAM[5:10], expected, error_msg)
        
        command = f"(int) {var_name} = -5;"   
        self.run_code(command)
        print(c.RAM)
    
    
    
    def NOT(self, val: int) -> str:
        val = bin(val).removeprefix('0b').zfill(5)
        out = ''
        for v in val:
            if v == '1':
                out += '0'
            else:
                out += '1'
        return out
        
        
        
    def test_NOT(self):
        for _ in range(n):
            var_name = fake.name().replace(' ','').lower()
            val = randint(0, 31)
            command = f"(int) {var_name} = {val}!;"
            
            self.run_code(command)
            
            expected = self.NOT(val)
            error_msg = f"Problem with NOT. Command: {command} returned {c.RAM[5:10]}"
            self.assertEqual(c.RAM[5:10], expected, error_msg)
    
    
    
    def test_NOT_EQUAL(self):
        for _ in range(n):
            var_name = fake.name().replace(' ','').lower()
            val1 = randint(0, 31)
            val2 = randint(0, 31)
            command = f"(int) {var_name} = {val1} !: {val2};"
            
            self.run_code(command)
            
            expected = '00001'
            if val1 == val2:
                expected = '00000'

            error_msg = f"Problem with NOT EQUAL. Command: {command} returned {c.RAM[5:10]}"
            self.assertEqual(c.RAM[5:10], expected, error_msg)



    def test_EQUAL(self):
       for _ in range(n):
            var_name = fake.name().replace(' ','').lower()
            val1 = randint(0, 31)
            val2 = randint(0, 31)
            command = f"(int) {var_name} = {val1} : {val2};"
            
            self.run_code(command)
            
            expected = '00000'
            if val1 == val2:
                expected = '00001'

            error_msg = f"Problem with EQUAL. Command: {command} returned {c.RAM[5:10]}"
            self.assertEqual(c.RAM[5:10], expected, error_msg)



    def test_LESS_THAN(self):
       for _ in range(n):
            var_name = fake.name().replace(' ','').lower()
            val1 = randint(0, 15)
            val2 = randint(0, 15)
            command = f"(int) {var_name} = {val1} < {val2};"
            
            self.run_code(command)
            
            expected = '00000'
            if val1 < val2:
                expected = '00001'

            error_msg = f"Problem with LESS THAN. Command: {command} returned {c.RAM[5:10]}"
            self.assertEqual(c.RAM[5:10], expected, error_msg)



    def test_GREATER_THAN(self):
       for _ in range(n):
            var_name = fake.name().replace(' ','').lower()
            val1 = randint(0, 15)
            val2 = randint(0, 15)
            command = f"(int) {var_name} = {val1} > {val2};"
            
            self.run_code(command)
            
            expected = '00000'
            if val1 > val2:
                expected = '00001'

            error_msg = f"Problem with GREATER THAN. Command: {command} returned {c.RAM[5:10]}"
            self.assertEqual(c.RAM[5:10], expected, error_msg)



    # def test_LESS_THAN_OR_EQUAL(self):
    #    for _ in range(n):
    #         var_name = fake.name().replace(' ','').lower()
    #         val1 = randint(0, 15)
    #         val2 = randint(0, 15)
    #         command = f"(int) {var_name} = {val1} <: {val2};"
            
    #         self.run_code(command)
            
    #         expected = '00000'
    #         if val1 <= val2:
    #             expected = '00001'

    #         error_msg = f"Problem with LESS THAN OR EQUAL. Command: {command} returned {c.RAM[5:10]}"
    #         self.assertEqual(c.RAM[5:10], expected, error_msg)
    
    
    
    def test_GREATER_THAN_OR_EQUAL(self):
       for _ in range(n):
            var_name = fake.name().replace(' ','').lower()
            val1 = randint(0, 15)
            val2 = randint(0, 15)
            command = f"(int) {var_name} = {val1} >: {val2};"
            
            self.run_code(command)
            
            expected = '00000'
            if val1 >= val2:
                expected = '00001'

            error_msg = f"Problem with GREATER THAN OR EQUAL. Command: {command} returned {c.RAM[5:10]}"
            self.assertEqual(c.RAM[5:10], expected, error_msg)
    
if __name__ == '__main__':
    unittest.main()
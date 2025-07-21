"""File unit tests Computer.py

Author: Drake Setera

Date: 6/20/2025

Version: 3.1.0
"""


import sys
import json
import unittest
from random import randint
from math import floor



json_data = dict()
with open("Private.json", "r") as file:
    json_data = json.load(file)   
sys.path.append(json_data["Unit_Test_Path"])



from Computer import Computer



c = Computer(code = ' ', display_error= False)
n = 5
class TestComputer(unittest.TestCase):
    """Tests Computer.py file
    """

    
    def test_INSERT(self):
        for _ in range(n):
            rand_val = randint(0,31)
            bin_val = bin(rand_val).removeprefix('0b').zfill(5)
            
            c.load_new_program(f"10001{bin_val}")
            c.run()

            error_msg = f"Bus value {c.BUS}. Did not equal Insert value {bin_val}"
            self.assertEqual(c.BUS, bin_val, error_msg)
    
    
    
    def test_REG(self):
        c.load_new_program(f"1000100000")
        c.run()
        self.assertEqual(c.REG, ['00000'] * 16, "Invalid starting state for REG")
        
        
        for x in range(15):
            if x != 2:
                rand_val = randint(0,31)
                bin_val = bin(rand_val).removeprefix('0b').zfill(5)
                REG_val = bin(x + 1).removeprefix('0b').zfill(5)
                
                c.load_new_program(f"10001{bin_val}{REG_val}")
                c.run()

                error_msg = f"REG value {c.REG[x]}. Did not equal Insert value {bin_val}"
                self.assertEqual(c.REG[x], bin_val, error_msg)
    
    
    
    def test_RCV_and_USER(self):
        c.load_new_program(f"10010")
        c.run()
        self.assertEqual(c.USER, True, "Invalid USER state")
        
        c.load_new_program(f"1001010010")
        c.run()
        self.assertEqual(c.USER, False, "Invalid USER state")
        
        c.load_new_program(f"10011")
        c.run()
        self.assertEqual(c.RCV, True, "Invalid RCV state")
        
        c.load_new_program(f"1001110011")
        c.run()
        self.assertEqual(c.RCV, False, "Invalid RCV state")
    
    
    
    def test_ALU(self):
        
        # ADD
        for _ in range(n):
            a = randint(0, 31)
            b = randint(0, 31)
            
            c.load_new_program(f"10001{bin(a).removeprefix('0b').zfill(5)}0000110001{bin(b).removeprefix('0b').zfill(5)}000101010100011")
            c.run()
            
            expected = bin(a + b).removeprefix('0b').zfill(5)[-5:]
            error_msg = f"ADD provided unexpected output: {a} + {b} != {int(c.BUS,2)}"
            self.assertEqual(c.BUS, expected, error_msg)
        
        
        # NOT
        for _ in range(n):
            a = randint(0, 31)
            
            c.load_new_program(f"10001{bin(a).removeprefix('0b').zfill(5)}000011011000011")
            c.run()
            
            expected = bin(a ^ 31).removeprefix('0b').zfill(5)
            error_msg = f"NOT provided unexpected output: {a}! != {int(c.BUS,2)}"
            self.assertEqual(c.BUS, expected, error_msg)
        
        
        # OR
        for _ in range(n):
            a = randint(0, 31)
            b = randint(0, 31)
            
            c.load_new_program(f"10001{bin(a).removeprefix('0b').zfill(5)}0000110001{bin(b).removeprefix('0b').zfill(5)}000101011100011")
            c.run()
            
            expected = bin(a | b).removeprefix('0b').zfill(5)
            error_msg = f"OR provided unexpected output: {bin(a).removeprefix('0b').zfill(5)} or {bin(b).removeprefix('0b').zfill(5)} != {c.BUS}"
            self.assertEqual(c.BUS, expected, error_msg)
        
        
        # XOR
        for _ in range(n):
            a = randint(0, 31)
            b = randint(0, 31)
            
            c.load_new_program(f"10001{bin(a).removeprefix('0b').zfill(5)}0000110001{bin(b).removeprefix('0b').zfill(5)}000101100000011")
            c.run()
            
            expected = bin(a ^ b).removeprefix('0b').zfill(5)[-5:]
            error_msg = f"XOR provided unexpected output: {bin(a).removeprefix('0b').zfill(5)} or {bin(b).removeprefix('0b').zfill(5)} != {c.BUS}"
            self.assertEqual(c.BUS, expected, error_msg)
        
        
        # R Shift
        for _ in range(n):
            a = randint(0, 31)
            
            c.load_new_program(f"10001{bin(a).removeprefix('0b').zfill(5)}000011100100011")
            c.run()
            
            expected = bin(floor(a / 2)).removeprefix('0b').zfill(5)
            error_msg = f"NOT provided unexpected output: {a}! != {int(c.BUS,2)}"
            self.assertEqual(c.BUS, expected, error_msg)



    def test_RAM(self):
        for _ in range(n):
            address_num = randint(0, 2 ** 10 - 1)
            address = bin(address_num).removeprefix('0b').zfill(10)
            val = bin(randint(0, 31)).removeprefix('0b').zfill(5)
            
            c.load_new_program(f"10001{val}0010010001{address[:5]}0011010001{address[5:]}0010111010100010000011011")
            c.run()
            
            error_msg = f"RAM GET wrong value, expected: {val}, got: {c.BUS}"
            self.assertEqual(c.BUS, val, error_msg)
            
            error_msg = f"RAM SET wrong value, expected: {val}, got: {c.RAM[5*address_num:5*(address_num+1)]}"
            self.assertEqual(c.RAM[5*address_num:5*(address_num+1)], val, error_msg)
if __name__ == '__main__':
    unittest.main()
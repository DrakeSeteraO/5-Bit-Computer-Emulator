"""File used to compile files to machine code the 5 bit computer can read

Author: Drake Setera

Date: 6/11/2025

Version: 3.0.0
"""



from CompileAssembly import CompiledAssembly
from CompileBase5 import Compiled5Bit
from CompileCode import CompiledCode



def main():
    """Function used to compressed data
    """


    file:str = input("What file would you like to compile?\n")

    valid_input = False
    choice = ''
    if file.endswith(".5ba"):
        while not valid_input:
            choice = input("\nWhat would you like to compress the file to?\nMachine code '.5b' (m)\nBase 5 '.b5' (b)\n")
            if choice.upper() in ['M','B']:
                valid_input = True
            else:
                print("Invalid input")

        if choice.upper() == 'M':
            compiled = CompiledAssembly(file)
        if choice.upper() == 'B':
            compiled = CompiledAssembly(file,'b5')

    elif file.endswith(".5bl"):
        while not valid_input:
            choice = input("\nWhat would you like to compress the file to?\nAssembly code '.5ba' (a)\nMachine code '.5b' (m)\nBase 5 '.b5' (b)")
            if choice.upper() in ['M', 'A', 'B']:
                valid_input = True
            else:
                print("Invalid input")

        if choice.upper() == 'A':
            compiled = CompiledCode(file)
        elif choice.upper() == 'M':
            compiled1 = CompiledCode(file)
            file = file.removesuffix("l") + "a"
            compiled2 = CompiledAssembly(file)
        elif choice.upper() == 'B':
            compiled1 = CompiledCode(file)
            file = file.removesuffix("l") + "a"
            compiled2 = CompiledAssembly(file, 'b5')
    
    elif file.endswith(".5b"):
        while not valid_input:
            choice = input("\nWhat would you like to compress the file to?\nBase 5 '.b5' (b)\n")
            if choice.upper() == 'B':
                valid_input = True
            else:
                print("Invalid input")

        if choice.upper() == 'B':
            compiled = Compiled5Bit(file)
    
    elif file.endswith(".b5"):
        while not valid_input:
            choice = input("\nWhat would you like to compress the file to?\nMachine code '.5b' (m)\n")
            if choice.upper() == 'M':
                valid_input = True
            else:
                print("Invalid input")

        if choice.upper() == 'B':
            compiled = Compiled5Bit(file)



if __name__ == '__main__':
    main()

"""File used to compile files to machine code the 5 bit computer can read

Author: Drake Setera

Date: 6/7/2025

Version: 2.1.0
"""



from CompileAssembly import CompiledAssembly
from CompileCode import CompiledCode



def main():
    """Function used to compressed data
    """


    file:str = input("What file would you like to compile?\n")

    valid_input = False
    choice = ''
    if file.endswith(".5ba"):
        while not valid_input:
            choice = input("\nWhat would you like to compress the file to?\nMachine code '.5b' (m)\n")
            if choice.upper() == 'M':
                valid_input = True
            else:
                print("Invalid input")

        if choice.upper() == 'M':
            compiled = CompiledAssembly(file)

    elif file.endswith(".5bl"):
        while not valid_input:
            choice = input("\nWhat would you like to compress the file to?\nAssembly code '.5ba' (a)\nMachine code '.5b' (m)\n")
            if choice.upper() == 'M' or choice.upper() == 'A':
                valid_input = True
            else:
                print("Invalid input")

        if choice.upper() == 'A':
            compiled = CompiledCode(file)
        elif choice.upper() == 'M':
            compiled1 = CompiledCode(file)
            file = file.removesuffix("l") + "a"
            compiled2 = CompiledAssembly(file)



if __name__ == '__main__':
    main()

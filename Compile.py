from CompileAssembly import CompiledAssembly

def main():
    file = input("What file would you like to compile?\n")
    
    valid_input = False
    choice = ''
    while not valid_input:
        choice = input("\nWhat would you like to compress the file to?\nMachine code '.5b' (m)\n")
        if choice.upper() == 'M':
            valid_input = True
        else:
            print("Invalid input")
    
    if choice.upper() == 'M':
        compiled = CompiledAssembly(file)

if __name__ == '__main__':
    main()
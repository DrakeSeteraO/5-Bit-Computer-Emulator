from datetime import date



def main():
    version_num = input("New version number:")
    today = date.today()
    
    update_files = [
        "Compile.py",
        "CompileAssembly.py",
        "CompileBase5.py",
        "CompileCode.py",
        "Computer.py",
        "main.py",
        "CodeLanguageBackEnd/Conditional.py",
        "CodeLanguageBackEnd/Mathematics.py",
        "CodeLanguageBackEnd/Print.py",
        "CodeLanguageBackEnd/Variable.py",
        "UnitTests/ComputerUnitTest.py",
        "UnitTests/CodeLanguageUnitTests/VariableUnitTest.py",
        "UnitTests/CodeLanguageUnitTests/MathUnitTest.py"]
    
    for file in update_files:
        locations = find_locations(file, ["Date: ","Version: "])
        
        
        if locations is None:
            print(f"There was an error with file: {file}")
        else:
            lines = locations[0]
            lines[locations[1][0]] = f"Date: {today.month}/{today.day}/{today.year}\n"
            lines[locations[1][1]] = f"Version: {version_num}\n"
        
        with open(file, "w") as cur_file:
            cur_file.writelines(lines)



def find_locations(file: str, identifiers: list[str]) -> list[int]:
    step = 0
    output = list()
    with open(file, "r") as cur_file:
        lines = cur_file.readlines()
        
        for l in range(len(lines)):
            
            if lines[l].find(identifiers[step]) != -1:
                output.append(l)
                step += 1
                
                if step == 2:
                    return lines, output
    
                
            
if __name__ == '__main__':
    main()
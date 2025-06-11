"""File contains Math functions for 5 Bit Language

Author: Drake Setera

Date: 6/11/2025

Version: 3.0.0
"""



from CodeLanguageBackEnd.Variable import *



def get_var(var: Variable, node = False) -> str:
    """Gets value stored at variable

    Args:
        var (Variable): variable or value to get data
        node (bool, optional): If function is inside of Math Tree. Defaults to False.

    Raises:
        ValueError: If value is out of bounds

    Returns:
        str: assembly to get value
    """


    if not node:
        if isinstance(var, Variable):
            return var.get_var()

        elif isinstance(var, int):
            if var < 0 or var > 31:
                raise ValueError
            else:
                return f'INSERT {var};'

        elif isinstance(var, str):
            return f'INSERT {var};'
    else:
        return var



def ADD(var_a: Variable, var_b: Variable, node = False) -> str:
    """Function to add two variables together

    Args:
        var_a (Variable): Variable or value A
        var_b (Variable): Variable or value B
        node (bool, optional): If function is inside of Math Tree. Defaults to False.

    Returns:
        str: Assembly to add var_a and var_b
    """
    return f"{get_var(var_b, node)} REG B; {get_var(var_a, node)} REG A; ADD; REG C;"



def NOT(var_a: Variable, node = False) -> str:
    """Function to not a variable

    Args:
        var_a (Variable): Variable or value A
        node (bool, optional): If function is inside of Math Tree. Defaults to False.

    Returns:
        str: Assembly to not var_a
    """
    return f"{get_var(var_a, node)} REG A; NOT; REG C;"



def OR(var_a: Variable, var_b: Variable, node = False) -> str:
    """Function to bitwise OR two variables together

    Args:
        var_a (Variable): Variable or value A
        var_b (Variable): Variable or value B
        node (bool, optional): If function is inside of Math Tree. Defaults to False.

    Returns:
        str: Assembly to bitwise OR var_a and var_b
    """
    return f"{get_var(var_b, node)} REG B; {get_var(var_a, node)} REG A; OR; REG C;"



def XOR(var_a: Variable, var_b: Variable, node = False) -> str:
    """Function to bitwise XOR two variables together

    Args:
        var_a (Variable): Variable or value A
        var_b (Variable): Variable or value B
        node (bool, optional): If function is inside of Math Tree. Defaults to False.

    Returns:
        str: Assembly to bitwise XOR var_a and var_b
    """
    return f"{get_var(var_b, node)} REG B; {get_var(var_a, node)} REG A; XOR; REG C;"



def RSHIFT(var_a: Variable, node = False) -> str:
    """Function to right shift a variable

    Args:
        var_a (Variable): Variable or value A
        node (bool, optional): If function is inside of Math Tree. Defaults to False.

    Returns:
        str: Assembly to right shift var_a
    """
    return f"{get_var(var_a, node)} REG A; >>; REG C;"



def AND(var_a: Variable, var_b: Variable, node = False) -> str:
    """Function to bitwise AND two variables together

    Args:
        var_a (Variable): Variable or value A
        var_b (Variable): Variable or value B
        node (bool, optional): If function is inside of Math Tree. Defaults to False.

    Returns:
        str: Assembly to bitwise AND var_a and var_b
    """
    return f"{NOT(var_b, node)} REG B; {NOT(var_a, node)} REG A; OR; REG C; REG A; NOT; REG C;"



def SUB(var_a: Variable, var_b: Variable, node = False) -> str:
    """Function to subtract two variables together

    Args:
        var_a (Variable): Variable or value A
        var_b (Variable): Variable or value B
        node (bool, optional): If function is inside of Math Tree. Defaults to False.

    Returns:
        str: Assembly to subtract var_b from var_a
    """
    return f"{get_var(var_b, node)} REG A; NOT; REG C; REG A; INSERT 1; REG B; ADD; REG C; REG B; {get_var(var_a, node)} REG A; ADD; REG C;"



class Node:
    """Node that stores part of math equation
    """



    def parenthesis_split(self, equation: str) -> list[str, str, str]:
        """Attempts to locate parenthesis

        Args:
            equation (str): equation to find parenthesis in

        Returns:
            list[str, str, str]: left side of equation, math symbol, right side of equation
        """


        found_left = False
        found_right = False
        layer = 0
        L_index = -1
        R_index = -1

        i = 0
        while i < len(equation) and not found_right:
            if equation[i] == '(' and not found_left:
                found_left = True
                layer = 1
                L_index = i

            elif equation[i] == '(':
                layer += 1

            elif equation[i] == ')':
                layer -= 1   

            if found_left and layer == 0 and not found_right:
                found_right = True
                R_index = i

            i += 1

        if L_index > 0:
            return [equation[:L_index-1], equation[L_index-1], equation[L_index:]]
        elif L_index == 0 and R_index == len(equation) - 1:
            return [equation[1:-1]]
        elif L_index == 0:
            right = equation[R_index+2:]
            if equation[R_index+2] == '(' and equation[-1] == ')':
                right = equation[R_index+3:-1]

            return [equation[1:R_index], equation[R_index+1], right]
        elif L_index == -1:
            return [equation]



    def split_symbol(self, equation: str, symbol: str) -> list[str, str, str]:
        """Attempts to split equation

        Args:
            equation (str): equation to split
            symbol (str): symbol to try and split

        Returns:
            list[str, str, str]: left side of equation, math symbol, right side of equation
        """


        parts = equation.split(symbol)
        if len(parts) == 1:
            return parts

        elif len(parts) == 2:
            return [parts[0], symbol, parts[1]]

        elif len(parts) > 2:
            right = parts[1]
            for i in range(2,len(parts)):
                right += symbol + parts[i]
            return [parts[0], symbol, right]



    def determine_split(self, equation: str, symbols: list) -> list[str, str, str]:
        """Determines symbols to split equation by

        Args:
            equation (str): equation to split
            symbols (list): symbols to try and split equation by

        Returns:
            list[str, str, str]: left side of equation, math symbol, right side of equation
        """


        if len(symbols) == 0:
            return [equation]

        parts = self.split_symbol(equation,symbols[0])

        if len(parts) == 3:
            return parts
        elif len(parts) == 1:
            return self.determine_split(equation, symbols[1:])



    def split_equation(self, equation: str) -> list[str, str, str]:
        """Splits equation if possible

        Args:
            equation (str): equation to split

        Returns:
            list[str, str, str]: left side of equation, math symbol, right side of equation
        """


        equation = equation.replace(" ","").replace("\n","")
        parts = self.parenthesis_split(equation)

        if len(parts) == 3:
            return parts

        elif len(parts) == 1:
            equation = parts[0]
            return self.determine_split(equation, ['+','-','*','/','|','&','^','!'])



    def __init__(self, equation: str, var_type: str, address: str):
        self.var_type = var_type
        self.address = address

        parts = self.split_equation(equation)
        self.symbol = None
        self.left = None
        self.right = None

        if len(parts) == 1:
            self.var = parts[0]

        elif len(parts) == 3:
            self.left = Node(parts[0], var_type, address)
            self.symbol = parts[1]
            self.right = Node(parts[2], var_type, address)



    def convert_val(self, val: str, variables: dict[str, Variable]) -> str:
        """Verifies value 
        
        Args:
            val (str): value to verify
            variables (dict[str, Variable]): Dictionary containing program variables

        Returns:
            str: verified value
        """


        if val[0] == "'":
            return val[1:-1]
        if val.isalpha():
            return variables[val]
        else:
            return val



    def get_address_amount(self, local: int) -> int:
        """Calculates the required number of RAM addresses to complete calculations

        Args:
            local (int): Local RAM address value

        Returns:
            int: Number of RAM addresses needed to complete calculations 
        """


        self.address_shift = -1

        if self.left is None and self.right is None:
            return 0
        if self.left is None:
            return self.right.get_address_amount(local)
        if self.right is None:
            return self.left.get_address_amount(local)

        if local <= 0:
            local = 1
        self.address_shift = local - 1

        left_global = self.left.get_address_amount(local)
        right_global = self.right.get_address_amount(local+1)

        return max(left_global, right_global, local)



    def get_math_assembly(self, variables: dict[str, Variable]) -> str:
        """Gets assembly to perform math calculations

        Args:
            variables (dict[str, Variable]): All declared variables in program

        Returns:
            str: Assembly to perform all math calculations
        """


        if self.left is None and self.right is None:
            return get_var(self.convert_val(self.var, variables))
        if self.right is None:
            return self.left.get_math_assembly(variables)
        if self.left is None:
            return self.right.get_math_assembly(variables)

        temp_address = self.get_temp_address()
        set_left_assembly = f"{self.left.get_math_assembly(variables)} REG D; INSERT {temp_address[:5]}; REG F; INSERT {temp_address[5:]}; REG E; SET;"
        get_left_assembly = f"INSERT {temp_address[:5]}; REG F; INSERT {temp_address[5:]}; REG E; GET;"

        return F"{set_left_assembly} {self.convert_symbol(get_left_assembly, self.right.get_math_assembly(variables))}"



    def convert_symbol(self, left: str, right: str) -> str:
        """Gets assembly based on math symbol

        Args:
            left (str): assembly to get left val
            right (str): assembly to get right val

        Returns:
            str: assembly to perform calculation
        """


        if self.symbol == '+':
            return ADD(left, right, True)
        if self.symbol == '-':
            return SUB(left, right, True)
        if self.symbol == '*':
            return None
        if self.symbol == '/':
            return None
        if self.symbol == '|':
            return OR(left, right, True)
        if self.symbol == '&':
            return AND(left, right, True)



    def get_temp_address(self) -> str:
        """Gets temporary RAM address to store variable

        Returns:
            str: Temporary RAM address
        """


        temp_address = bin(int(self.address, 2) + self.address_shift).removeprefix('0b').zfill(10)
        return temp_address



    def get_tree(self) -> list[list]:
        """Gets a list representation of the Math Tree

        Returns:
            list: list representation of Math Tree
        """


        if self.left is None and self.right is None:
            return self.var
        if self.left is None:
            return [self.symbol, self.right.get_tree()]
        if self.right is None:
            return [self.left.get_tree(), self.symbol]
        return [self.left.get_tree(), self.symbol, self.right.get_tree()]



class MathTree:
    """Binary tree to determine order of operations of calculations
    """


    def __init__(self, equation: str, address: str, var_type: str):
        if len(address) != 10:
            raise ValueError
        else:
            self.address = address

        self.var_type = var_type
        self.root = Node(equation, var_type, address)



    def get_address_size(self) -> int:
        """Gets the number of addresses required to calculate equation

        Returns:
            int: Number of addresses required
        """
        return self.root.get_address_amount(0)



    def get_assembly(self, variables: dict[str, Variable]) -> str:
        """Gets the assembly to calculate equation

        Args:
            variables (dict[str, Variable]): All declared variables in the program

        Returns:
            str: assembly to calculate equation
        """
        return self.root.get_math_assembly(variables)



    def print_tree(self):
        """Prints representation of Math Tree
        """
        print(self.root.get_tree())

# n = MathTree("((1+2)-(1+1))+((1+2)+(3+4))", '0000000000', 'int')
# print(n.get_address_size())
# print(n.get_assembly())
# n.print_tree()
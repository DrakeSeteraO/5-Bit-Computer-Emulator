"""File contains Conditional functions for 5 Bit Language

Author: Drake Setera

Date: 6/20/2025

Version: 3.1.0
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



def EQUAL(var_a: Variable, var_b: Variable, node = False) -> str:
    return f"{NOT_EQUAL(var_a, var_b, node)} REG A; INSERT 00001; REG B; XOR; REG C;"



def NOT_EQUAL(var_a: Variable, var_b: Variable, node = False) -> str:
    return f"{get_var(var_b, node)} REG H; {get_var(var_a, node)} REG G; INSERT 1; IF; INSERT 0;"
    


def LESS_THAN(var_a: Variable, var_b: Variable, node = False) -> str:
    return f"{SUB(var_a, var_b, node)} REG A; >>; REG C; REG A; >>; REG C; REG A; >>; REG C; REG A; >>; REG C;"



def GREATER_THAN(var_a: Variable, var_b: Variable, node = False) -> str:
    return f"{SUB(var_a, var_b, node)} REG A; NOT; REG C; REG A; >>; REG C; REG A; >>; REG C; REG A; >>; REG C; REG A; >>; REG C;"



def LESS_THAN_OR_EQUAL(var_a: Variable, var_b: Variable, node = False) -> str:
    return LESS_THAN(var_a, get_var(var_b) + "REG A; INSERT 1; REG B; ADD; REG C;", node)



def GREATER_THAN_OR_EQUAL(var_a: Variable, var_b: Variable, node = False) -> str:
    return f"{SUB(var_a, var_b, node)} REG A; NOT; REG C; REG A; >>; REG C; REG A; >>; REG C; REG A; >>; REG C; REG A; >>; REG C;"
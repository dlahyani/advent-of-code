
from functools import lru_cache
from operator import eq
from typing import Literal


def parse_equation(equation: str) -> tuple[int, tuple[int, ...]]:
    res_str, factors_str = equation.split(": ")
    factors =  tuple(int(f) for f in factors_str.split(" "))
    return int(res_str), factors


def load_equations(input_file: str) -> list[tuple[int, tuple[int, ...]]]:
    with open(input_file, "r") as f:
        return [parse_equation(l.strip()) for l in f.readlines()]
    
Operator = Literal['+', '*']
    
@lru_cache(maxsize=None)
def gen_operators(n: int) -> list[tuple[Operator, ...]]:
    num_strings = 2**n  # Total number of strings
    results: list[tuple[Operator, ...]] = []
    
    for i in range(num_strings):
        binary_representation = bin(i)[2:].zfill(n)  # Get binary string padded to length n
        custom_representation = binary_representation.replace('0', '+').replace('1', '*')
        results.append(tuple(custom_representation))  # type: ignore
    
    return results

def evaluate_equation(equation: tuple[int, tuple[int, ...]], operators: tuple[Operator, ...]) -> int:
    _, factors = equation
    result = factors[0]
    for i, operator in enumerate(operators):
        if operator == '+':
            result += factors[i+1]
        elif operator == '*':
            result *= factors[i+1]
        else:
            raise ValueError(f"Unknown operator {operator}")
    
    return result
    
def equation_has_solution(equation: tuple[int, tuple[int, ...]]) -> bool:
    res, factors = equation
    possible_operators = gen_operators(len(factors) - 1)
    for operators in possible_operators:
        if evaluate_equation(equation, operators) == res:
            return True
        
    return False
    

equations = load_equations("2024/07/input.txt")
valid_equations = [eq for eq in equations if equation_has_solution(eq)]
s = sum([eq[0] for eq in valid_equations])
print(s)


   

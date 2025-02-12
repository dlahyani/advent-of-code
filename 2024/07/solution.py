
from functools import lru_cache
from itertools import product

def parse_equation(equation: str) -> tuple[int, tuple[int, ...]]:
    res_str, factors_str = equation.split(": ")
    factors =  tuple(int(f) for f in factors_str.split(" "))
    return int(res_str), factors


def load_equations(input_file: str) -> list[tuple[int, tuple[int, ...]]]:
    with open(input_file, "r") as f:
        return [parse_equation(l.strip()) for l in f.readlines()]
    
@lru_cache(maxsize=None)
def gen_operators(n: int, allowed_ops: tuple[str]) -> list[tuple[str, ...]]:
    return [tuple(comb) for comb in product(allowed_ops, repeat=n)]

def evaluate_equation(equation: tuple[int, tuple[int, ...]], operators: tuple[str, ...]) -> int:
    _, factors = equation
    result = factors[0]
    for i, operator in enumerate(operators):
        if operator == '+':
            result += factors[i+1]
        elif operator == '*':
            result *= factors[i+1]
        elif operator == '||':
            result = int(str(result) + str(factors[i+1]))
        else:
            raise ValueError(f"Unknown operator {operator}")
    
    return result
    
def equation_has_solution(equation: tuple[int, tuple[int, ...]], allowed_ops: tuple[str, ...]) -> bool:
    res, factors = equation
    possible_operators = gen_operators(len(factors) - 1, allowed_ops)
    for operators in possible_operators:
        if evaluate_equation(equation, operators) == res:
            return True
        
    return False
    

equations = load_equations("2024/07/input.txt")

# Part 1
OPERATORS = ('+', '*')
valid_equations = [eq for eq in equations if equation_has_solution(eq, OPERATORS)]
s = sum([eq[0] for eq in valid_equations])
print(s)


# Part 2
OPERATORS = ('+', '*', '||')
valid_equations = [eq for eq in equations if equation_has_solution(eq, OPERATORS)]
s = sum([eq[0] for eq in valid_equations])
print(s)

   

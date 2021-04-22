from typing import Tuple


def apply_operator(lv, rv, operator) -> float:
    return lv + rv if operator == "+" else lv * rv

def log(*kargs):
    pass


def eval_expression(exp_str: str, start: int = 0) -> Tuple[float, int]:
    log(f"==> eval_expression(\"{exp_str}\", {start})")

    exp_value = 0
    cur_operator = '+'
    cur_term = None
    ptr = start
    while ptr < len(exp_str):
        c = exp_str[ptr]
        ptr += 1
        if c == '(':
            v, p = eval_expression(exp_str, ptr)
            exp_value = apply_operator(exp_value, v, cur_operator)
            ptr += p
        elif c == ')':
            break
        elif c in "0123456789":
            cur_term = c
        elif c in '+*':
            if cur_term:
                v = float(cur_term)
                exp_value = apply_operator(exp_value, v, cur_operator)
                cur_term = None

            cur_operator = c

    if cur_term:
        v = float(cur_term)
        exp_value = apply_operator(exp_value, v, cur_operator)

    log(f"<== eval_expression(\"{exp_str}\", {start}) = {exp_value}")
    return exp_value, (ptr - start)


def modify_expression(exp_str: str, start: int = 0) -> Tuple[str, int]:
    log(f"==> modify_expression(\"{exp_str}\", {start})")
    exp = ""
    operands = []

    ptr = start
    while ptr < len(exp_str):
        c = exp_str[ptr]
        ptr += 1
        if c == '(':
            sub_exp, p = modify_expression(exp_str, ptr)
            operands.append(f"({sub_exp})")
            ptr += p
        elif c == ')':
            break
        elif c == "*":
            exp += f"{operands[0]} * "
            operands = []
        elif c in "0123456789":
            operands.append(c)

        if len(operands) == 2:
            operands = [f"({operands[0]} + {operands[1]})"]

    exp += operands[0]
    log(f"<== modify_expression: {exp}")
    return exp, (ptr - start)


if __name__ == "__main__":
    expressions = [line[:-1] for line in open("2020/18/input.txt", "r").readlines()]

    # Part 1
    s = sum([eval_expression(e)[0] for e in expressions])
    print(f"Sum of expressions: {s}")

    # Part 2
    modified_expressions = [modify_expression(e)[0] for e in expressions]
    s = sum([eval_expression(e)[0] for e in modified_expressions])
    print(f"Sum of expressions: {s}")

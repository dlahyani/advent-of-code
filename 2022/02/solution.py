def score_for_round(opponent, you):
    return (ord(you) - ord("A") + 1) + (
        3 if opponent == you else 6 if (opponent, you) in (("A", "B"), ("B", "C"), ("C", "A")) else 0
    )


### Part 1
def instruction_to_round(l: str) -> tuple[str, str]:
    t = str.maketrans({"X": "A", "Y": "B", "Z": "C"})
    return l.translate(t).split()


rounds = [instruction_to_round(l) for l in open("2022/02/input.txt").readlines()]
total_score = sum([score_for_round(*r) for r in rounds])
print(f"Total score: {total_score}")


### Part 2
def instruction_to_round(l: str) -> tuple[str, str]:
    op, res = l.split()
    return (
        (op, op)
        if res == "Y"
        else ((op, {"A": "C", "B": "A", "C": "B"}[op]) if res == "X" else (op, {"A": "B", "B": "C", "C": "A"}[op]))
    )


rounds = [instruction_to_round(l) for l in open("2022/02/input.txt").readlines()]
total_score = sum([score_for_round(*r) for r in rounds])
print(f"Total score: {total_score}")

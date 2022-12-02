instructions = [l.strip() for l in open("2022/02/input.txt")]

### Part 1
instruction_to_score = {
    "A X": 1+3, "A Y": 2+6, "A Z": 3+0,
    "B X": 1+0, "B Y": 2+3, "B Z": 3+6,
    "C X": 1+6, "C Y": 2+0, "C Z": 3+3,
}
total_score = sum([instruction_to_score[i] for i in instructions])
print(f"Total score: {total_score}")

### Part 2
instruction_to_score = {
    "A X": 3+0, "A Y": 1+3, "A Z": 2+6,
    "B X": 1+0, "B Y": 2+3, "B Z": 3+6,
    "C X": 2+0, "C Y": 3+3, "C Z": 1+6,
}
total_score = sum([instruction_to_score[i] for i in instructions])
print(f"Total score: {total_score}")
from functools import reduce

calories_carried_per_elf = sorted(
    reduce(
        lambda c, l: c + [0] if l == "\n" else c[:-1] + [c[-1] + int(l)],
        open("2022/01/input.txt"),
        [0],
    ),
    reverse=True,
)

### Part 1
print(f"Max calories: {calories_carried_per_elf[0]}")

### Part 2
print(f"Sum of top 3 calories carrying elves: {sum(calories_carried_per_elf[0:3])}")

from collections import Counter

# Common
with open("2024/01/input.txt", "r") as f:
    l1, l2 = zip(*((int(r[0]), int(r[1])) for r in (l.split("   ") for l in f)))

#### Part 1    
sum_diffs = sum(abs(a - b) for a, b in zip(sorted(l1), sorted(l2)))
print("Part 1: The total distance between your lists is:", sum_diffs)

    
#### Part 2
l2_counter = Counter(l2)
sum_counts = sum(a * l2_counter.get(a, 0) for a in l1)
print("Part 2: The lists total similarity score is:", sum_counts)

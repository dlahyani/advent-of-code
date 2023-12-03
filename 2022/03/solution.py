def get_item_priority(item: str) -> int:
    return 1 + ord(item) - (ord("a") if item >= "a" else ord("A") - 26)


### Part 1
rucksacks = [l.strip() for l in open("2022/03/input.txt")]
compartments = [(r[: len(r) // 2], r[len(r) // 2 :]) for r in rucksacks]
items = [set(c1).intersection(c2).pop() for c1, c2 in compartments]
priorities = [get_item_priority(i) for i in items]
print(f"Sum of priorities: {sum(priorities)}")

### Part 2
badges = []
for i in range(0, len(rucksacks), 3):
    r1, r2, r3 = rucksacks[i : i + 3]
    badges.append(set(r1).intersection(set(r2)).intersection(set(r3)).pop())
badge_priorities = [get_item_priority(b) for b in badges]
print(f"Sum of badges priorities: {sum(badge_priorities)}")

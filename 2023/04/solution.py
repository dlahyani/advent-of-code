import re
from collections import defaultdict

LINE_PATTERN = re.compile(r"^Card\s+(\d+):((\s+\d+)+)\s+\|((\s+\d+)+)$")


def parse_line(l: str) -> tuple[int, set[int], set[int]]:
    m = LINE_PATTERN.match(l.strip())
    assert m is not None
    card_id = int(m.group(1))
    winning_numbers = set(int(n) for n in m.group(2).split())
    numbers = set(int(n) for n in m.group(4).split())
    return card_id, winning_numbers, numbers


def part1():
    with open("input.txt", "r") as f:
        parsed_lines = list(map(parse_line, f))

    total_points = 0
    for card_id, winning_numbers, numbers in parsed_lines:
        matches = len(winning_numbers.intersection(numbers))
        card_points = 2 ** (matches - 1) if matches > 0 else 0
        total_points += card_points

    print(f"Total points: {total_points}")


def part2():
    card_counters: dict[int, int] = defaultdict(lambda: 1)

    with open("input.txt", "r") as f:
        parsed_lines = list(map(parse_line, f))

    for card_id, winning_numbers, numbers in parsed_lines:
        count = card_counters[card_id]
        for i in range(count):
            matches = len(winning_numbers.intersection(numbers))
            for j in range(card_id + 1, card_id + matches + 1):
                card_counters[j] += 1

    print(f"Total cards scratched: {sum(card_counters.values())}")


part1()
part2()

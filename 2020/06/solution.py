from functools import reduce
from typing import Callable


def _get_group_answers_counter(group_answers: str, reducer: Callable) -> int:
    individuals_answers = [set(p) for p in group_answers.split("\n")]
    return len(reduce(reducer, individuals_answers))


def get_group_answers_counter_union(group_answers: str) -> int:
    return _get_group_answers_counter(group_answers, lambda g, a: g.union(a))


def get_group_answers_counter_intersection(group_answers: str) -> int:
    return _get_group_answers_counter(group_answers, lambda g, a: g.intersection(a))


if __name__ == "__main__":
    grouped_answers = open("2020/06/input.txt", "r").read().split("\n\n")

    # Part 1
    part1_counters_sum = sum(map(get_group_answers_counter_union, grouped_answers))
    print(f"Part 1 counters sum: {part1_counters_sum}")

    # Part 2
    part2_counters_sum = sum(map(get_group_answers_counter_intersection, grouped_answers))
    print(f"Part 2 counters sum: {part2_counters_sum}")

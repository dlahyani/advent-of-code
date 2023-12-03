from typing import NamedTuple
from collections import defaultdict
from math import prod

ADJACENCY_OFFSETS: list[tuple[int, int]] = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


def get_adjacent_symbol(
    rows: list[str], row: int, col: int
) -> tuple[str, tuple[int, int]] | None:
    indexes_to_check = filter(
        lambda p: 0 <= p[0] < len(rows) and 0 <= p[1] < len(rows[0]),
        [(row + offset[0], col + offset[1]) for offset in ADJACENCY_OFFSETS],
    )
    for r, c in indexes_to_check:
        cur_char = rows[r][c]
        if not cur_char.isdigit() and cur_char != ".":
            return cur_char, (r, c)

    return None


class PartNumberDetails(NamedTuple):
    part_number: int
    position: tuple[int, int]
    adjacent_symbol: str
    adjacent_symbol_position: tuple[int, int]


def find_part_numbers(rows: list[str]) -> list[PartNumberDetails]:
    part_numbers: list[PartNumberDetails] = []
    for i in range(len(rows)):
        row = rows[i]

        cur_num: int = 0
        cur_num_position: tuple[int, int] | None = None
        adjacent_symbol_info: tuple[str, tuple[int, int]] | None = None
        for j in range(len(row)):
            cur_char = row[j]
            if cur_char.isdigit():
                cur_num = cur_num * 10 + int(cur_char)
                cur_num_position = cur_num_position or (i, j)
                adjacent_symbol_info = adjacent_symbol_info or get_adjacent_symbol(
                    rows, i, j
                )
                continue
            elif adjacent_symbol_info is not None:
                part_numbers.append(
                    PartNumberDetails(
                        cur_num,
                        cur_num_position,
                        adjacent_symbol_info[0],
                        adjacent_symbol_info[1],
                    )
                )

            cur_num = 0
            cur_num_position = None
            adjacent_symbol_info = None

    return part_numbers


def main():
    with open("input.txt", "r") as f:
        rows = [r.replace("\n", ".") for r in f]

    part_numbers = find_part_numbers(rows)
    part_1(part_numbers)
    part_2(part_numbers)


def part_1(part_numbers: list[PartNumberDetails]) -> None:
    print("Part 1:", sum([p.part_number for p in part_numbers]))


def part_2(part_numbers: list[PartNumberDetails]) -> None:
    gear_pos_to_part_numbers: dict[tuple[int, int], list[int]] = defaultdict(list)
    for p in part_numbers:
        if p.adjacent_symbol != "*":
            continue
        gear_pos_to_part_numbers[p.adjacent_symbol_position].append(p.part_number)

    gear_powers = [
        prod(gear_pos_to_part_numbers[p])
        for p in gear_pos_to_part_numbers
        if len(gear_pos_to_part_numbers[p]) == 2
    ]

    print("Part 2:", sum(gear_powers))


if __name__ == "__main__":
    main()

from collections import Counter
from functools import cache
from itertools import product
from typing import Collection, Dict, List, Tuple

ACTIVE = "#"
INACTIVE = "."

Coords = Tuple[int]
PocketSpace = Dict[Coords, str]

# A multi-dimensional array of neighboring offsets.
NEIGHBORING_OFFSETS: Dict[int, Tuple[Coords]] = {i: tuple(product([-1, 0, 1], repeat=i)) for i in range(3, 5)}


@cache
def get_neighbors(point: Coords) -> set[Coords]:
    dim = len(point)
    z = (0,) * dim
    neighbors = {tuple(sum(i) for i in zip(point, no)) for no in NEIGHBORING_OFFSETS[dim] if no != z}
    return neighbors


def init_pocket_space(lines: List[str], dimension: int) -> Dict[Tuple[int], str]:
    pocket_space = {}
    for y in range(len(lines)):
        for x in range(len(lines[y].strip())):
            if lines[y][x] == ACTIVE:
                coords = (x, y) + (0,) * (dimension - 2)
                pocket_space[coords] = ACTIVE

    return pocket_space


def simulate_cycle(pocket_space: PocketSpace) -> PocketSpace:
    neighbors_counter = Counter()
    for c in pocket_space:
        neighbors_counter.update(get_neighbors(c))

    new_pocket_space = {}
    for c, n in neighbors_counter.items():
        c_state = pocket_space.get(c, INACTIVE)
        if c_state == ACTIVE and n in [2, 3]:
            new_pocket_space[c] = ACTIVE
        elif c_state == INACTIVE and n == 3:
            new_pocket_space[c] = ACTIVE

    return new_pocket_space


def simulate_multiple_cycles(pocket_space: PocketSpace, count: int) -> PocketSpace:
    for i in range(count):
        pocket_space = simulate_cycle(pocket_space)
    return pocket_space


if __name__ == "__main__":
    lines = open("2020/17/input.txt", "r").readlines()

    # Part 1
    pocket_space = init_pocket_space(lines, 3)
    pocket_space = simulate_multiple_cycles(pocket_space, 6)
    active_cubes = list(filter(lambda c: pocket_space[c] == ACTIVE, pocket_space))
    print(f"Active cubes after 6 cycles: {len(active_cubes)}")

    pocket_space = init_pocket_space(lines, 4)
    pocket_space = simulate_multiple_cycles(pocket_space, 6)
    active_cubes = list(filter(lambda c: pocket_space[c] == ACTIVE, pocket_space))
    print(f"Active cubes after 6 cycles: {len(active_cubes)}")

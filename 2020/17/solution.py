from functools import cache
from itertools import product
from typing import Dict, List, Tuple

ACTIVE = "#"
INACTIVE = "."

# A multi-dimensional array of neighboring offsets.
NEIGHBORING_OFFSETS: Dict[int, Tuple[Tuple[int]]] = {
    i: tuple(product([-1, 0, 1], repeat=i)) for i in range(3, 5)
}

@cache
def get_neighbors(point: tuple) -> set:
    dim = len(point)
    z = (0,)*dim
    neighbors = {
        tuple(sum(i) for i in zip(point, no)) for no in NEIGHBORING_OFFSETS[dim] if no != z
    }
    return neighbors


PocketSpace = Dict[Tuple[int], str]


def simulate_cycle(pocket_space: PocketSpace) -> PocketSpace:
    new_pocket_space = pocket_space.copy()
    for point, cube_state in pocket_space.items():
        active_neighbors = list(filter(
            lambda n: n in pocket_space and pocket_space[n] == ACTIVE,
            get_neighbors(point)
        ))

        if cube_state == ACTIVE and len(active_neighbors) not in [2, 3]:
            set_cube_state(new_pocket_space, point, INACTIVE)
        elif cube_state == INACTIVE and len(active_neighbors) == 3:
            set_cube_state(new_pocket_space, point, ACTIVE)

    return new_pocket_space

def set_cube_state(pocket_space, point, state):
    pocket_space[point] = state
    for n in get_neighbors(point):
        if not n in pocket_space:
            pocket_space[n] = INACTIVE


def print_pocket_space(pocket_space: dict):
    z_planes = {}
    for point, cube_state in pocket_space.items():
        x, y, z = point
        if not z in z_planes:
            z_planes[z] = {}
        
        z_planes[z][(y, x)] = cube_state
    
    for z in sorted(z_planes.keys()):
        plane = z_planes[z]
        print(f"z={z}")
        print_z_plane(plane)
        print("\n")
        
    print("\n")

def print_z_plane(plane: dict):  
    sorted_keys = sorted(plane.keys())
    min_y = sorted_keys[0][0]
    max_y = sorted_keys[-1][0]
    min_x = min([p[1] for p in sorted_keys])
    max_x = max([p[1] for p in sorted_keys])
    
    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            line = line + (plane[(y, x)] if (y, x) in plane else ".")
        print(line)

def init_pocket_space(lines: List[str], dimension: int) -> Dict[Tuple[int], str]:
    pocket_space = {}
    for y in range(len(lines)):
        for x in range(len(lines[y].strip())):
            coords = (x, y) + (0,) * (dimension - 2)
            set_cube_state(pocket_space, coords, lines[y][x])

    return pocket_space

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

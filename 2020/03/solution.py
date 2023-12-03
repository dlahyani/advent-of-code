from functools import reduce
from typing import List, Optional, Tuple

SEGMENT_WIDTH = 31
MAP_TREE_MARK = "#"
SLOPES = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]


def count_slope_trees(road_map: List[str], slope: Tuple[int, int]) -> int:
    """
    Slides down the road, starting at position `(0, 0)` in `road_map` and moving forward in steps
    as defined by `slope` until reaching the bottom of the. On the way down the function counts
    the number of trees encountered and return it.
    """
    trees = 0

    try:
        cur_pos = (0, 0)
        while True:
            x, y = cur_pos[0] % SEGMENT_WIDTH, cur_pos[1]
            trees += int(road_map[y][x] == MAP_TREE_MARK)
            cur_pos = (cur_pos[0] + slope[0], cur_pos[1] + slope[1])
    except IndexError:
        return trees


if __name__ == "__main__":
    lines = open("2020/03/input.txt", "r").readlines()

    # Part 1
    trees_encountered = count_slope_trees(lines, SLOPES[1])
    print(f"Trees encountered using slope {SLOPES[1]}: {trees_encountered}")

    # Part 2
    product = reduce(lambda a, b: a * b, map(lambda slope: count_slope_trees(lines, slope), SLOPES))
    print(f"Product of trees encountered in each slope: {product}")

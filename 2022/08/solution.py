from functools import reduce
from itertools import chain

TreeMapEntry = list[int]
TreeMap = list[list[int]]

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
DIRECTIONS = (UP, RIGHT, DOWN, LEFT)
STEP_IN_DIRECTION = {UP: (-1, 0), RIGHT: (0, 1), DOWN: (1, 0), LEFT: (0, -1)}


def in_bounds(tree_map: TreeMap, row: int, col: int) -> bool:
    return row >= 0 and row < len(tree_map) and col >= 0 and col < len(tree_map[0])


tree_map = [[int(t) for t in list(l.strip())] for l in open("2022/08/input.txt").readlines()]
h, w = len(tree_map), len(tree_map[0])
map_cords = tuple(chain.from_iterable([[(r, c) for c in range(w)] for r in range(h)]))


### Part 1
def is_tree_visible_from_direction(tree_map: TreeMap, row: int, col: int, direction: int) -> bool:
    step = STEP_IN_DIRECTION[direction]
    n_row, n_col = row + step[0], col + step[1]
    while in_bounds(tree_map, n_row, n_col):
        if tree_map[row][col] <= tree_map[n_row][n_col]:
            return False
        n_row, n_col = n_row + step[0], n_col + step[1]
    return True


def is_tree_visible(tree_map: TreeMap, row: int, col: int) -> bool:
    return any(map(lambda d: is_tree_visible_from_direction(tree_map, row, col, d), DIRECTIONS))


visible_trees = list(filter(lambda p: is_tree_visible(tree_map, p[0], p[1]), map_cords))
print(f"Total visible trees: {len(visible_trees)}")


### Part 2
def visible_trees_in_direction(tree_map: TreeMap, row: int, col: int, direction: int) -> int:
    step = STEP_IN_DIRECTION[direction]
    n_row, n_col = row + step[0], col + step[1]
    visible_trees = 0
    while in_bounds(tree_map, n_row, n_col):
        visible_trees += 1
        if tree_map[row][col] <= tree_map[n_row][n_col]:
            break
        n_row, n_col = n_row + step[0], n_col + step[1]
    return visible_trees


def tree_scenic_score(tree_map: TreeMap, row: int, col: int) -> int:
    return reduce(
        lambda x, y: x * y,
        map(lambda d: visible_trees_in_direction(tree_map, row, col, d), DIRECTIONS),
        1,
    )


highest_score = max(map(lambda p: tree_scenic_score(tree_map, p[0], p[1]), map_cords))
print(f"Highest scenic score: {highest_score}")

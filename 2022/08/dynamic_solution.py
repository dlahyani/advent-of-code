from typing import Optional

TreeMapEntry = list[int]
TreeMap = list[list[int]]
MaxHeightMap = list[list[list[int]]]

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


def in_bounds(tree_map: TreeMap, row: int, col: int) -> bool:
    return row >= 0 and row < len(tree_map) and col >= 0 and col < len(tree_map[0])

def find_max_height_in_direction(tree_map: TreeMap, max_heights_map: MaxHeightMap, row: int, col: int, direction: int) -> int:
    step = {UP: (-1, 0), RIGHT: (0, 1), DOWN: (1, 0), LEFT: (0, -1)}[direction]
    n_row, n_col = row + step[0], col + step[1]
    if max_heights_map[row][col][direction] is not None:
        max_height = max_heights_map[row][col][direction]
    elif not in_bounds(tree_map, n_row, n_col):
        max_height = -1
    else:
        max_height = find_max_height_in_direction(tree_map, max_heights_map, n_row, n_col, direction)
    
    max_heights_map[row][col][direction] = max_height
    return max(max_height, tree_map[row][col])

def find_max_heights_in_all_directions(tree_map: TreeMap, max_heights_map: MaxHeightMap, row: int, col: int):
    for d in (UP, RIGHT, DOWN, LEFT):
        find_max_height_in_direction(tree_map, max_heights_map, row, col, d)

def build_max_heights_map(tree_map: TreeMap) -> MaxHeightMap:
    max_heights_map = [[[None, None, None, None] for _ in tree_map[0]] for _ in tree_map]
    for r in range(len(tree_map)):
        for c in range(len(tree_map[0])):
            find_max_heights_in_all_directions(tree_map, max_heights_map, r, c)
    
    return max_heights_map
                
def is_tree_visible_from_direction(tree_map: TreeMap, max_heights_map: MaxHeightMap, row: int, col: int, direction: int) -> bool:
    return tree_map[row][col] > max_heights_map[row][col][direction]

def is_tree_visible_from_outside(tree_map: TreeMap, max_heights_map: MaxHeightMap, row: int, col: int) -> bool:
    return any([is_tree_visible_from_direction(tree_map, max_heights_map, row, col, d) for d in (UP, RIGHT, DOWN, LEFT)])


tree_map = [[int(t) for t in list(l.strip())] for l in open("2022/08/input.txt").readlines()]    
max_heights_map = build_max_heights_map(tree_map)

visible_trees = []
for r in range(len(tree_map)):
    for c in range(len(tree_map[0])):
        if is_tree_visible_from_outside(tree_map, max_heights_map, r, c):
            visible_trees.append((r,c))

print(f"Total visible trees: {len(visible_trees)}")

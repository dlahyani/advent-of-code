from collections import deque
from itertools import product
import string

Grid = list[list[str]]
Cell = tuple[int, int]

neighbors_offsets = ((1, 0), (0, 1), (-1, 0), (0, -1))


def can_move_to_cell(grid: Grid, src: Cell, dst: Cell) -> bool:
    return (
        0 <= dst[0] < len(grid)
        and 0 <= dst[1] < len(grid[0])
        and ord(grid[dst[0]][dst[1]]) <= ord(grid[src[0]][src[1]]) + 1
    )


def get_grid_neighbors(grid: Grid, p: Cell) -> tuple[Cell]:
    return tuple(
        filter(
            lambda c: can_move_to_cell(grid, p, c),
            [(p[0] + o[0], p[1] + o[1]) for o in neighbors_offsets],
        )
    )


def find_shortest_path(grid: Grid, start: tuple[Cell], end: Cell) -> tuple[int, dict[Cell, Cell]]:
    if start == end:
        return 0, {}

    queue = deque(((c, 0) for c in start))
    traceback = {start: None}
    while len(queue) > 0:
        cell, cell_distance = queue.popleft()
        if cell == end:
            return cell_distance, traceback

        for n in get_grid_neighbors(grid, cell):
            if n not in traceback:
                queue.append((n, cell_distance + 1))
                traceback[n] = cell

    # Queue is empty end we never reached the target cell.
    return -1, None


grid = [list(l.strip()) for l in open("2022/12/input.txt")]
grid_indexes = tuple((r, c) for r, c in product(range(len(grid)), range(len(grid[0]))))
start_marker = tuple(filter(lambda gi: grid[gi[0]][gi[1]] == "S", grid_indexes))[0]
end_marker = tuple(filter(lambda gi: grid[gi[0]][gi[1]] == "E", grid_indexes))[0]
grid[start_marker[0]][start_marker[1]] = "a"
grid[end_marker[0]][end_marker[1]] = "z"

start_cells = (start_marker,)
shortest_path_len, traceback = find_shortest_path(grid, start_cells, end_marker)
print(f"Shortest path (len = {shortest_path_len})")

start_cells = tuple((r, c) for r, c in grid_indexes if grid[r][c] == "a")
shortest_path_len, traceback = find_shortest_path(grid, start_cells, end_marker)
print(f"Shortest path (len = {shortest_path_len})")

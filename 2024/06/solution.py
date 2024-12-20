from typing import Literal, NamedTuple, cast

Location = tuple[int, int]
Direction = Literal["^", "v", "<", ">"]
DIRECTIONS: tuple[Direction, ...] = ("^", ">", "v", "<")

class Position(NamedTuple):
    location: Location
    direction: Direction

Path = list[Position]


def get_initial_guard_position_and_direction(board: list[str]) -> Position:
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] in DIRECTIONS:
                d: Direction = cast(Direction, board[r][c])
                return Position((r, c), d)
            
    raise LookupError("Guard not found")


def get_next_guard_position(board: list[str], cur_pos: Position) -> Position | None:
    cur_loc, cur_dir = cur_pos
    r, c = cur_loc
    if cur_dir == "^":
        next_loc = r - 1, c
    elif cur_dir == "v":
        next_loc = r + 1, c
    elif cur_dir == "<":
        next_loc = r, c - 1
    elif cur_dir == ">":
        next_loc = r, c + 1
    else:
        raise ValueError(f"Invalid direction: {cur_dir}")
    
    if not (0 <= next_loc[0] < len(board) and 0 <= next_loc[1] < len(board[0])):
        return None
    
    if board[next_loc[0]][next_loc[1]] == "#":
        next_dir = DIRECTIONS[(DIRECTIONS.index(cur_dir) + 1) % 4]
        return Position(cur_loc, next_dir)
    
    return Position(next_loc, cur_dir)


def is_location_valid(board: list[str], loc: Location) -> bool:
    r, c = loc
    return 0 <= r < len(board) and 0 <= c < len(board[0])

    
def get_patrol_path(board: list[str], start_pos: Position) -> tuple[Path, bool]:
    path = []
    path_set = set()
    cur_pos: Position | None = start_pos
    loop = False
    while cur_pos is not None and cur_pos not in path_set:
        path.append(cur_pos)
        path_set.add(cur_pos)
        cur_pos = get_next_guard_position(board, cur_pos)
        if cur_pos in path_set:
            loop = True
        
    return path, loop

with open("2024/06/input.txt", "r") as f:
    board = [l.strip() for l in f.readlines()]
    
initial_pos = get_initial_guard_position_and_direction(board)
path, _ = get_patrol_path(board, initial_pos)

# Part 1
unique_path_locations = {p.location for p in path}
print(len(unique_path_locations))

# Part 2
def find_potential_obstruction_locations(board: list[str], path: Path) -> set[Location]:
    initial_pos = path[0]
    potential_obstruction_locations = set()
    
    for pos in path:
        if pos == initial_pos:
            continue
        
        loc = pos.location
        
        # Temporarily place an obstacle
        original_row = board[loc[0]]
        board[loc[0]] = original_row[:loc[1]] + "#" + original_row[loc[1] + 1:]
        
        # Re-simulate the patrol
        _, loop = get_patrol_path(board, initial_pos)
        
        # If the loop persists, add the location
        if loop:
            potential_obstruction_locations.add(loc)
        
        # Restore the original board
        board[loc[0]] = original_row
    
    return potential_obstruction_locations

print(len(find_potential_obstruction_locations(board, path)))

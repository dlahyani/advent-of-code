
# Common
from typing import Literal


Direction = Literal["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

def move_in_direction(pos: tuple[int, int], direction: Direction, distance: int) -> tuple[int, int]:
    if direction == "N":
        return pos[0] - distance, pos[1]
    elif direction == "NE":
        return pos[0] - distance, pos[1] + distance
    elif direction == "E":
        return pos[0], pos[1] + distance
    elif direction == "SE":
        return pos[0] + distance, pos[1] + distance
    elif direction == "S":
        return pos[0] + distance, pos[1]
    elif direction == "SW":
        return pos[0] + distance, pos[1] - distance
    elif direction == "W":
        return pos[0], pos[1] - distance
    elif direction == "NW":
        return pos[0] - distance, pos[1] - distance
    else:
        raise ValueError(f"Invalid direction: {direction}")
    
def is_pos_in_board(board: list[str], pos: tuple[int, int]) -> bool:
    return pos[0] >= 0 and pos[0] < len(board) and pos[1] >= 0 and pos[1] < len(board[0])
    
def match_letter_in_direction(board: list[str], letter: str, base_pos: tuple[int, int], direction: Direction, distance: int) -> bool:
    target_pos = move_in_direction(base_pos, direction, distance)    
    return is_pos_in_board(board, target_pos) and (board[target_pos[0]][target_pos[1]] == letter)
        

def match_word_in_direction(board: list[str], word: str, pos: tuple[int, int], direction: Direction) -> bool:
    return all(match_letter_in_direction(board, c, pos, direction, i) for i, c in enumerate(word))

def match_word_in_all_directions(board: list[str], word: str, pos: tuple[int, int]) -> list[Direction]:
    return [
            direction  # type: ignore
            for direction in ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
            if match_word_in_direction(board, word, pos, direction)  #type: ignore
        ]


with open("2024/04/input.txt", "r") as f:
    data = [l.strip() for l in f.readlines()]

# Part 1
h = len(data)
w = len(data[0])
matches = {}
for r in range(h):
    for c in range(w):
        matched_directions = match_word_in_all_directions(data, "XMAS", (r, c))
        if len(matched_directions) > 0:
            matches[(r, c)] = matched_directions

total_matches = sum(len(v) for v in matches.values())
print(f"Found {total_matches} of 'XMAS' in the board")


# Part 2

def match_block(board: list[str], block: list[str], pos: tuple[int, int]) -> bool:
    for r, row in enumerate(block):
        for c, letter in enumerate(row):
            if not is_pos_in_board(board, (pos[0] + r, pos[1] + c)):
                return False
            if letter != "." and board[pos[0] + r][pos[1] + c] != letter:
                return False
    return True

X_MAS_BLOCKS = [
    ["M.M", ".A.", "S.S"],
    ["S.S", ".A.", "M.M"],
    ["M.S", ".A.", "M.S"],
    ["S.M", ".A.", "S.M"],
]

def match_x_mas_block_at_position(board: list[str], pos: tuple[int, int]) -> bool:
    for block in X_MAS_BLOCKS:
        if match_block(board, block, pos):
            return True
    return False

total_matches = 0
for r in range(h):
    for c in range(w):
        if match_x_mas_block_at_position(data, (r, c)):
            total_matches += 1

print(f"Found {total_matches} of X-'MAS' blocks in the board")
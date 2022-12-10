
from typing import Iterable

Position = tuple[int, int]
Rope = list[Position]

def simulate_rope_movement(rope_length: int, start_position: Position, instructions: Iterable[str]):
    rope: Rope = [start_position] * rope_length
    rope_movement: list[Rope] = [rope]

    for i in instructions:
        direction, steps = i.split(" ")
        steps = int(steps)
        rope_movement.extend(move_rope(rope_movement[-1], direction, steps))
    
    return rope_movement


def move_rope(rope: Rope, direction: str, steps: int) -> list[Rope]:
    rope_movement: list[Rope] = [rope]
    for _ in range(steps):
        rope_movement.append(move_rope_one_step(rope_movement[-1], direction))
    return rope_movement[1:]
            
def move_rope_one_step(rope: Rope, direction: str) -> Rope:
    new_rope = [move_head(rope[0], direction)]
    for i in range(1, len(rope)):
        new_rope.append(rope_knot_follow(new_rope[i-1], rope[i]))
    return new_rope

def move_head(head: Position, direction: str) -> Position:
    if direction == "R":
        head = head[0]+1, head[1]
    elif direction == "U":
        head = head[0], head[1]+1
    elif direction == "L":
        head = head[0]-1, head[1]
    else:
        head = head[0], head[1]-1
    return head

def rope_knot_follow(leading: Position, following: Position) -> Position:
    # Leading and following are adjacent, no need to move.
    if abs(following[0] - leading[0]) <= 1 and abs(following[1] - leading[1]) <= 1:
        return following
    # Following is 2 steps to the right of leading, move following one step left.
    elif following[0] - leading[0] > 1 and following[1] - leading[1] == 0:
        following = following[0] - 1, following[1]
    # Following is 2 steps to the right and above leading, move following one step left and one step down.
    elif following[0] - leading[0] > 0 and following[1] - leading[1] > 0:
        following = following[0] - 1, following[1] - 1
    # Following is 2 steps to above leading, move following one step down.
    elif following[0] == leading[0] and following[1] - leading[1] > 1:
        following = following[0], following[1] - 1
    # Following is 2 steps to the left and above leading, move following one step right and one step down.
    elif following[0] - leading[0] < 0 and following[1] - leading[1] > 0:
        following = following[0] + 1, following[1] - 1
    # Following is 2 steps to the right of leading, move following one step right.
    elif following[0] - leading[0] < -1 and following[1] - leading[1] == 0:
        following = following[0] + 1, following[1]
    # Following is 2 steps to the left and below leading, move following one step right and one step up.
    elif following[0] - leading[0] < 0 and following[1] - leading[1] < 0:
        following = following[0] + 1, following[1] + 1
    # Following is 2 steps to below leading, move following one step up.
    elif following[0] == leading[0] and following[1] - leading[1] < -1:
        following = following[0], following[1] + 1
    # Following is 2 steps to the right and below leading, move following one step left and one step up.
    else:
        following = following[0] - 1, following[1] + 1
    
    assert abs(following[0] - leading[0]) <= 1 and abs(following[1] - leading[1]) <= 1
    return following

instructions = tuple(map(lambda l: l.strip(), open("2022/09/input.txt")))

### Part 1
rope_movement = simulate_rope_movement(2, (0,0), instructions)
tail_visited = set(map(lambda rp: rp[-1], rope_movement))
print(f"Tail visited in {len(tail_visited)} unique spots")

### Part 2
rope_movement = simulate_rope_movement(10, (0,0), instructions)
tail_visited = set(map(lambda rp: rp[-1], rope_movement))
print(f"Tail visited in {len(tail_visited)} unique spots")

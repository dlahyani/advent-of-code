
from functools import reduce
from typing import Iterable

Position = tuple[int, int]
Rope = list[Position]

def simulate_rope_movement(rope_length: int, start_position: Position, instructions: Iterable[str]) -> Iterable[Rope]:
    return reduce(lambda rope_movement, i: rope_movement + move_rope(rope_movement[-1], i[0], i[1]),
        map(lambda i: (i[0], int(i[1])),
            map(lambda i: i.strip().split(), instructions)
        ), [[start_position] * rope_length])

def move_rope(rope: Rope, direction: str, steps: int) -> Iterable[Rope]:
    return reduce(lambda m, _: m + [move_rope_one_step(m[-1], direction)], range(steps), [rope])[1:]
            
def move_rope_one_step(rope: Rope, direction: str) -> Rope:
    return reduce(lambda new_rope, i: new_rope + [rope_knot_follow(new_rope[i-1], rope[i])],
        range(1, len(rope)), [move_rope_knot(rope[0], direction)])

def move_rope_knot(knot: Position, direction: str) -> Position:
    step = {"R": (1, 0), "U": (0, 1), "L": (-1, 0), "D": (0, -1)}[direction]
    return (knot[0] + step[0], knot[1] + step[1])

def sign(n: int) -> int:
    return 0 if n == 0 else 1 if n > 0 else -1

def rope_knot_follow(leading: Position, following: Position) -> Position:
    # Leading and following are adjacent, no need to move.
    if abs(following[0] - leading[0]) <= 1 and abs(following[1] - leading[1]) <= 1:
        return following
    
    step = sign(leading[0] - following[0]), sign(leading[1] - following[1])
    return following[0] + step[0] , following[1] + step[1]

instructions = open("2022/09/input.txt").readlines()

### Part 1
tail_positions = set(map(lambda rp: rp[-1], simulate_rope_movement(2, (0,0), instructions)))
print(f"Rope length: 2 knots, Unique tail positions: {len(tail_positions)} ")

### Part 2
tail_positions = set(map(lambda rp: rp[-1], simulate_rope_movement(10, (0,0), instructions)))
print(f"Rope length: 10 knots, Unique tail positions: {len(tail_positions)}")

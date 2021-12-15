from functools import reduce


def make_step_1(start_position, direction, offset):
    new_position = start_position.copy() if start_position else {"h": 0, "d": 0}
    if direction == "up":
        new_position["d"] -= int(offset)
    elif direction == "down":
        new_position["d"] += int(offset)
    else:
        new_position["h"] += int(offset)
    
    return new_position

def make_step_2(start_position, direction, offset):
    new_position = start_position.copy() if start_position else {"h": 0, "d": 0, "a": 0}
    if direction == "up":
        new_position["a"] -= int(offset)
    elif direction == "down":
        new_position["a"] += int(offset)
    else:
        new_position["h"] += int(offset)
        new_position["d"] += new_position["a"] * int(offset)
    
    return new_position
    

with open("2021/02/input.txt") as f:
    instructions = f.readlines()

# Part 1
position = reduce(
    lambda p, i: make_step_1(p, *(i.split())), instructions, None
)

print("***** Part 1:")
print(f"Final position: {position}")
print(f"Horizontal * Depth = {position['h'] * position['d']}")

# Part 2
position = reduce(
    lambda p, i: make_step_2(p, *(i.split())), instructions, None
)

print("***** Part 2:")
print(f"Final position: {position}")
print(f"Horizontal * Depth = {position['h'] * position['d']}")


from __future__ import annotations
from enum import Enum
from typing import Tuple

Position = Tuple[int, int]
Direction = int
EAST = 0
NORTH = 90
WEST = 180
SOUTH = 270
ValidDirections = (EAST, NORTH, WEST, SOUTH)


class DirectionalPosition:
    def __init__(self, direction: Direction, position: Position):
        assert direction in ValidDirections
        self.direction = direction
        self.position = position
        
    def translate(self, direction: Direction, units: int) -> DirectionalPosition:
        direction_to_translation_factor = {EAST: (1, 0), WEST: (-1, 0), NORTH: (0, 1), SOUTH: (0, -1)}
        factor = direction_to_translation_factor[direction]
        new_position = self.position[0] + factor[0]*units, self.position[1] + factor[1]*units 
        return DirectionalPosition(self.direction, new_position)
    
    def rotate(self, degrees: int) -> DirectionalPosition:
        return DirectionalPosition((self.direction + degrees) % 360, self.position)
    
    def manhattan_distance_from(self, dp: DirectionalPosition) -> int:
        return abs(dp.position[0] - self.position[0]) + abs(dp.position[1] - self.position[1])
    
    def __repr__(self) -> str:
        direction_to_name = {EAST: "EAST", WEST: "WEST", NORTH: "NORTH", SOUTH: "SOUTH"}
        direction_name = direction_to_name[self.direction]
        return f"(Position={self.position}, Direction={direction_name})"


class Instruction:
    VALID_ACTIONS = "EWNSLRF"
    
    def __init__(self, action: str, value: int):
        assert action in Instruction.VALID_ACTIONS
        self.action = action
        self.value = value
    
    @staticmethod
    def direction_from_action(action: str):
        return {"E": EAST, "W": WEST, "N": NORTH, "S": SOUTH}[action]
        
    def apply(self, dp: DirectionalPosition) -> DirectionalPosition:
        if self.action in "EWNS":
            direction = self.direction_from_action(self.action)
            return dp.translate(direction, self.value)
        elif self.action in "LR":
            degrees = self.value * (1 if self.action == "L" else -1)
            return dp.rotate(degrees)
        elif self.action == "F":
            return dp.translate(dp.direction, self.value)
        else:
            raise ValueError("Invalid instruction")
        
instructions = [Instruction(l[:1], int(l[1:].strip())) for l in open("2020/12/input.txt").readlines()]

initial_pos = DirectionalPosition(EAST, (0,0))
trajectory = [initial_pos]
cur_pos = initial_pos
for i in instructions:
    cur_pos = i.apply(cur_pos)
    trajectory.append(cur_pos)

final_pos = trajectory[-1]
md = initial_pos.manhattan_distance_from(final_pos)
# print(f"Ferry trajectory: {trajectory}")
print(f"Manhattan distance after all instructions: {md}")
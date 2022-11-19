
from __future__ import annotations
from enum import Enum
from typing import Tuple

Offset = Tuple[int, int]
Direction = int
EAST = 0
NORTH = 90
WEST = 180
SOUTH = 270
ValidDirections = (EAST, NORTH, WEST, SOUTH)

class Point:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
    
    def rotate(self, degrees: int) -> Point:
        degrees = degrees % 360
        if degrees == 0:
            return Point(self.x, self.y)
        elif degrees == 90:
            return Point(-self.y, self.x)
        elif degrees == 180:
            return Point(-self.x, -self.y)
        elif degrees == 270:
            return Point(self.y, -self.x)
        else:
            raise ValueError("Rotating is only allowed by 90 degrees multiply")
            
    def __add__(self, offset: Offset) -> Point:
        return Point(self.x + offset[0], self.y + offset[1])
    
    def __mul__(self, scalar: int) -> Point:
        return Point(self.x * scalar, self.y * scalar)
    
    def manhattan_distance_from(self, p: Point) -> int:
        return abs(p.x - self.x) + abs(p.y - self.y)

class Instruction:
    VALID_ACTIONS = "EWNSLRF"
    
    def __init__(self, action: str, value: int):
        assert action in Instruction.VALID_ACTIONS
        self.action = action
        self.value = value
        
    @property
    def direction(self) -> Direction:
        if self.action not in "EWNS":
            raise AttributeError(f"Instruction with '{self.action}' has no direction attribute")
        
        return {"E": EAST, "W": WEST, "N": NORTH, "S": SOUTH}[self.action]
         
    @property
    def offset(self) -> Offset:
        if self.action not in "EWNS":
            raise AttributeError(f"Instruction with '{self.action}' has no offset attribute")
        
        return {"E": (self.value, 0), "W": (-self.value, 0), "N": (0, self.value), "S": (0, -self.value)}[self.action]
    
    @property
    def degrees(self) -> int:
        if self.action == "L":
            return self.value
        elif self.action == "R":
            return 360 - self.value
        else:
            raise AttributeError(f"Instruction with '{self.action}' has no degrees attribute")
            
        

class Ferry:
    def __init__(self, initial_position: Point, direction: Direction):
        assert direction in ValidDirections
        self._position = initial_position
        self._direction = direction
        
    @property
    def position(self) -> Point:
        return self._position
    
    @property
    def direction(self) -> Direction:
        return self._direction    
    
    def apply_instruction(self, instruction: Instruction):
        if instruction.action in "EWNS":
            self._move_by_offset(instruction.offset)
        elif instruction.action in "LR":
            self._rotate(instruction.degrees)
        elif instruction.action == "F":
            self._move_forward(instruction.value)
        else:
            raise ValueError("Invalid instruction")
    
    def _move_by_offset(self, offset: Offset):
        self._position = self._position + offset
        
    def _rotate(self, degrees: int):
        self._direction = (self.direction + degrees) % 360
    
    def _move_forward(self, units: int):
        direction_to_translation_factor = {EAST: (1, 0), WEST: (-1, 0), NORTH: (0, 1), SOUTH: (0, -1)}
        factor = direction_to_translation_factor[self._direction]
        offset = factor[0]*units, factor[1]*units
        self._move_by_offset(offset)
    

class FerryWithWayPoint:
    def __init__(self, position: Point, waypoint_offset: Offset):
        self._ferry_position = position
        self._waypoint_offset = waypoint_offset
    
    @property
    def position(self) -> Point:
        return self._ferry_position
    
    @property
    def waypoint_offset(self) -> Offset:
        return self._waypoint_offset
    
    @property
    def waypoint_position(self) -> Point:
        return self._ferry_position + self._waypoint_offset
    
    def apply_instruction(self, instruction: Instruction):
        if instruction.action in "EWNS":
            offset = instruction.offset
            self._waypoint_offset = self._waypoint_offset[0]+offset[0], self._waypoint_offset[1]+offset[1]
        elif instruction.action in "LR":
            self._rotate_waypoint_around_ferry(instruction.degrees)
        elif instruction.action == "F":
            self._move_ferry_to_waypoint(instruction.value)
    
    def _rotate_waypoint_around_ferry(self, degrees: int):
        new_offset = Point(self._waypoint_offset[0], self._waypoint_offset[1]).rotate(degrees)
        self._waypoint_offset = new_offset.x, new_offset.y
    
    def _move_ferry_to_waypoint(self, times: int):
        for i in range(times):
            self._ferry_position = self._ferry_position + self._waypoint_offset
                

instructions = [Instruction(l[:1], int(l[1:].strip())) for l in open("2020/12/input.txt").readlines()]

initial_pos = Point(0,0)
ferry = Ferry(initial_pos, EAST)
trajectory = [initial_pos]
cur_pos = initial_pos
for i in instructions:
    ferry.apply_instruction(i)
    trajectory.append(ferry.position)

final_pos = trajectory[-1]
md = initial_pos.manhattan_distance_from(final_pos)
print(f"Manhattan distance after all instructions: {md}")

### Part 2
initial_pos = Point()
waypoint_offset = (10, 1)
ferry = FerryWithWayPoint(initial_pos, waypoint_offset)
trajectory = [initial_pos]
cur_pos = initial_pos
for i in instructions:
    ferry.apply_instruction(i)
    trajectory.append(ferry.position)

final_pos = trajectory[-1]
md = initial_pos.manhattan_distance_from(final_pos)
# print(f"Ferry trajectory: {trajectory}")
print(f"Manhattan distance after all instructions: {md}")
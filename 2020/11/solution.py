
from typing import Dict, Iterable, List, Optional, Tuple

SeatingMap = List[List[str]]
Position = Tuple[int, int]
Offset = Tuple[int, int]

Neighboring = Iterable[Offset]
Nearest8Neighboring = ([-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1])

EMPTY_SEAT = "L"
OCCUPIED_SEAT = "#"
FLOOR = "."


def get_neighbors(
        seating_area: SeatingMap,
        seat_position: Position,
        neighbors_offsets: Neighboring = Nearest8Neighboring
    ) -> Dict[Position, str]:
    res: Dict[Position, str] = {}
    for o in neighbors_offsets:
        neighbor_pos = seat_position[0]+o[0], seat_position[1]+o[1]
        if (neighbor_pos[0] < 0 or neighbor_pos[0] >= len(seating_area) or
            neighbor_pos[1] < 0 or neighbor_pos[1] >= len(seating_area[0])):
                continue
        
        res[neighbor_pos] = seating_area[neighbor_pos[0]][neighbor_pos[1]]
        
    return res

def apply_offset(seating_area: SeatingMap, pos: Position, offset: Offset) -> Optional[Position]:
    pos_with_offset = pos[0]+offset[0], pos[1]+offset[1]
    if (pos_with_offset[0] < 0 or pos_with_offset[0] >= len(seating_area) or
        pos_with_offset[1] < 0 or pos_with_offset[1] >= len(seating_area[0])):
        return None
    return pos_with_offset

def get_neighbors2(
        seating_area: SeatingMap,
        seat_position: Position,
        neighbors_offsets: Neighboring = Nearest8Neighboring
    ) -> Dict[Position, str]:
    res: Dict[Position, str] = {}
    for o in neighbors_offsets:
        neighbor_pos = apply_offset(seating_area, seat_position, o)
        if neighbor_pos is None:
            continue
        
        neighbor_state = seating_area[neighbor_pos[0]][neighbor_pos[1]]
        while neighbor_state == FLOOR:
            neighbor_pos = apply_offset(seating_area, neighbor_pos, o)
            if neighbor_pos is None:
                break
            neighbor_state = seating_area[neighbor_pos[0]][neighbor_pos[1]]
        
        if neighbor_pos == FLOOR:
            continue
        
        res[neighbor_pos] = neighbor_state
        
    return res        

def should_flip_seat(seating_area: SeatingMap, pos: Position) -> bool:
    pos_state = seating_area[pos[0]][pos[1]]
    if pos_state == FLOOR:
        return False
    
    neighbors = get_neighbors2(seating_area, pos)
    occupied_neighbors = len(list(filter(lambda v: v == OCCUPIED_SEAT, neighbors.values())))
    if pos_state == EMPTY_SEAT and occupied_neighbors == 0:
        return True
    elif pos_state == OCCUPIED_SEAT and occupied_neighbors >= 5:
        return True
    
    return False

def get_seats_to_flip(seating_area: SeatingMap) -> List[Position]:
    seats_to_flip = []
    for r in range(len(seating_area)):
        row = seating_area[r]
        for c in range(len(row)):
            if should_flip_seat(seating_area, (r, c)):
                seats_to_flip.append((r, c))
    
    return seats_to_flip

def flip_seat(seating_area: SeatingMap, pos: Position):
    cur_state = seating_area[pos[0]][pos[1]]
    if cur_state == EMPTY_SEAT:
        seating_area[pos[0]][pos[1]] = OCCUPIED_SEAT
    elif cur_state == OCCUPIED_SEAT:
        seating_area[pos[0]][pos[1]] = EMPTY_SEAT
    else:
        raise ValueError(f"Unexpected seat state '{cur_state}' at position {pos}")

def flip_seats(seating_area: SeatingMap, seats: List[Position]):
    for p in seats:
        flip_seat(seating_area, p)

def get_seats_with_state(seating_area: SeatingMap, state: str) -> List[Position]:
    matching_seats = []
    for r in range(len(seating_area)):
        row = seating_area[r]
        for c in range(len(row)):
            seat = seating_area[r][c]
            if seat == state:
                matching_seats.append((r, c))
    
    return matching_seats

def print_seating_area(seating_area: SeatingMap):
    for r in range(len(seating_area)):
        row = ''.join(seating_area[r])
        print(row)
    print("\n\n")
    
seating_area = [list(l.strip()) for l in open("2020/11/input.txt").readlines()]

print("Initial seat map")
print_seating_area(seating_area)

rounds = 0
while(True):
    seats_to_flip = get_seats_to_flip(seating_area)
    if len(seats_to_flip) == 0:
        break
    flip_seats(seating_area, seats_to_flip)
    rounds += 1
    print(f"{rounds} flip rounds done")
    


occupied_seats = get_seats_with_state(seating_area, OCCUPIED_SEAT)
print(f"Reached equilibrium after {rounds} rounds")
print(f"Total occupied seats: {len(occupied_seats)}")

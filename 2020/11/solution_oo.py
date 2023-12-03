from typing import Dict, Iterable, List, Optional, Protocol, Tuple

SeatingMap = List[List[str]]
Position = Tuple[int, int]
Offset = Tuple[int, int]

EMPTY_SEAT = "L"
OCCUPIED_SEAT = "#"
FLOOR = "."


def apply_offset(seating_area: SeatingMap, pos: Position, offset: Offset) -> Optional[Position]:
    pos_with_offset = pos[0] + offset[0], pos[1] + offset[1]
    if (
        pos_with_offset[0] < 0
        or pos_with_offset[0] >= len(seating_area)
        or pos_with_offset[1] < 0
        or pos_with_offset[1] >= len(seating_area[0])
    ):
        return None
    return pos_with_offset


class Visibility(Protocol):
    def get_visible_seats(self, seating_map: SeatingMap, seat_position: Position) -> Dict[Position, str]:
        pass


class StaticOffsetNeighborsVisibility:
    Nearest4Neighboring = ((-1, 0), (0, 1), (1, 0), (0, -1))
    Nearest8Neighboring = (
        (-1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
    )

    def __init__(self, neighbors_offsets: Iterable[Offset] = Nearest8Neighboring):
        self._neighbors_offsets = neighbors_offsets

    def get_visible_seats(self, seating_map: SeatingMap, seat_position: Position) -> Dict[Position, str]:
        visible_seats: Dict[Position, str] = {}
        for o in self._neighbors_offsets:
            neighbor_pos = apply_offset(seating_map, seat_position, o)
            if neighbor_pos is None:
                continue

            visible_seats[neighbor_pos] = seating_map[neighbor_pos[0]][neighbor_pos[1]]

        return visible_seats


class OcclusionBasedVisibility:
    Classic8PointsCompassRose = (
        (-1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
    )

    def __init__(self, visibility_directions: Iterable[Offset] = Classic8PointsCompassRose):
        self._visibility_directions = visibility_directions

    def get_visible_seats(self, seating_map: SeatingMap, seat_position: Position) -> Dict[Position, str]:
        visible_seats: Dict[Position, str] = {}
        for d in self._visibility_directions:
            nearest_visible_seat = self._get_nearest_seat_in_direction(seating_map, seat_position, d)
            if nearest_visible_seat is None:
                continue

            visible_seats[nearest_visible_seat[0]] = nearest_visible_seat[1]

        return visible_seats

    def _get_nearest_seat_in_direction(
        self, seating_map: SeatingMap, pos: Position, direction: Offset
    ) -> Optional[Tuple[Position, str]]:
        next_pos: Optional[Position] = pos
        next_pos_state = FLOOR
        while next_pos_state == FLOOR:
            assert next_pos is not None
            next_pos = apply_offset(seating_map, next_pos, direction)
            if next_pos is None:
                return None

            next_pos_state = seating_map[next_pos[0]][next_pos[1]]

        assert next_pos is not None and next_pos_state != FLOOR
        return next_pos, next_pos_state


class SeatFlippingRules(Protocol):
    def should_flip_seat(self, seating_area: SeatingMap, pos: Position) -> bool:
        pass


class VisibilityThresholdBasedSeatFlippingRules:
    def __init__(
        self,
        empty_seat_flip_threshold: int,
        occupied_seat_flip_threshold: int,
        seat_visibility: Visibility,
    ):
        self._empty_seat_flip_threshold = empty_seat_flip_threshold
        self._occupied_seat_flip_threshold = occupied_seat_flip_threshold
        self._seat_visibility = seat_visibility

    def should_flip_seat(self, seating_area: SeatingMap, pos: Position) -> bool:
        pos_state = seating_area[pos[0]][pos[1]]
        if pos_state == FLOOR:
            return False

        visible_seats = self._seat_visibility.get_visible_seats(seating_area, pos)
        occupied_neighbors = len(list(filter(lambda v: v == OCCUPIED_SEAT, visible_seats.values())))
        if pos_state == EMPTY_SEAT and occupied_neighbors <= self._empty_seat_flip_threshold:
            return True
        elif pos_state == OCCUPIED_SEAT and occupied_neighbors >= self._occupied_seat_flip_threshold:
            return True

        return False


class SeatingAreaLifecycleAlgorithm:
    def __init__(self, seat_flipping_rules: SeatFlippingRules):
        self._seat_flipping_rules = seat_flipping_rules

    def get_seats_to_flip(self, seating_area: SeatingMap) -> List[Position]:
        seats_to_flip = []
        for r in range(len(seating_area)):
            row = seating_area[r]
            for c in range(len(row)):
                if self._seat_flipping_rules.should_flip_seat(seating_area, (r, c)):
                    seats_to_flip.append((r, c))

        return seats_to_flip

    def flip_seats(self, seating_area: SeatingMap, seats: List[Position]):
        for p in seats:
            self._flip_seat(seating_area, p)

    def _flip_seat(self, seating_area: SeatingMap, pos: Position):
        cur_state = seating_area[pos[0]][pos[1]]
        if cur_state == EMPTY_SEAT:
            seating_area[pos[0]][pos[1]] = OCCUPIED_SEAT
        elif cur_state == OCCUPIED_SEAT:
            seating_area[pos[0]][pos[1]] = EMPTY_SEAT
        else:
            raise ValueError(f"Unexpected seat state '{cur_state}' at position {pos}")

    def flip_seats_till_equilibrium(
        self,
        seating_area: SeatingMap,
        max_rounds: int = 2**10,
        print_board: bool = False,
    ) -> int:
        rounds = 0
        while True:
            print(".", end="", flush=True)
            seats_to_flip = self.get_seats_to_flip(seating_area)
            if len(seats_to_flip) == 0:
                break
            elif rounds >= max_rounds:
                raise ValueError(f"Equilibrium was not reached within {max_rounds} rounds")

            seat_flipping_algo.flip_seats(seating_area, seats_to_flip)
            rounds += 1
            if print_board:
                print_seating_area(seating_area)

        print("\n")
        return rounds


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
        row = "".join(seating_area[r])
        print(row)
    print("\n\n")


g_seating_area = [list(l.strip()) for l in open("2020/11/input.txt").readlines()]

print("Initial seat map")
print_seating_area(g_seating_area)

### Part 1
print("Part 1: Trying to reach equilibrium with simple neighboring rules")
seat_flipping_algo = SeatingAreaLifecycleAlgorithm(
    VisibilityThresholdBasedSeatFlippingRules(0, 4, StaticOffsetNeighborsVisibility())
)
rounds = seat_flipping_algo.flip_seats_till_equilibrium(g_seating_area)
occupied_seats = get_seats_with_state(g_seating_area, OCCUPIED_SEAT)
print(f"Reached equilibrium after {rounds} rounds")
print(f"Total occupied seats: {len(occupied_seats)}")

### Part 2
print("Part 2: Trying to reach equilibrium with complex occlusion based visibility rules")
g_seating_area = [list(l.strip()) for l in open("2020/11/input.txt").readlines()]
seat_flipping_algo = SeatingAreaLifecycleAlgorithm(
    VisibilityThresholdBasedSeatFlippingRules(0, 5, OcclusionBasedVisibility())
)
rounds = seat_flipping_algo.flip_seats_till_equilibrium(g_seating_area)
occupied_seats = get_seats_with_state(g_seating_area, OCCUPIED_SEAT)
print(f"Reached equilibrium after {rounds} rounds")
print(f"Total occupied seats: {len(occupied_seats)}")

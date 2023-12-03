from typing import Iterable, Generator


Point = tuple[int, int]
Line = tuple[Point, Point]
Vector = tuple[int, int]


def parse_point(point: str) -> Point:
    x1, y1 = [int(c) for c in point.split(",")]
    return (x1, y1)


def parse_line(line: str) -> Line:
    start, end = [parse_point(p) for p in line.split(" -> ")]
    return (start, end)


def line_direction(line: Line) -> str:
    return "v" if line[0][0] == line[1][0] else ("h" if line[0][1] == line[1][1] else "d")


def get_line_length(line: Line) -> int:
    fixed_cord = 0 if line_direction(line) == "v" else 1
    return abs(line[1][1 - fixed_cord] - line[0][1 - fixed_cord]) + 1


def get_line_step(line: Line) -> tuple[int, int]:
    dx = line[1][0] - line[0][0]
    dy = line[1][1] - line[0][1]

    sx = 0 if dx == 0 else (1 if dx > 0 else -1)
    sy = 0 if dy == 0 else (1 if dy > 0 else -1)
    return (sx, sy)


def steps_from_point(point: Point, step: Vector, steps: int = 1) -> Point:
    return (point[0] + step[0] * steps, point[1] + step[1] * steps)


def line_points(line: Line) -> Generator:
    step = get_line_step(line)
    cur_point = line[0]
    while cur_point != line[1]:
        yield cur_point
        cur_point = steps_from_point(cur_point, step)

    yield cur_point


def mark_line_points(line: Line, board: dict[Point, int]) -> Iterable[Point]:
    danger_points = set()
    for p in line_points(line):
        board[p] = 1 if not p in board else board[p] + 1
        if board[p] >= 2:
            danger_points.add(p)

    return danger_points


print("Part 1, ignoring diagonals")
board = {}
danger_points = set()
lines = [parse_line(l) for l in open("2021/05/input.txt", "r").readlines()]
for l in lines:
    if line_direction(l) == "d":
        print(f"Line: {l} is diagonal, skiping")
        continue

    danger_points = danger_points.union(mark_line_points(l, board))

print(f"Danger spots: {len(danger_points)}")

print("Part 2, allowing diagonals")
board = {}
danger_points = set()
lines = [parse_line(l) for l in open("2021/05/input.txt", "r").readlines()]
for l in lines:
    danger_points = danger_points.union(mark_line_points(l, board))

print(f"Danger spots: {len(danger_points)}")

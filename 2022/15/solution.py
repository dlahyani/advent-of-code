from itertools import chain, product
import itertools
import re


def minimize_intervals(intervals):
    if len(intervals) <= 1:
        return intervals

    intervals.sort(key=lambda x: x[0])
    minimized = [intervals[0]]
    for i in range(1, len(intervals)):
        last_interval = minimized[-1]
        current_interval = intervals[i]
        if current_interval[0] <= last_interval[1]:
            minimized[-1] = (
                last_interval[0],
                max(last_interval[1], current_interval[1]),
            )
        else:
            minimized.append(current_interval)

    return minimized


def parse_input(lines):
    pattern = re.compile("^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$")
    return {
        tuple(int(c) for c in m.groups()[0:2]): tuple(int(c) for c in m.groups()[2:4])
        for m in [pattern.match(l.strip()) for l in lines]
    }


def get_row_coverage_by_sensors(sensors_to_beacons_distance, row):
    row_coverage_ranges = []
    for s, d in sensors_to_beacons_distance.items():
        r = (d - abs(s[1] - row)) * 2 + 1
        if r <= 0:
            continue
        row_coverage_ranges.append((s[0] - (r // 2), s[0] + r // 2 + 1))

    return minimize_intervals(row_coverage_ranges)


def get_sensor_boundary_lines(s, r):
    """
    Sensor coverage is bounded by a diamond shaped box, defining 4 boundary lines,
    two lines with gradient of 1 and two lines with gradient of -1.
    The formula for a line with gradient m which passes through point (x1, y1) is:
      l := (y - y1) = m(x - x1) ==> y = m*x - m*x1+y1

    We know m = 1 or -1, and (x1, y1) is the sensor coords (xs, ys) + (r+1, 0) / (-r-1, 0) / (0, r+1) / (0, -r-1)
    Thus we get:
      l1 (m=1, (x1,y1)=(xs,ys)+(r+1, 0))   := y = x - xs - r - 1 + ys
      l2 (m=1, (x1,y1)=(xs,ys)+(-r-1, 0))  := y = x - xs + r + 1 + ys
      l3 (m=-1, (x1,y1)=(xs,ys)+(0, r+1))  := y = -x + xs + ys + r + 1
      l4 (m=-1, (x1,y1)=(xs,ys)+(0, -r-1)) := y = -x + xs + ys - r - 1
    """
    return (
        (1, -s[0] - r - 1 + s[1]),
        (1, -s[0] + r + 1 + s[1]),
        (-1, s[0] + s[1] + r + 1),
        (-1, s[0] + s[1] - r - 1),
    )


def get_lines_intersection_point(l1, l2):
    """
    Determining where a lines l1 and l2 intersect.
    Assuming l1 and l2 are of the form l1:y=mx+a and a line l2:y=-mx+b this is easy, the intersection point
    is ((b-a)/2, (a+b)/2).
    """
    assert l1[0] == -l2[0]
    return ((l2[1] - l1[1]) // 2, (l1[1] + l2[1]) // 2)


def is_point_covered_by_sensor(s, d, p):
    return abs(s[0] - p[0]) + abs(s[1] - p[1]) <= d


sensors_to_beacons = parse_input(open("2022/15/input.txt").readlines())
sensors_to_beacons_distance = {s: abs(s[0] - b[0]) + abs(s[1] - b[1]) for s, b in sensors_to_beacons.items()}

### Part 1
row = 2000000
row_coverage_ranges = get_row_coverage_by_sensors(sensors_to_beacons_distance, row)
beacons = set(sensors_to_beacons.values())
row_coverage = sum([r[1] - r[0] - len([b for b in beacons if b[1] == row]) for r in row_coverage_ranges])
print(f"Number of points covered by sensor in row {row} is: {row_coverage}")

### Part 2
min_x, max_x = 0, 4000000
min_y, max_y = 0, 4000000

lines = list(chain.from_iterable(get_sensor_boundary_lines(s, d) for s, d in sensors_to_beacons_distance.items()))
pos_lines, neg_lines = filter(lambda l: l[0] > 0, lines), filter(lambda l: l[0] < 0, lines)
all_intersection_points = {get_lines_intersection_point(*p) for p in product(pos_lines, neg_lines)}
for p in all_intersection_points:
    if p[0] < min_x or p[0] > max_x or p[1] < min_y or p[1] > max_y:
        continue

    p_covered = False
    for s, d in sensors_to_beacons_distance.items():
        p_covered |= is_point_covered_by_sensor(s, d, p)
        if p_covered:
            break
    if not p_covered:
        break

print(f"Point {p} is not covered by any sensor")
print(f"The tuning frequency for a beacon in this point would be: {p[0] * 4000000 + p[1]}")

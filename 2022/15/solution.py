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
            minimized[-1] = (last_interval[0], max(last_interval[1], current_interval[1]))
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
        r = (d - abs(s[1]-row))*2 + 1
        if r <= 0: continue
        row_coverage_ranges.append((s[0]-(r//2), s[0] + r//2 + 1))
        
    return minimize_intervals(row_coverage_ranges)
    
sensors_to_beacons = parse_input(open("2022/15/input.txt").readlines())
sensors_to_beacons_distance = {s: abs(s[0]-b[0]) + abs(s[1]-b[1]) for s, b in sensors_to_beacons.items()}

### Part 1
row = 2000000
row_coverage_ranges = get_row_coverage_by_sensors(sensors_to_beacons_distance, row)
beacons = set(sensors_to_beacons.values())
row_coverage = sum([r[1]-r[0] - len([b for b in beacons if b[1]==row]) for r in row_coverage_ranges])
print(row_coverage)

### Part 2
min_x, max_x = 0, 4000000
min_y, max_y = 0, 4000000
x, y = None, None
row_coverage_ranges = None
for r in range(min_y, max_y+1):
    r_coverage_ranges = get_row_coverage_by_sensors(sensors_to_beacons_distance, r)
    if len(r_coverage_ranges) != len(minimize_intervals(r_coverage_ranges + [(min_x, max_x+1)])):
        y, row_coverage_ranges = r, r_coverage_ranges
        break
    
for c in row_coverage_ranges:
    if c[0] > min_x and c[0] < max_x+1:
        x = c[0]-1
    
print(f"Found slot for hidden beacon at (x={x}, y={y})")
print(f"The tuning frequency for this beacon is: {x * 4000000 + y}")
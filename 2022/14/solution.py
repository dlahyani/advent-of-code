SAND_SRC_COORDS = (500, 0)
SAND_SRC_MARK = "S"
AIR_MARK = "."
ROCK_MARK = "#"
SAND_UNIT_MARK = "o"


def create_empty_cave_map(paths, initial_top_left, initial_bottom_right, extra_rows=0, extra_cols=0):
    top_left = initial_top_left
    bottom_right = initial_bottom_right
    for p in paths:
        for i in range(len(p)):
            if p[i][0] < top_left[0]:
                top_left = (p[i][0], 0)
            if p[i][0] > bottom_right[0]:
                bottom_right = (p[i][0], bottom_right[1])
            if p[i][1] > bottom_right[1]:
                bottom_right = (bottom_right[0], p[i][1])

    rows = bottom_right[1] - top_left[1] + 1 + extra_rows
    cols = bottom_right[0] - top_left[0] + 1 + extra_cols
    cave_map = [["."]*cols for _ in range(rows)]
    
    top_left = (top_left[0] - extra_cols//2, top_left[1])
    bottom_right = (bottom_right[0] + extra_cols//2, bottom_right[1] + extra_rows)
    return cave_map, top_left, bottom_right

def get_value_at_map_coords(cave_map, top_left, coords):
    c, r = coords[0] - top_left[0], coords[1] - top_left[1]
    return cave_map[r][c]

def set_value_at_map_coords(cave_map, top_left, coords, value):
    c, r = coords[0] - top_left[0], coords[1] - top_left[1]
    cave_map[r][c] = value

def set_path_values_on_map(cave_map, top_left, path):
    for i in range(1, len(path)):
        if path[i][0] == path[i-1][0]:
            d = 1 if path[i][1] > path[i-1][1] else -1
            s_coords = ((path[i][0], r) for r in range(path[i-1][1], path[i][1]+d, d))
        else:
            d = 1 if path[i][0] > path[i-1][0] else -1
            s_coords = ((c, path[i][1]) for c in range(path[i-1][0], path[i][0]+d, d))
        for c in s_coords: set_value_at_map_coords(cave_map, top_left, c, ROCK_MARK)
    

def drop_sand_unit(cave_map, top_left, sand_source_coords):
    if get_value_at_map_coords(cave_map, top_left, sand_source_coords) != SAND_SRC_MARK:
        return None
    
    sand_unit_pos = sand_source_coords
    while True:
        try:
            if get_value_at_map_coords(cave_map, top_left, (sand_unit_pos[0], sand_unit_pos[1]+1)) == AIR_MARK:
                sand_unit_pos = sand_unit_pos[0], sand_unit_pos[1]+1
            elif get_value_at_map_coords(cave_map, top_left, (sand_unit_pos[0]-1, sand_unit_pos[1]+1)) == AIR_MARK:
                sand_unit_pos = sand_unit_pos[0]-1, sand_unit_pos[1]+1
            elif get_value_at_map_coords(cave_map, top_left, (sand_unit_pos[0]+1, sand_unit_pos[1]+1)) == AIR_MARK:
                sand_unit_pos = sand_unit_pos[0]+1, sand_unit_pos[1]+1
            else:
                break
        except IndexError:
            sand_unit_pos = None
            break
    
    if sand_unit_pos is not None:
        set_value_at_map_coords(cave_map, top_left, sand_unit_pos, SAND_UNIT_MARK)
    return sand_unit_pos

def create_cave_map(paths, floor):
    extra_rows, extra_cols = 0, 0
    if floor: extra_rows, extra_cols = 2, 500
        
    cave_map, top_left, bottom_right = create_empty_cave_map(
        paths, SAND_SRC_COORDS, SAND_SRC_COORDS, extra_rows, extra_cols)
    set_value_at_map_coords(cave_map, top_left, SAND_SRC_COORDS, SAND_SRC_MARK)
    for p in paths: set_path_values_on_map(cave_map, top_left, p)
    if floor:
        floor_path = [[top_left[0], bottom_right[1]], bottom_right]
        set_path_values_on_map(cave_map, top_left, floor_path)
    
    return cave_map, top_left


paths = [[[int(c) 
           for c in s.split(",")]
          for s in p] 
         for p in [l.strip().split(" -> ") for l in open("2022/14/input.txt")]]

### Part 1
cave_map, top_left = create_cave_map(paths, False)
sand_units = 0
while drop_sand_unit(cave_map, top_left, SAND_SRC_COORDS) != None:
    sand_units += 1
    
print(f"Sand units dropped: {sand_units}")

### Part 2
cave_map, top_left = create_cave_map(paths, True)
sand_units = 0
while drop_sand_unit(cave_map, top_left, SAND_SRC_COORDS) != None:
    sand_units += 1

print(f"Sand units dropped: {sand_units}")
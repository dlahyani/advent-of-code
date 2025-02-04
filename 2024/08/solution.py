from typing import Any, Callable, Iterable


with open("2024/08/input.txt", "r") as f:
    data = [l.strip() for l in f.readlines()]
    

Frequency = str
Location = tuple[int, int]
Size = tuple[int, int]
AntennaMap = dict[Frequency, list[Location]]
AntennaPair = tuple[Location, Location]
AntinodesGenerator = Callable[[AntennaPair, Size], Iterable[Location]]
    
def get_antennas_map(full_map: list[str]) -> AntennaMap:
    antennas: AntennaMap = {}
    for r in range(len(full_map)):
        for c in range(len(full_map[0])):
            freq = full_map[r][c]
            if freq == ".":
                continue
            
            antennas.setdefault(freq, []).append((r, c))
    
    return antennas

        
def get_all_pairs(values: list[Any]) -> list[tuple[Any, Any]]:
    if len(values) < 2:
        return []
    
    return [(values[i], values[j]) for i in range(len(values)) for j in range(i+1, len(values))]

def get_freq_antenna_pairs(antennas: AntennaMap, freq: Frequency) -> list[AntennaPair]:
    return get_all_pairs(antennas[freq])


def get_freq_antinodes(antennas: AntennaMap, freq: Frequency, map_size: Size, antenna_pair_antinodes_generator: AntinodesGenerator) -> Iterable[Location]:
    antenna_pairs = get_freq_antenna_pairs(antennas, freq)
    antinodes: list[Location] = []
    for p in antenna_pairs:
        antinodes.extend(antenna_pair_antinodes_generator(p, map_size))
    
    return antinodes

def get_antinodes(full_map: list[str], antinodes_generator: AntinodesGenerator) -> set[Location]:
    map_size = len(full_map), len(full_map[0])
    antennas = get_antennas_map(full_map)
    antinodes: list[Location] = []
    for freq in antennas.keys():
        antinodes.extend(get_freq_antinodes(antennas, freq, map_size, antinodes_generator))
    
    return set(antinodes)
    
    
# Part 1
def get_antennas_pair_antinodes_1(antennas: AntennaPair, map_size: Size) -> Iterable[Location]:
    distance = antennas[1][0] - antennas[0][0], antennas[1][1] - antennas[0][1]
    antinodes: list[Location] = [
        (antennas[0][0] - distance[0], antennas[0][1] - distance[1]),
        (antennas[1][0] + distance[0], antennas[1][1] + distance[1]),
    ]
    verify_antinodes(antinodes, antennas)
    return filter(
        lambda l:  0 <= l[0] < map_size[0] and 0 <= l[1] < map_size[1],
        antinodes
    )

def verify_antinodes(antinodes: list[Location], antennas: AntennaPair) -> None:
    for a in antinodes:
        dist_1 = abs(a[0] - antennas[0][0]) + abs(a[1] - antennas[0][1])
        dist_2 = abs(a[0] - antennas[1][0]) + abs(a[1] - antennas[1][1])
        assert dist_1 == dist_2*2 or dist_2 == dist_1*2



antinodes = get_antinodes(data, antinodes_generator=get_antennas_pair_antinodes_1)
print(len(antinodes))

# Part 2
def get_antennas_pair_antinodes_2(antennas: AntennaPair, map_size: Size) -> Iterable[Location]:
    yield antennas[0]
    yield antennas[1]
    
    step = antennas[1][0] - antennas[0][0], antennas[1][1] - antennas[0][1]
    
    d = 1
    while True:
        antinode = antennas[0][0] - step[0]*d, antennas[0][1] - step[1]*d
        if not (0 <= antinode[0] < map_size[0] and 0 <= antinode[1] < map_size[1]):
            break
        yield antinode
        d+=1
    
    d = 1
    while True:
        antinode = antennas[1][0] + step[0]*d, antennas[1][1] + step[1]*d
        if not (0 <= antinode[0] < map_size[0] and 0 <= antinode[1] < map_size[1]):
            break
        
        yield antinode
        d+=1
        
antinodes = get_antinodes(data, antinodes_generator=get_antennas_pair_antinodes_2)
print(len(antinodes))

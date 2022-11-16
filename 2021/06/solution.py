
import copy
from functools import reduce

DAYS_TO_SIMULATE = 256


SpawnMap = dict[int, int]
    
def spawn_map_reducer(spawn_map: SpawnMap, i: int) -> SpawnMap:
    spawn_map[i] = spawn_map[i] + 1 if i in spawn_map else 1
    return spawn_map

def spawn_map_tick(spawn_map: SpawnMap) -> SpawnMap:
    new_map = {}
    for i in range(9):
        new_map[i] = spawn_map[i + 1] if (i + 1) in spawn_map else 0
        if i == 6:
            new_map[i] += spawn_map[0] if 0 in spawn_map else 0
        if i == 8:
            new_map[i] = spawn_map[0] if 0 in spawn_map else 0
    
    return new_map


def simulate_spawn_cycles(initial_spawn_map, cycles):
    spawn_map = copy.copy(initial_spawn_map)
    for i in range(cycles):
        spawn_map = spawn_map_tick(spawn_map)
    
    return spawn_map

with open("2021/06/input.txt", "r") as f:
    lf_horde = [int(n) for n in f.read().split(",")]

spawn_map = reduce(spawn_map_reducer, lf_horde, {})
assert sum(spawn_map.values()) == len(lf_horde)
print(f"Initial horde size: {sum(spawn_map.values())}")
print(spawn_map)

spawn_map = simulate_spawn_cycles(spawn_map, DAYS_TO_SIMULATE)
print(f"After {DAYS_TO_SIMULATE} days: New fish={spawn_map[8]}, Horde size={sum(spawn_map.values())}")
print(spawn_map)

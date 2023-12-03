from dataclasses import dataclass
from typing import Optional
import regex


@dataclass
class Valve:
    id: str
    flow_rate: int
    tunnels_dst: set[str]


class TunnelSystem:
    def __init__(self, valves: list[Valve]):
        self._valves = {v.id: v for v in valves}
        self._broken_valves = {v.id for v in valves if v.flow_rate == 0}
        self._open_valves = set()

    @property
    def valves(self) -> set[str]:
        return set(self._valves.keys())

    @property
    def broken_valves(self) -> set[str]:
        return self._broken_valves

    @property
    def open_valves(self) -> set[str]:
        return self._open_valves

    @property
    def flow_rate(self) -> int:
        return sum([self._valves[vid].flow_rate for vid in self._open_valves])

    def __len__(self) -> int:
        return len(self._valves)

    def valve(self, vid: str) -> Valve:
        return self._valves[vid]

    def open_valve(self, vid: str) -> None:
        self._open_valves.add(vid)

    def close_valve(self, vid: str) -> None:
        self._open_valves.remove(vid)


def parse_input(raw_input):
    pattern = regex.compile(r"Valve ([A-Z][A-Z]) has flow rate=(\d+); tunnels? leads? to valves?( ([A-Z][A-Z]),?)+")
    return [
        Valve(
            id=m.groups()[0],
            flow_rate=int(m.groups()[1]),
            tunnels_dst=set(m.captures(4)),
        )
        for m in map(lambda l: pattern.match(l.strip()), raw_input)
    ]


def maximize_flow(ts: TunnelSystem, cur_v: str, max_time: int) -> int:
    cache = {}

    def _maximize_flow(v: str, ttl: int) -> tuple[int, tuple[str]]:
        if ttl == 0 or len(ts.open_valves) == (len(ts) - len(ts.broken_valves)):
            return ts.flow_rate * ttl, tuple()

        k = (v, ttl, tuple(ts.open_valves))
        if k in cache:
            return cache[k]

        max_flow = 0
        max_flow_steps = None
        if v not in ts.open_valves and v not in ts.broken_valves:
            ts.open_valve(v)
            max_flow, max_flow_steps = _maximize_flow(v, ttl - 1)
            max_flow += ts.flow_rate
            max_flow_steps = (v,) + max_flow_steps
            ts.close_valve(v)

        for next_v in ts.valve(v).tunnels_dst:
            next_v_max_flow, next_v_max_flow_steps = _maximize_flow(next_v, ttl - 1)
            next_v_max_flow += ts.flow_rate
            if next_v_max_flow > max_flow:
                max_flow, max_flow_steps = next_v_max_flow, next_v_max_flow_steps

        cache[k] = (max_flow, max_flow_steps)
        return max_flow, max_flow_steps

    return _maximize_flow(cur_v, max_time - 1)


raw_input = open("2022/16/input.txt").readlines()
valves = parse_input(raw_input)
tunnel_system = TunnelSystem(valves)

### Part 1
max_flow, max_flow_steps = maximize_flow(tunnel_system, "AA", 30)
print(f"Max flow: {max_flow}")

# Part 2
max_flow_human, human_steps = maximize_flow(tunnel_system, "AA", 26)
for v in human_steps:
    tunnel_system.valve(v).flow_rate = 0
    tunnel_system.open_valve(v)
max_flow_elephant, elephant_steps = maximize_flow(tunnel_system, "AA", 26)
print(f"Max flow achieved: {max_flow_human + max_flow_elephant}")

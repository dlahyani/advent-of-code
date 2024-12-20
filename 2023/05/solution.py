from dataclasses import dataclass
from bisect import bisect_left, insort_left

SEEDS_LINE_PREFIX = "seeds: "


@dataclass
class RawRangeMapping:
    source_start: int
    dest_start: int
    length: int

    def is_source_index_within_range(self, source_index: int) -> bool:
        return self.source_start <= source_index < self.source_start + self.length

    def get_dest_index(self, source_index: int) -> int:
        if not self.is_source_index_within_range(source_index):
            raise ValueError(f"Source index {source_index} is not within range")

        return self.dest_start + (source_index - self.source_start)


@dataclass
class RawSectionMapping:
    source_type: str
    dest_type: str
    range_mappings: list[RawRangeMapping]

    def get_dest_index(self, source_index: int) -> tuple[int, int]:
        i = bisect_left(self.range_mappings, source_index, key=lambda x: x.source_start)
        range_left = self.range_mappings[i].dest_start - (source_index + 1) if i < len(self.range_mappings) else -1
        if i == 0:
            return source_index, range_left

        range_mapping = self.range_mappings[i - 1]
        if not range_mapping.is_source_index_within_range(source_index):
            return source_index, range_left

        return range_mapping.get_dest_index(source_index), range_left


def load_input(input_file_name: str) -> tuple[list[int], dict[str, RawSectionMapping]]:
    with open(input_file_name, "r") as f:
        seeds_lines = f.readline().strip()
        seeds_to_plant = [int(i) for i in seeds_lines[len(SEEDS_LINE_PREFIX) :].split(" ")]

        sections_mappings: dict[str, RawSectionMapping] = {}
        cur_section_mapping: RawSectionMapping | None = None
        for line in f:
            if line == "\n":
                cur_section_mapping = None
                continue

            if cur_section_mapping is None:
                source_type, dest_type = line.strip().split(" ")[0].split("-to-")
                cur_section_mapping = RawSectionMapping(source_type, dest_type, [])
                sections_mappings[source_type] = cur_section_mapping
                continue

            dest_start, source_start, length = [int(i) for i in line.strip().split(" ")]
            insort_left(
                cur_section_mapping.range_mappings,
                RawRangeMapping(source_start, dest_start, length),
                key=lambda x: x.source_start,
            )

    return seeds_to_plant, sections_mappings


def get_dest_id(
    source_id: int, source_type: str, sections_mappings: dict[str, RawSectionMapping]
) -> tuple[str, int, int] | None:
    if source_type not in sections_mappings:
        return None

    s = sections_mappings[source_type]
    dest_id, range_left = s.get_dest_index(source_id)
    dest_type = s.dest_type
    return dest_type, dest_id, range_left


def get_deps_chain_for_seed(
    seed_index: int, sections_mappings: dict[str, RawSectionMapping]
) -> list[tuple[str, int, int]]:
    deps_chain: list[tuple[str, int, int]] = []
    cur_src_type, cur_src_index = "seed", seed_index
    while True:
        dest_id = get_dest_id(cur_src_index, cur_src_type, sections_mappings)
        if dest_id is None:
            break

        dst_type, dst_index, range_left = dest_id
        deps_chain.append((cur_src_type, cur_src_index, range_left))
        deps_chain.append((dst_type, dst_index, -1))
        cur_src_type, cur_src_index = dst_type, dst_index

    return deps_chain


def part1() -> None:
    seeds_to_plant, sections_mappings = load_input("input.txt")
    seeds_dep_chains: list[list[tuple[str, int]]] = [
        get_deps_chain_for_seed(seed_index, sections_mappings) for seed_index in seeds_to_plant
    ]
    seeds_dep_chains.sort(key=lambda x: x[-1][1])

    print(f"Seed {seeds_dep_chains[0][0][1]} is the first seed to be planted @ location {seeds_dep_chains[0][-1][1]}")


def part2() -> None:
    seeds_to_plant, sections_mappings = load_input("input.txt")
    seeds_to_plant_ranges: list[tuple[int, int]] = []
    for i in range(0, len(seeds_to_plant), 2):
        seeds_to_plant_ranges.append((seeds_to_plant[i], seeds_to_plant[i + 1]))

    seeds_dep_chains: list[list[tuple[str, int]]] = []

    for seed_range_start, seed_range_len in seeds_to_plant_ranges:
        for seed_index in range(seed_range_start, seed_range_start + seed_range_len):
            seeds_dep_chains.append(get_deps_chain_for_seed(seed_index, sections_mappings))

    seeds_dep_chains.sort(key=lambda x: x[-1][1])

    print(f"Seed {seeds_dep_chains[0][0][1]} is the first seed to be planted @ location {seeds_dep_chains[0][-1][1]}")


if __name__ == "__main__":
    part1()
    part2()

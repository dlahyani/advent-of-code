
from functools import cmp_to_key
from itertools import chain


def compare(v1, v2) -> int:
    if type(v1) == int and type(v2) == int:
        return v1 - v2
    elif type(v1) == list and type(v2) == list:
        for i in range(min(len(v1), len(v2))):
            if (c := compare(v1[i], v2[i])) != 0:
                return c
        return len(v1) - len(v2)
    elif type(v1) == int and type(v2) == list:
        return compare([v1], v2)
    return compare(v1, [v2])


### Load input
packet_pairs = [[eval(p.strip()) for p in pp.split("\n")] for pp in open("2022/13/input.txt").read().split("\n\n")]

### Part 1
right_order_pairs = list(filter(
    lambda i: compare(packet_pairs[i-1][0], packet_pairs[i-1][1]) <= 0,
    range(1, len(packet_pairs)+1)
))
print(f"Sum of right order packet pairs indices: {sum(right_order_pairs)}")

### Part 2
dividers = [[[2]], [[6]]]    
sorted_packets = sorted(list(chain.from_iterable(packet_pairs)) + dividers, key=cmp_to_key(compare))
dividers_indices = sorted_packets.index(dividers[0]) + 1, sorted_packets.index(dividers[1]) + 1
print(f"Decoder key for distress signal is: {dividers_indices[0] * dividers_indices[1]}")
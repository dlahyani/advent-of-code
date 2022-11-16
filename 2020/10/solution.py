from collections import Counter
from typing import Dict, Tuple, Iterable


adapters = sorted([int(l[:-1]) for l in open("2020/10/input.txt").readlines()])
adapters = [0] + adapters + [adapters[-1]+3]
diffs = [adapters[i+1] - adapters[i] for i in range(len(adapters)-1)]
diffs_counter = Counter(diffs)
print("Part 1 solution: ", diffs_counter[1] * diffs_counter[3])


# In order to calculate all possible arrangements we will have to identify an "optional" adapter in
# the given adapter-set and then calculate the number of possible arrangements with and without this
# adapter. We need to calculate both options and we can't just multiply by 2 because omitting an
# optional adapter defines a new set of adapters which may impact the necessity of other adapters.
# For example in this adapter-set: {0, 1, 2, 4, 7}, adapter 1 is clearly optional and can be omitted,
# however if omitted we are left with a new adapter-set {0, 2, 4, 7} in which adapter 2 is mandatory.
# But if adapter 1 is used then adapter 2 becomes optional as this is also a valid adapter-set
# {0, 1, 4, 7}.
# This split will be required for every optional adapter we find. This is basically means we have an
# exponential runtime complexity with the number of optional adapters as the exponent.
# One way to improve performance is to use dynamic programming approach - break down the problem to
# smaller similar problems and use a cache to store results of values that we calculate over and
# over again. To do this we examine the adapters one by one, if we identify an optional adapter we
# will split the calculation and count the possible sets with and without this adapter by considering
# only adapters left.
#
# For example given this adapter-set {0, 1, 2, 4, 5, 8} the call tree will look like this:
# 0, 1, 2, 4, 5, 8 -> 5
#   1, 2, 4, 5, 8 -> 3
#     2, 4, 5, 8 -> 2
#       4, 5, 8 -> 1
#         5, 8 -> 1
#       2, 5, 8 -> 1
#         5, 8 -> 1
#     1, 4, 5, 8 -> 1
#       4, 5, 8 -> 1
#         5, 8 -> 1
#   0, 2, 4, 5, 8 -> 2
#     2, 4, 5, 8 -> 2
#       4, 5, 8 -> 1
#         5, 8 -> 1
#       2, 5, 8 -> 1
#         5, 8 -> 1
def count_arrangements(adapters: Tuple[int], cache: Dict[Tuple[int], int] = {}):
    if adapters in cache:
        return cache[adapters]
    
    if len(adapters) < 3:
        return 1
    
    res = count_arrangements(adapters[1:], cache)
    
    is_optional = (adapters[2] - adapters[0]) <= 3
    if is_optional:
        res += count_arrangements((adapters[0],) + adapters[2:], cache)
        
    cache[adapters] = res
    return res

print("Part 2 solution (fast): ", count_arrangements(tuple(adapters)))

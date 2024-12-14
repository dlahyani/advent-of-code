
from typing import Callable, Iterator
from functools import cmp_to_key

PageOrderingMap = dict[int, tuple[set[int], set[int]]]
PageOrderComparator = Callable[[int, int], int]

def build_rules_dict(rules) -> PageOrderingMap:
    rules_by_page: PageOrderingMap = {}
    for p1, p2 in rules:
        if p1 not in rules_by_page:
            rules_by_page[p1] = set(), set()
        rules_by_page[p1][0].add(p2)
        
        if p2 not in rules_by_page:
            rules_by_page[p2] = set(), set()
        rules_by_page[p2][1].add(p1)
    
    return rules_by_page

def get_page_order_comparator(page_ordering_map: PageOrderingMap) -> PageOrderComparator:
    def page_order_comparator(p1: int, p2: int) -> int:
        if p1 in page_ordering_map and p2 in page_ordering_map[p1][0]:
            return -1
        if p1 in page_ordering_map and p2 in page_ordering_map[p1][1]:
            return 1
        return 0
    
    return page_order_comparator


def is_update_correctly_ordered(update: tuple[int, ...], page_order_comparator: PageOrderComparator) -> bool:
    return all(page_order_comparator(update[i - 1], update[i]) <= 0 for i in range(1, len(update)))


with open("2024/05/input.txt", "r") as f:
    data = [l.strip() for l in f.readlines()]

section_separator = data.index("")
rules = [tuple(map(int, l.split("|"))) for l in data[:section_separator]]
updates = [tuple(map(int, l.split(","))) for l in data[section_separator + 1:]]
page_order_map = build_rules_dict(rules)
comparator = get_page_order_comparator(page_order_map)

# Part 1:
correctly_ordered_updates = [u for u in updates if is_update_correctly_ordered(u, comparator)]
s = sum(u[len(u) // 2] for u in correctly_ordered_updates)
print(s)
        

# Part 2:
incorrectly_ordered_updates = [u for u in updates if not is_update_correctly_ordered(u, comparator)]
fixed_order_updates = [tuple(sorted(u, key=cmp_to_key(comparator))) for u in incorrectly_ordered_updates]
s = sum(u[len(u) // 2] for u in fixed_order_updates)
print(s)

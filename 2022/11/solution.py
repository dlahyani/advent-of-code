from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
import regex

@dataclass
class Item:
    worry_level: int
    
    def add(self, b: int):
        self.worry_level += b
            
    def mul(self, b: int):
        self.worry_level *= b
        
    def div(self, b: int):
        self.worry_level //= b
    
    def sqr(self):
        self.worry_level *= self.worry_level
    
    def is_divisible(self, d: int) -> bool:
        return self.worry_level % d == 0

@dataclass
class ModulusItem:
    base_worry_level: int
    modulus_worry_levels: dict[int, int] | None = None
    
    def init_modulus_worry_levels(self, dividers: list[int]):
        self.modulus_worry_levels = {d: self.base_worry_level % d for d in dividers}
    
    def add(self, b: int):
        self.modulus_worry_levels = {d: (v + b) % d for d, v in self.modulus_worry_levels.items()}
            
    def mul(self, b: int):
        self.modulus_worry_levels = {d: (v * b) % d for d, v in self.modulus_worry_levels.items()}

    def sqr(self):
        self.modulus_worry_levels = {d: (v * v) % d for d, v in self.modulus_worry_levels.items()}
    
    def is_divisible(self, d: int) -> bool:
        return self.modulus_worry_levels[d] == 0


@dataclass
class Monkey:
    id: int
    items: list[Item | ModulusItem]
    inspect_item: Callable[[int], None]
    divider: int
    determine_next_monkey: Callable[[int], int]
    
    @classmethod
    def from_descriptor(cls, descriptor: str, item_cls) -> Monkey:
        d_lines = [l.strip() for l in descriptor.split("\n")]
        monkey_id = int(regex.match("^Monkey (\d+):$", d_lines[0]).groups()[0])
        starting_items = [item_cls(int(i)) for i in regex.match("^Starting items: ((\d+),? ?)+$", d_lines[1]).captures(2)]
        inspector = cls.get_item_inspector(d_lines[2])
        decider, divider = cls.get_divisibility_decider(d_lines[3:6])
        return Monkey(monkey_id, starting_items, inspector, divider, decider)

    @staticmethod    
    def get_item_inspector(d_line: str):
        m = regex.match("^Operation: new = old (\*|\+) (\d+|old)", d_line)
        op, right = m.groups()
        def inspect_operation(item: Item):
            if op == "+":
                item.add(int(right))
            else:
                if right == "old":
                    item.sqr()
                else:
                    item.mul(int(right))
        
        return inspect_operation

    @staticmethod
    def get_divisibility_decider(d_lines: list[str]):
        divider = int(regex.match("^Test: divisible by (\d+)", d_lines[0]).groups()[0])
        true_target = int(regex.match("^If true: throw to monkey (\d+)$", d_lines[1]).groups()[0])
        false_target = int(regex.match("^If false: throw to monkey (\d+)$", d_lines[2]).groups()[0])
        def decider(item: Item) -> int:
            return true_target if item.is_divisible(divider) else false_target
        return decider, divider


def process_input(raw_input: str, modulus: bool = False) -> list[Monkey]:
    item_class = ModulusItem if modulus else Item
    monkeys: list[Monkey] = [Monkey.from_descriptor(d, item_class) for d in raw_input.split("\n\n")]
    if not modulus:
        return monkeys
    
    dividers: list[int] = [m.divider for m in monkeys]
    for m in monkeys:
        for i in m.items:
            i.init_modulus_worry_levels(dividers)
    return monkeys
    

def play_round(monkeys: list[Monkey], relief: bool = True) -> list[int]:
    inspection_counters: list[int] = [0] * len(monkeys)
    for m in monkeys:
        while len(m.items) > 0:
            i = m.items.pop(0)
            m.inspect_item(i)
            inspection_counters[m.id] += 1
            if relief:
                i.div(3)
            next_monkey = m.determine_next_monkey(i)
            monkeys[next_monkey].items.append(i)
    
    return inspection_counters

raw_input = open("2022/11/input.txt").read()
monkeys = process_input(raw_input)

### Part 1
counters = [play_round(monkeys) for _ in range(20)]
total_counters = [sum(c) for c in zip(*counters)]
top1, top2 = sorted(total_counters, reverse=True)[0:2]
print(top1*top2)


### Part 2

monkeys = process_input(raw_input, True)
counters = [play_round(monkeys, False) for _ in range(10000)]
total_counters = [sum(c) for c in zip(*counters)]
top1, top2 = sorted(total_counters, reverse=True)[0:2]
print(top1*top2)

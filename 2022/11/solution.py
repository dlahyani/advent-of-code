from dataclasses import dataclass
import math
import regex


@dataclass
class Monkey:
    id: int
    items: list[int]
    operator: str
    right_operand: str
    divider: int
    next_monkey_true: int
    next_monkey_false: int

    @classmethod
    def from_descriptor(cls, descriptor: str) -> "Monkey":
        d_lines = [l.strip() for l in descriptor.split("\n")]
        monkey_id = int(regex.match("^Monkey (\d+):$", d_lines[0]).groups()[0])
        starting_items = [int(i) for i in regex.match("^Starting items: ((\d+),? ?)+$", d_lines[1]).captures(2)]
        operator, right_operand = regex.match("^Operation: new = old (\*|\+) (\d+|old)", d_lines[2]).groups()
        divider = int(regex.match("^Test: divisible by (\d+)", d_lines[3]).groups()[0])
        true_target = int(regex.match("^If true: throw to monkey (\d+)$", d_lines[4]).groups()[0])
        false_target = int(regex.match("^If false: throw to monkey (\d+)$", d_lines[5]).groups()[0])
        return Monkey(
            id=monkey_id,
            items=starting_items,
            operator=operator,
            right_operand=right_operand,
            divider=divider,
            next_monkey_true=true_target,
            next_monkey_false=false_target,
        )

    def inspect_item(self, item: int) -> int:
        return (
            item + int(self.right_operand)
            if self.operator == "+"
            else (item * item if self.right_operand == "old" else item * int(self.right_operand))
        )

    def next_monkey(self, item: int) -> int:
        return self.next_monkey_true if item % self.divider == 0 else self.next_monkey_false


def process_input(raw_input: str) -> list[Monkey]:
    return [Monkey.from_descriptor(d) for d in raw_input.split("\n\n")]


def play_round(monkeys: list[Monkey], relief: bool = True, common_divisor: int = 0) -> list[int]:
    inspection_counters: list[int] = [0] * len(monkeys)
    for m in monkeys:
        while len(m.items) > 0:
            i = m.items.pop(0)
            i = m.inspect_item(i)
            inspection_counters[m.id] += 1
            if relief:
                i //= 3
            else:
                i %= common_divisor
            next_monkey = m.next_monkey(i)
            monkeys[next_monkey].items.append(i)

    return inspection_counters


raw_input = open("2022/11/input.txt").read()
monkeys = process_input(raw_input)

### Part 1
counters = [play_round(monkeys) for _ in range(20)]
total_counters = [sum(c) for c in zip(*counters)]
top1, top2 = sorted(total_counters, reverse=True)[0:2]
print(top1 * top2)


### Part 2
common_divisor = math.prod([m.divider for m in monkeys])
counters = [play_round(monkeys, False, common_divisor) for _ in range(10000)]
total_counters = [sum(c) for c in zip(*counters)]
top1, top2 = sorted(total_counters, reverse=True)[0:2]
print(top1 * top2)

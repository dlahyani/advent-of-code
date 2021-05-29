from enum import Enum
from typing import Any, Iterable, Dict, Tuple

import regex


class RuleType(Enum):
    SimpleRule = 0
    ChainedRule = 1,
    FlexRule = 2,


class RuleDescriptor:
    def __init__(self, rule_type: RuleType, rule_data: Any):
        self.type = rule_type
        self.data = rule_data


RulesMap = Dict[int, RuleDescriptor]


def match_rule(rule_id: int, line: str, rules_map: RulesMap, index: int = 0, match_all: bool = True) -> bool:
    matched = _match_rule(rules_map[rule_id], line, rules_map, index)
    if matched == 0:
        return False

    print(f"'{line[:index]}[{line[index:index+matched]}]{line[index+matched:]}' {matched} chars matched rule #{rule_id}")
    return matched if not match_all or matched + index == len(line) else 0


def _match_rule(rule: RuleDescriptor, line: str, rules_map: RulesMap, index: int = 0) -> int:
    if rule.type == RuleType.SimpleRule:
        return _match_simple_rule(rule, line, rules_map, index)
    elif rule.type == RuleType.ChainedRule:
        return _match_chained_rule(rule, line, rules_map, index)
    elif rule.type == RuleType.FlexRule:
        return _match_flex_rule(rule, line, rules_map, index)

    raise ValueError(f"Invalid rule type, rule ID={rule.id}, rule type={rule.type}")


def _match_simple_rule(rule: RuleDescriptor, line: str, _: RulesMap, index: int = 0) -> int:
    return len(rule.data) if line.startswith(rule.data, index) else 0


def _match_chained_rule(rule: RuleDescriptor, line: str, rules_map: RulesMap, index: int = 0) -> int:
    sub_rules = rule.data
    total_matched = 0
    for sr in sub_rules:
        sub_rule = rules_map[sr]
        matched = _match_rule(sub_rule, line, rules_map, index + total_matched)
        if matched == 0:
            return 0
        total_matched += matched

    return total_matched


def _match_flex_rule(rule: RuleDescriptor, line: str, rules_map: RulesMap, index: int = 0) -> Tuple[int]:
    chained_rules_groups: Tuple[Tuple[int]] = rule.data
    for crg in chained_rules_groups:
        sub_rule = RuleDescriptor(RuleType.ChainedRule, crg)
        matched = _match_rule(sub_rule, line, rules_map, index)
        if matched > 0:
            return matched

    return 0


def parse_rules(rules: Iterable[str]) -> RulesMap:
    parsed_rules = [parse_rule(r) for r in rules]
    return {rule_id: rule for rule_id, rule in parsed_rules}


def parse_rule(rule: str) -> Tuple[int, RuleDescriptor]:
    return _parse_simple_rule(rule) or _parse_compound_rule(rule)


def _parse_simple_rule(rule: str):
    SIMPLE_RULE_PATTERN = r'(\d+): ("[a-z]+")'

    m = regex.match(SIMPLE_RULE_PATTERN, rule)
    if not m:
        return None

    groups = m.groups()
    rule_id = int(groups[0])
    rule_str = groups[1][1:-1]

    # print(f"Rule #{rule_id}: Simple, {rule_str}")
    return rule_id, RuleDescriptor(RuleType.SimpleRule, rule_str)


def _parse_compound_rule(rule: str):
    COMPOUND_RULE_PATTERN = r'(\d+):( \d+)+( \|( \d+)+)?'

    m = regex.match(COMPOUND_RULE_PATTERN, rule)
    if not m:
        return None

    groups = m.groups()
    rule_type = RuleType.ChainedRule
    rule_id = int(groups[0])
    sub_rules = tuple(int(sr) for sr in m.captures(2))

    if m.captures(4):
        rule_type = RuleType.FlexRule
        sub_rules = (sub_rules, tuple(int(sr) for sr in m.captures(4)))

    # print(f"Rule #{rule_id}: {'Chained' if rule_type == RuleType.ChainedRule else 'Flex'}, {sub_rules}")
    return rule_id, RuleDescriptor(rule_type, sub_rules)


def main():
    lines = open("2020/19/input.txt", "r").readlines()
    rules_strings_separator = lines.index("\n")
    raw_rules = lines[:rules_strings_separator]
    strings = [line[:-1] for line in lines[rules_strings_separator + 1:]]

    print(f"# of rules: {len(raw_rules)}")
    print(f"# of strings: {len(strings)}")

    rules_map = parse_rules(raw_rules)

    # Part 1:
    lines_matching_rule_0 = set(filter(lambda s: match_rule(0, s, rules_map) > 0, strings))
    print(f"Number of lines matching rule #0: {len(lines_matching_rule_0)}")

    # Part 2


if __name__ == "__main__":
    main()

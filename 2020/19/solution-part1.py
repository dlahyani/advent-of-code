from enum import Enum
from typing import Any, Iterable, Dict, Tuple, Callable, Protocol

import regex


class Rule(Protocol):
    def match(self, line: str, index: int = 0, match_all: bool = False) -> int:
        pass


class SimpleRule:
    def __init__(self, rule_str: str):
        self.rule_str = rule_str

    def match(self, line: str, index: int = 0, match_all: bool = False) -> int:
        matched = len(self.rule_str) if line[index:].startswith(self.rule_str) else 0
        return matched if not match_all or index + matched == len(line) else 0

    def __repr__(self):
        return f"<SimpleRule: '{str(self)}'>"

    def __str__(self):
        return self.rule_str


class ChainedRule:
    def __init__(self, sub_rules: Tuple[Rule]):
        self.sub_rules = sub_rules

    def match(self, line: str, index: int = 0, match_all: bool = False) -> int:
        total_digested = 0
        for rule in self.sub_rules:
            digested = rule.match(line, index + total_digested)
            if digested == 0:
                return 0
            assert index + total_digested + digested <= len(line)
            total_digested += digested

        return total_digested if not match_all or index + total_digested == len(line) else 0

    def __repr__(self):
        return f"<ChainedRule: '{str(self)}'>"

    def __str__(self):
        return '+'.join([str(sr) for sr in self.sub_rules])


class FlexRule:
    def __init__(self, sub_rules: Tuple[Rule]):
        self.sub_rules = sub_rules

    def match(self, line: str, index: int = 0, match_all: bool = False) -> int:
        for rule in self.sub_rules:
            digested = rule.match(line, index, match_all)
            assert index + digested <= len(line)
            if digested != 0:
                return digested

        return 0

    def __repr__(self):
        return f"<FlexRule: '{str(self)}'>"

    def __str__(self):
        return "(" + " | ".join([str(sr) for sr in self.sub_rules]) + ")"


def _parse_simple_rule(rule: str):
    SIMPLE_RULE_PATTERN = '(\d+): ("[a-z]+")'

    m = regex.match(SIMPLE_RULE_PATTERN, rule)
    if not m:
        return None
    
    groups = m.groups()
    rule_id = int(groups[0])
    rule_str = groups[1][1:-1]
    return rule_id, SimpleRule, rule_str


def _parse_compound_rule(rule: str):
    COMPOUND_RULE_PATTERN = '(\d+):( \d+)+( \|( \d+)+)?'

    m = regex.match(COMPOUND_RULE_PATTERN, rule)
    if not m:
        return None

    groups = m.groups()
    rule_type = ChainedRule
    rule_id = int(groups[0])
    sub_rules = (int(sr) for sr in m.captures(2))

    if m.captures(4):
        rule_type = FlexRule
        sub_rules = (sub_rules, (int(sr) for sr in m.captures(4)))

    assert (('|' in rule and rule_type == FlexRule) or rule_type == ChainedRule)

    return rule_id, rule_type, sub_rules


def parse_rule(rule: str) -> Rule:
    return _parse_simple_rule(rule) or _parse_compound_rule(rule)

ParsedRulesMap = Dict[int, Tuple[Callable, Any]]


def parse_rules(rules: Iterable[str]) -> ParsedRulesMap:
    parsed_rules = [parse_rule(r) for r in rules]
    return {rule_id: (rule_type, params) for rule_id, rule_type, params in parsed_rules}


def build_rules(rules: ParsedRulesMap) -> Dict[int, Rule]:
    built_rules = {}
    for rid in rules:
        _build_rule(rules, built_rules, rid)
    return built_rules


def _build_rule(rules, built_rules, rule_id):
    if rule_id in built_rules:
        return

    rule_type, params = rules[rule_id]

    if rule_type == SimpleRule:
        built_rules[rule_id] = rule_type(params)
    elif rule_type == ChainedRule:
        sub_rules = []
        for srid in params:
            sub_rules.append(
                built_rules[srid] if srid in built_rules else
                _build_rule(rules, built_rules, srid)
            )
        built_rules[rule_id] = rule_type(tuple(sub_rules))
    else:
        flex_rule_sub_rules = []
        for chained_group in params:
            chained_rule_sub_rules = []
            for srid in chained_group:
                chained_rule_sub_rules.append(
                    built_rules[srid] if srid in built_rules else
                    _build_rule(rules, built_rules, srid)
                )
            chained_sub_rule = ChainedRule(tuple(chained_rule_sub_rules))
            flex_rule_sub_rules.append(chained_sub_rule)

        built_rules[rule_id] = rule_type(tuple(flex_rule_sub_rules))

    return built_rules[rule_id]


def main():
    lines = open("2020/19/input.txt", "r").readlines()
    rules_strings_separator = lines.index("\n")
    raw_rules = lines[:rules_strings_separator]
    strings = [l[:-1] for l in lines[rules_strings_separator + 1:]]

    print(f"# of rules: {len(raw_rules)}")
    print(f"# of strings: {len(strings)}")

    parsed_rules = parse_rules(raw_rules)
    rules = build_rules(parsed_rules)

    # Part 1:
    lines_matching_rule_0 = list(filter(lambda s: rules[0].match(s, 0, True) != 0, strings))
    print("\n".join(lines_matching_rule_0))
    print(f"Number of lines matching rule #0: {len(list(lines_matching_rule_0))}")


if __name__ == "__main__":
    main()

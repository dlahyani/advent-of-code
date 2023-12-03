from enum import Enum
from typing import Iterable, Dict, Tuple, Callable, Union
import regex


class RuleType(Enum):
    SimpleRule = (0,)
    ChainedRule = (1,)
    FlexRule = 2


SimpleRuleData = str
CompoundRuleData = Tuple[int]
FlexRuleData = Tuple[Union[SimpleRuleData, CompoundRuleData]]
RuleDesc = Tuple[RuleType, Union[SimpleRuleData, CompoundRuleData, FlexRuleData]]
RulesMap = Dict[int, RuleDesc]


class RuleParser:
    SIMPLE_RULE_PATTERN = r'(\d+): ("[a-z]+")'
    COMPOUND_RULE_PATTERN = r"(\d+):( \d+)+( \|( \d+)+)?"

    @classmethod
    def parse_rule(cls, rule: str) -> Tuple[int, RuleDesc]:
        return cls._parse_simple_rule(rule) or cls._parse_compound_rule(rule)

    @classmethod
    def parse_rules(cls, rules: Iterable[str]) -> RulesMap:
        parsed_rules = [cls.parse_rule(r) for r in rules]
        return {rule_id: rule_desc for rule_id, rule_desc in parsed_rules}

    @staticmethod
    def _parse_simple_rule(rule: str) -> Tuple[int, type, str]:
        m = regex.match(RuleParser.SIMPLE_RULE_PATTERN, rule)
        if not m:
            return None

        groups = m.groups()
        rule_id = int(groups[0])
        rule_str = groups[1][1:-1]
        return rule_id, (RuleType.SimpleRule, rule_str)

    @staticmethod
    def _parse_compound_rule(rule: str):
        m = regex.match(RuleParser.COMPOUND_RULE_PATTERN, rule)
        if not m:
            return None

        groups = m.groups()
        rule_type = RuleType.ChainedRule
        rule_id = int(groups[0])
        sub_rules = tuple(int(sr) for sr in m.captures(2))

        if m.captures(4):
            rule_type = RuleType.FlexRule
            sub_rules = (sub_rules, tuple(int(sr) for sr in m.captures(4)))

        return rule_id, (rule_type, sub_rules)


class RuleRegexifier:
    def __init__(self, rules_map: RulesMap):
        self._rules_map = rules_map
        self._max_depth = 100

    def regexify_rule(self, rule_id: int):
        rule_desc = self._rules_map[rule_id]
        return "^" + self._regexify_rule(rule_desc) + "$"

    def _regexify_rule(self, rule_desc: RuleDesc, depth: int = 0):
        if depth > self._max_depth:
            return ""

        rule_type = rule_desc[0]
        if rule_type == RuleType.SimpleRule:
            return self._regexify_simple_rule(rule_desc, depth)
        elif rule_type == RuleType.ChainedRule:
            return self._regexify_chained_rule(rule_desc, depth)
        return self._regexify_flex_rule(rule_desc, depth)

    def _regexify_simple_rule(self, rule: RuleDesc, _: int) -> str:
        return rule[1]

    def _regexify_chained_rule(self, rule: RuleDesc, depth: int) -> str:
        return "".join([self._regexify_rule(self._rules_map[sub_rule], depth + 1) for sub_rule in rule[1]])

    def _regexify_flex_rule(self, rule: RuleDesc, depth: int) -> str:
        rule_regex = "("
        sub_chains = rule[1]
        for i in range(len(sub_chains)):
            chained_rule = (RuleType.ChainedRule, sub_chains[i])
            rule_regex += self._regexify_rule(chained_rule, depth + 1)
            if i < len(sub_chains) - 1:
                rule_regex += "|"
        rule_regex += ")"
        return rule_regex


def solution_for_input(input_filename: str):
    lines = open(input_filename, "r").readlines()
    rules_strings_separator = lines.index("\n")
    raw_rules = lines[:rules_strings_separator]
    strings = [line[:-1] for line in lines[rules_strings_separator + 1 :]]

    print(f"# of rules: {len(raw_rules)}")
    print(f"# of strings: {len(strings)}")

    rules_map = RuleParser.parse_rules(raw_rules)
    regexifier = RuleRegexifier(rules_map)

    r0_regex = regexifier.regexify_rule(0)
    lines_matching_r0_regex = filter(lambda l: regex.match(r0_regex, l) is not None, strings)
    print(f"Number of lines matching rule #0 regex: {len(list(lines_matching_r0_regex))}")


def main():
    # Part 1:
    print("********* Part 1:")
    solution_for_input("2020/19/input.txt")

    # Part 2:
    print("********** Part 2:")
    solution_for_input("2020/19/input2.txt")


if __name__ == "__main__":
    main()

from dataclasses import dataclass
from typing import Dict, Iterable, List

#############################
## Models


@dataclass
class Range:
    min_value: int
    max_value: int

    def is_value_in_range(self, value) -> bool:
        return self.min_value <= value <= self.max_value

    @classmethod
    def from_str(cls, range_str: str) -> "Range":
        min_value, max_value = range_str.split("-")
        return cls(int(min_value), int(max_value))


@dataclass
class RangeSet:
    ranges: List[Range]

    def is_value_in_range_set(self, value):
        return any([r.is_value_in_range(value) for r in self.ranges])

    @classmethod
    def from_str(cls, range_set_str: str) -> "RangeSet":
        return cls([Range.from_str(r) for r in range_set_str.split(" or ")])


@dataclass
class Rule:
    field_name: str
    valid_ranges: RangeSet

    def is_valid_value(self, value: int) -> bool:
        return self.valid_ranges.is_value_in_range_set(value)

    def are_all_values_valid(self, values: Iterable[int]) -> bool:
        return all([self.is_valid_value(v) for v in values])

    @classmethod
    def from_str(cls, rule_str: str) -> "Rule":
        name, ranges = rule_str.split(": ")
        return cls(name, RangeSet.from_str(ranges))


Ticket = Iterable[int]

#############################
## Logic


def parse_rules(raw_rules: List[str]) -> List[Rule]:
    return [Rule.from_str(r) for r in raw_rules]


def parse_tickets(raw_tickets: Iterable[str]) -> List[Ticket]:
    return [[int(v) for v in t.split(",")] for t in raw_tickets]


def is_valid_value(rules: Iterable[Rule], value: int) -> bool:
    return any([r.is_valid_value(value) for r in rules])


def ticket_invalid_values(rules: Iterable[Rule], ticket: Ticket) -> List[int]:
    """
    Returns a list of all values in the given `ticket` that are not valid according to any of the
    given set  of `rules`. If every value in `ticket` is valid according to at least one rule then
    an empty list is returned.
    """
    return list(filter(lambda v: not is_valid_value(rules, v), ticket))


def _get_matching_columns_per_field(rules: Iterable[Rule], columns: List[int]) -> Dict[str, List[int]]:
    """
    Find which columns potentially match to every field based on the given set of `rules`. A column
    is a potential match for a specific field if ALL the values in this column adhere to the rules
    of that field.

    Returns a dictionary where each key is a name of a field and the value is a list of indexes of
    potentially matching columns.
    """
    col_count = len(columns)
    return {r.field_name: [c for c in range(col_count) if r.are_all_values_valid(columns[c])] for r in rules}


def _unique_field_to_col_matching(
    rules: Iterable[Rule], field_to_matching_cols: Dict[str, List[int]]
) -> Dict[str, int]:
    """
    Given a potential field to column matching this functions tries to determine a unique 1-to-1
    matching.

    Returns a dictionary in which each key is a name of a filed and the value is the index of the
    best matching column.
    """
    # This method works by elimination - we give higher priority to fields with less potential
    # matches. We determine their best matching column and then we can eliminate that column for
    # other fields.
    sorted_rules = sorted(rules, key=lambda r: len(field_to_matching_cols[r.field_name]))
    unallocated_columns = set(range(len(rules)))
    field_to_col = {}
    for r in sorted_rules:
        col = [c for c in field_to_matching_cols[r.field_name] if c in unallocated_columns][0]
        field_to_col[r.field_name] = col
        unallocated_columns.remove(col)

    return field_to_col


def identify_tickets_fields(rules: Iterable[Rule], tickets: Iterable[Ticket]) -> Dict[str, int]:
    """
    Based on the given set of `rules` this function finds a 1-to-1 mapping from field names (as
    defined in the `rules`) to a the index of that field in the given set of `tickets`.

    Note: We assume that fields consistently appear in the same position in all tickets.

    Returns a dictionary in which each key is a name of a filed and the value is the index of that
    field in the tickets.
    """
    columns = list(zip(*tickets))
    field_to_matching_cols = _get_matching_columns_per_field(rules, columns)
    return _unique_field_to_col_matching(rules, field_to_matching_cols)


def ticket_departure_product(ticket: Ticket, field_to_col: Dict[str, int]) -> int:
    departure_fields_product = 1
    for f, c in field_to_col.items():
        if f.startswith("departure"):
            departure_fields_product *= my_ticket[c]
    return departure_fields_product


if __name__ == "__main__":
    sections = open("2020/16/input.txt", "r").read().split("\n\n")
    rules = parse_rules(raw_rules=sections[0].split("\n"))
    my_ticket = parse_tickets(sections[1].split("\n")[1:])[0]
    nearby_tickets = parse_tickets(sections[2].split("\n")[1:])

    # Part 1
    invalid_values = [ticket_invalid_values(rules, t) for t in nearby_tickets]
    invalid_values_sum = sum([sum(iv) for iv in invalid_values])
    print(f"Sum of invalid values: {invalid_values_sum}")

    # Part 2
    valid_tickets = [nearby_tickets[i] for i in range(len(nearby_tickets)) if not invalid_values[i]]
    field_to_col = identify_tickets_fields(rules, valid_tickets)
    departure_fields_product = ticket_departure_product(my_ticket, field_to_col)
    print(departure_fields_product)

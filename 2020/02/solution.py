from collections import Counter
from dataclasses import dataclass
from re import match


@dataclass
class PasswordPolicy1:
    min_occurrences: int
    max_occurrences: int
    char: str

    def verify_policy(self, password):
        occurrences_of_char_in_password = Counter(password)[self.char]
        return (
            occurrences_of_char_in_password >= self.min_occurrences
            and occurrences_of_char_in_password <= self.max_occurrences
        )


@dataclass
class PasswordPolicy2:
    index_1: int
    index_2: int
    char: str

    def verify_policy(self, password):
        return (password[self.index_1 - 1] == self.char) ^ (password[self.index_2 - 1] == self.char)


# Password line sample: 12-16 s: mzrhmvswtsgsxbpsj
LINE_FORMAT = "([\d]+)-(\d+) ([a-z]): ([a-z]+)"


def parse_input_line(line: str, password_policy_class):
    m = match(LINE_FORMAT, line)
    if not m:
        return None

    groups = m.groups()
    return password_policy_class(int(groups[0]), int(groups[1]), groups[2]), groups[3]


if __name__ == "__main__":
    lines = open("2020/02/input.txt").readlines()

    # Part 1
    pp_pairs = [parse_input_line(l, PasswordPolicy1) for l in lines]
    validity = [policy.verify_policy(password) for policy, password in pp_pairs]
    valid_count = Counter(validity)[True]
    print("Password policy 1")
    print(f"Total passwords: {len(pp_pairs)}, Valid passwords: {valid_count}")

    # Part 2
    pp_pairs = [parse_input_line(l, PasswordPolicy2) for l in lines]
    validity = [policy.verify_policy(password) for policy, password in pp_pairs]
    valid_count = Counter(validity)[True]
    print("Password policy 2")
    print(f"Total passwords: {len(pp_pairs)}, Valid passwords: {valid_count}")

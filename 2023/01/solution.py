import regex as re


def extract_calibration_values(line: str, allow_mnemonics: bool = False):
    mnemonics = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8", 
        "nine": "9",
    }
    regex = re.compile("(\d|%s)" % "|".join(mnemonics.keys())) if allow_mnemonics else re.compile("(\d)")
    matches = regex.findall(line, overlapped=True)
    d0, d1 = mnemonics.get(matches[0], matches[0]), mnemonics.get(matches[-1], matches[-1])
    return int(d0 + d1)
    

#### Part 1
with open("2023/01/input.txt", "r") as f:
    calibration_values = map(lambda l: extract_calibration_values(l, False), f)
    s = sum(calibration_values)
    print(f"Solution: {s}")


#### Part 2
with open("2023/01/input.txt", "r") as f:
    calibration_values = map(lambda l: extract_calibration_values(l, True), f)
    s = sum(calibration_values)
    print(f"Solution: {s}")

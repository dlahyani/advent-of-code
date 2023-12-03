from re import match
from typing import Dict


def verify_birth_year(birth_year: str) -> bool:
    return match("^[0-9]{4}$", birth_year) and 1920 <= int(birth_year) <= 2002


def verify_issue_year(issue_year: str) -> bool:
    return match("^[0-9]{4}$", issue_year) and 2010 <= int(issue_year) <= 2020


def verify_expiration_year(expiration_year: str) -> bool:
    return match("^[0-9]{4}$", expiration_year) and 2020 <= int(expiration_year) <= 2030


def verify_height(height: str) -> bool:
    try:
        h, u = match("^([0-9]+)(cm|in)$", height).groups()
        return (u == "cm" and 150 <= int(h) <= 193) or (u == "in" and 59 <= int(h) <= 76)
    except AttributeError:
        return False


def verify_hair_color(hair_color: str) -> bool:
    return match("^#[0-9a-f]{6}$", hair_color) is not None


def verify_eye_color(eye_color: str) -> bool:
    return eye_color in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def verify_passport_id(passport_id: str) -> bool:
    return match("^[0-9]{9}$", passport_id) is not None


PASSPORT_REQUIRED_FIELDS = {
    "byr": verify_birth_year,
    "iyr": verify_issue_year,
    "eyr": verify_expiration_year,
    "hgt": verify_height,
    "hcl": verify_hair_color,
    "ecl": verify_eye_color,
    "pid": verify_passport_id,
}


def create_passport(passport_raw: str) -> Dict[str, str]:
    """
    Convert raw textual passport to a dictionary of fields without validating the passport.
    """
    return {f[0]: f[1] for f in map(lambda p: p.split(":"), passport_raw.split())}


def verify_passport(passport: Dict[str, str]) -> bool:
    """
    Verify a passport in dictionary format.
    Returns True if the passport contains all required fields.
    """
    return all([f in passport for f in PASSPORT_REQUIRED_FIELDS])


def verify_passport_and_fields(passport: Dict[str, str]) -> bool:
    """
    Verify a passport in dictionary format.
    Returns True if the passport contains all required fields and all of them contain a valid value.
    """
    try:
        return all([f in passport and v(passport[f]) for f, v in PASSPORT_REQUIRED_FIELDS.items()])
    except ValueError:
        return False


if __name__ == "__main__":
    passports = [create_passport(p) for p in open("2020/04/input.txt", "r").read().split("\n\n")]

    # Part 1
    valid_passports = filter(verify_passport, passports)
    print(f"Valid passports: {len(list(valid_passports))}")

    # Part 2
    valid_passports = filter(verify_passport_and_fields, passports)
    print(f"Valid passports: {len(list(valid_passports))}")

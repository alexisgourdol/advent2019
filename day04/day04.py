import ipdb


INPUT = "134564-585159"

"""
- It is a six-digit number.
- The value is within the range given in your puzzle input.
- Two adjacent digits are the same (like 22 in 122345).
- Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

How many different passwords within the range given in your puzzle input meet these criteria?"""


def check_rules(pw: int) -> bool:
    """Returns True if all conditions for a valid password are met, False otherwise"""
    duplicated_digits = ["00", "11", "22", "33", "44", "55", "66", "77", "88", "99"]
    pw_str = str(pw)

    if len(pw_str) != 6:
        return False

    if not any(dd in pw_str for dd in duplicated_digits):
        return False

    for index, digit in enumerate(pw_str):
        if index == len(pw_str) - 1:
            break
        if int(digit) > int(pw_str[index + 1]):
            return False

    return True


def check_range(r: str = "134564-585159") -> int:
    upper, lower = int(r.partition("-")[0]), int(r.partition("-")[-1])
    return sum([check_rules(pw) for pw in range(upper, lower + 1)])


if __name__ == "__main__":

    print(check_range())

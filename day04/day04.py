import re
from collections import Counter
from typing import List

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


# Credits for part 2 : https://github.com/joelgrus/advent2019/blob/master/day04/day04.py


def is_increasing(ds: List[int]) -> bool:
    return all(x <= y for x, y in zip(ds, ds[1:]))


def has_group_of_two(ds: List[int]) -> bool:
    counts = Counter(ds)
    return any(v == 2 for v in counts.values())


def digits(n: int, num_digits: int = 6) -> List[int]:
    d = []
    for _ in range(num_digits):
        d.append(n % 10)
        n = n // 10
    return list(reversed(d))


def is_valid2(n: int) -> bool:
    d = digits(n)
    return is_increasing(d) and has_group_of_two(d)


def check_range(r: str = "134564-585159") -> int:
    upper, lower = int(r.partition("-")[0]), int(r.partition("-")[-1])
    return sum([check_rules(pw) for pw in range(upper, lower + 1)])


def check_range_2(r: str = "134564-585159") -> int:
    upper, lower = int(r.partition("-")[0]), int(r.partition("-")[-1])
    return sum([is_valid2(pw) for pw in range(upper, lower + 1)])


if __name__ == "__main__":

    print("Part 1", check_range())
    assert is_valid2(112233) == True
    assert is_valid2(123444) == False
    assert is_valid2(111122) == True
    print("Part 2", check_range_2())

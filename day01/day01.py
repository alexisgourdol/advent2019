import csv

### PART 1
def fuel_required(mass: int) -> int:
    """Computes fuel required for a given mass"""
    return mass // 3 - 2


def fuel_needs(modules_list: list) -> list:
    """Returns a list of fuel requirements for a list of masses (modules_list)"""
    return [fuel_required(m) for m in modules_list]


def main_01() -> int:
    """Processes the input of part 1"""
    with open("input.txt") as f:
        modules = [int(m) for m in f.readlines()]
        needs = fuel_needs(modules)
        return sum(needs)


### PART 2
def rec_ful_required(mass: int) -> int:
    """Recursively calls `fuel_required` as long as the result is positive. Returns the sum of fuel for one given mass"""
    res_list = []
    res = fuel_required(mass)
    res_list.append(res)
    while res > 0:
        res = fuel_required(res)
        if res > 0:
            res_list.append(res)

    return sum(res_list)


def main_02() -> int:
    """Processes the input of part 2"""
    with open("input.txt") as f:
        modules = [int(m) for m in f.readlines()]
        needs = [rec_ful_required(m) for m in modules]
        return sum(needs)


if __name__ == "__main__":
    # print(f"{fuel_required(12)=}")
    # print(f"{fuel_required(14)=}")
    # print(f"{fuel_required(1969)=}")
    # print(f"{fuel_required(100756)=}")
    # print(main_01())

    # print(f"{rec_ful_required(12)=}")
    # print(f"{rec_ful_required(14)=}")
    # print(f"{rec_ful_required(1969)=}")
    # print(f"{rec_ful_required(100756)=}")
    print(main_02())

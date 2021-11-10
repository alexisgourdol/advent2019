import csv

### PART 1
def fuel_required(mass: int) -> int:
    """Computes fuel required for a given mass"""
    return mass // 3 - 2


def fuel_needs(modules_list: list) -> list:
    """Returns a list of fuel requirements for a list of masses (modules_list)"""
    return [fuel_required(m) for m in modules_list]


### PART 2
def rec_ful_required(mass: int) -> int:
    """Recursively calls `fuel_required` as long as the result is positive. Returns the sum of fuel for one given mass"""
    total = 0
    next_fuel = fuel_required(mass)

    while next_fuel > 0:
        total += next_fuel
        next_fuel = fuel_required(next_fuel)

    return total


def main() -> int:
    """Processes the input"""
    with open("input.txt") as f:
        modules = [int(m) for m in f.readlines()]

        needs = fuel_needs(modules)
        print(f"Part 1 results :  {sum(needs)}")

        rec_needs = [rec_ful_required(m) for m in modules]
        print(f"Part 2 results :  {sum(rec_needs)}")

        return sum(rec_needs)


if __name__ == "__main__":
    assert fuel_required(12) == 2
    assert fuel_required(14) == 2
    assert fuel_required(1969) == 654
    assert fuel_required(100756) == 33583

    assert rec_ful_required(12) == 2
    assert rec_ful_required(1969) == 966
    assert rec_ful_required(100756) == 50346
    main()

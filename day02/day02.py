from typing import List, Sequence


def intcode(numbers: List, skip_error=True) -> List:

    start_position = 0

    while numbers[start_position] != 99:
        opcode, pos_1, pos_2, storage_position = (
            numbers[start_position],
            numbers[start_position + 1],
            numbers[start_position + 2],
            numbers[start_position + 3],
        )
        if opcode == 1:
            numbers[storage_position] = numbers[pos_1] + numbers[pos_2]
        elif opcode == 2:
            numbers[storage_position] = numbers[pos_1] * numbers[pos_2]
        else:
            if skip_error:
                continue
            else:
                raise RuntimeError(
                    f"beginning of sequence is not valid (not 1, 2 or 99): {numbers[start_position]}"
                )
        start_position += 4

    return numbers


### PART 2
TARGET = 19690720


def search(numbers: List) -> Sequence[int]:
    for noun in range(100):
        for verb in range(100):
            num = numbers[:]
            num[1], num[2] = noun, verb
            if intcode(num)[0] == TARGET:
                return noun, verb
            del num


if __name__ == "__main__":
    assert intcode([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]) == [
        3500,
        9,
        10,
        70,
        2,
        3,
        11,
        0,
        99,
        30,
        40,
        50,
    ]
    assert intcode([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99]
    assert intcode([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]
    assert intcode([2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801]
    assert intcode([1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99]

    with open("input.txt") as f:
        input = f.readline()
        numbers = [int(number) for number in input.split(",")]

        num = numbers[:]
        # before running the program, replace position 1 with the value 12 and replace position 2 with the value 2
        num[1], num[2] = 12, 2
        program = intcode(num)
        print(f"{program[0]=}")

        noun, verb = search(numbers)
        print(f"Solution part 2 with {noun=} and {verb=} : {100 * noun + verb}")

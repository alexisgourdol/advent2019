from typing import List, Optional
from time import sleep

# First, you'll need to add two new instructions:
def intcode(
    numbers: List,
    output_value: Optional[int] = None,
    input_value: int = 1,
    skip_error=True,
) -> List:

    start_position = 0
    # OUTPUT value needs to come from somewhere and be update someplace
    while numbers[start_position] != 99:
        opcode = numbers[start_position]
        pos_1 = left_term = numbers[start_position + 1]
        pos_2 = right_term = numbers[start_position + 2]
        storage_position = numbers[start_position + 3]
        # Second, you'll need to add support for parameter modes:
        print(start_position, "", numbers[:20], "...\n")
        if len(str(opcode)) > 3:
            mode_1st_param = int(str(opcode)[-3])
            mode_2nd_param = int(str(opcode)[-4])
            mode_3rd_param = int(str(opcode)[0]) if len(str(opcode)) == 5 else 0
            opcode = int(str(opcode)[-1])
            left_term = pos_1 if mode_1st_param == 1 else numbers[pos_1]
            right_term = pos_2 if mode_2nd_param == 1 else numbers[pos_2]
            # print(f"{mode_1st_param=}, {mode_2nd_param=}, {mode_3rd_param=}, {opcode=}")
            # print(f"{left_term=}, {right_term=}")
            sleep(1)
        if opcode == 1:
            numbers[storage_position] = left_term + right_term
            start_position += 4
        elif opcode == 2:
            numbers[storage_position] = left_term * right_term
            start_position += 4
        elif opcode == 3:
            numbers[pos_1] = input_value
            # output_value = input_value
            start_position += 2
        elif opcode == 4:
            output_value = numbers[pos_1]
            start_position += 2
        else:
            if skip_error:
                continue
            else:
                raise RuntimeError(
                    f"beginning of sequence is not valid (not 1, 2 or 99): {numbers[start_position]}"
                )

    return numbers


if __name__ == "__main__":
    with open("day05.txt") as f:
        inp = f.readline()
        # import ipdb

        # ipdb.set_trace()
        inp = [int(c) for c in inp.split(",")]
        intcode(inp)
